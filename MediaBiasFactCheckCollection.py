import time
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from data_standardization_helpers import get_url_from_news_title, get_bias_fact_cred, add_to_error_list, clean_url

class MediaBiasFactCheckCollection():
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def all_biases_collection(self, output_file = './all_bias_output.csv', manual_corrections=False):
        all_news_classifications = {}
        for bias in ['left', 'leftcenter', 'center', 'right-center', 'right']:
            (news_classifications, error_dict) = self.__collect_urls_by_bias(bias)
            if(manual_corrections):
                news_classifications = self.__add_missing_data(news_classifications, error_dict)
            for news in news_classifications:
                all_news_classifications[news] = news_classifications[news]
        self.__output_classifications(all_news_classifications, output_file)
        return

    def bias_based_collection(self, bias=None, output_file='./bias_output.csv', manual_corrections=False):
        valid_bias_inputs = ['left', 'left-center', 'center', 'right-center', 'right']
        if(bias not in valid_bias_inputs):
            print('must enter one of the following bias categories: left, left-center, center, right-center, right')
            return
        if(bias == 'left-center'): bias = 'leftcenter'
        (news_classifications_dict, error_dict) = self.__collect_urls_by_bias(bias)
        if(manual_corrections):
            news_classifications_dict = self.__add_missing_data(news_classifications_dict, error_dict)
        self.__output_classifications(news_classifications_dict, output_file)
        return

    def conspiracy_pseudoscience_collection(self, output_file='./conspiracy_output.csv', manual_corrections=False):
        url_dict = self.__collect_urls_from_webpage('https://mediabiasfactcheck.com/conspiracy/', manual_corrections)
        self.__output_urls_to_csv(url_dict, output_file, 'Conspiracy/Pseudoscience')

    def questionable_sources_collection(self, output_file='./questionable_output.csv', manual_corrections=False):
        url_dict = self.__collect_urls_from_webpage('https://mediabiasfactcheck.com/fake-news/', manual_corrections)
        self.__output_urls_to_csv(url_dict, output_file, 'Questionable/Fake')



    def __collect_urls_by_bias(self, bias):
        mbfc_dict = {}
        mbfc_url = 'https://mediabiasfactcheck.com/'
        mbfc_error_dict = {}
        url_bias_types = {'left': 'LEFT', 'leftcenter': 'LEFT-CENTER', 'right-center': 'RIGHT-CENTER', 'right': 'RIGHT', 'center': 'CENTER'}
        media_table_len = 100
        collected_counter = 0
        driver = None
        #while there are still news media in this category that have not be saved, keep restarting the browser and trying
        while(collected_counter < media_table_len): 
            try:
                #go to the bias website and iterate over the news orgs listed, saving their titles and associated classifications
                driver = self.__reset_browser(mbfc_url + bias, driver)
                media_table = driver.find_element_by_id('mbfc-table')
                media_table_len = len(media_table.find_elements_by_css_selector('a'))
                for media_index in range(media_table_len):  
                    media_table = driver.find_element_by_id('mbfc-table')
                    media_elem = media_table.find_elements_by_css_selector('a')[media_index]
                    media_title = media_elem.text
                    #if the news org hasn't already been saved (could happen if the driver had an error and had to restart),
                    #go to the news org's page and pull its classifications
                    if(media_title not in mbfc_dict):
                        print(media_title)
                        driver.execute_script("arguments[0].click();", media_elem)
                        time.sleep(1)
                        report_text = []
                        (report, sub_element_types) = self.__get_classification_element(driver)
                        if(report == None): 
                            (report, sub_element_types) = self.__get_classification_element(driver, check_alternative=True)
                        if(report != None):
                            report_text = []
                            for sub_element_type in sub_element_types:
                                for element in report.find_elements_by_css_selector(sub_element_type):
                                    report_text.append(element.text)
                            news_bias_fact_cred_dict = get_bias_fact_cred(report_text, url_bias_types[bias])
                            mbfc_dict[media_title] = news_bias_fact_cred_dict
                        else:
                            #if couldn't find classifications, save its bias and error instead
                            mbfc_error_dict = add_to_error_list(media_title, "couldn't find classifications", mbfc_error_dict)
                            mbfc_dict[media_title] = {'Bias': url_bias_types[bias]}

                        media_url = get_url_from_news_title(media_title)
                        if(media_url == None): 
                            try:
                                source_url = driver.find_element_by_xpath("//p[contains(text(), 'Source:')]")
                                media_url = source_url.find_element_by_css_selector('a').text
                                media_url = clean_url(media_url)
                            except:
                                mbfc_error_dict = add_to_error_list(media_title, "couldn't find domain URL", mbfc_error_dict)
                        if(media_url != None):
                            mbfc_dict[media_title]['URL'] = media_url

                        collected_counter += 1

                        #go back from the news org page to the main bias page
                        driver.back()
                        time.sleep(2)
            except:
                print("Having to restart!")
                print("Total news media to collect: " + str(media_table_len))
                print("Number collected so far: " + str(collected_counter))

        driver.close()
        return (mbfc_dict, mbfc_error_dict)

    def __get_classification_element(self, driver, check_alternative=False):
        prefix = "//p"
        up_level = ""
        sub_element_type = ['span']
        if(check_alternative): 
            prefix = "//span"
            up_level = "/.."
            sub_element_type = ['b', 'strong']
        try:
            return(driver.find_element_by_xpath(prefix + "[contains(text(), 'Bias Rating:')]" + up_level), sub_element_type)
        except:
            try: 
                return(driver.find_element_by_xpath(prefix + "[contains(text(), 'Factual Reporting:')]" + up_level), sub_element_type)
            except:
                return (None, None)

    def __reset_browser(self, url_to_go_to, old_driver=None):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.headless = True
        if(old_driver != None): old_driver.close()
        time.sleep(1)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        #log into ad-free account
        driver.get("https://mediabiasfactcheck.com/login")
        try:
            close_message = driver.find_element_by_xpath("//a[contains(text(), 'Never see this message again')]")
            driver.execute_script("arguments[0].click();", close_message)
            time.sleep(0.1)
        except:
            time.sleep(0.1)
        self.__write_in_text_box(driver, "wpforms-87369-field_0", self.username)
        self.__write_in_text_box(driver, "wpforms-87369-field_1", self.password)
        submit_box = driver.find_element_by_id("wpforms-submit-87369")
        action = ActionChains(driver)
        action.move_to_element(submit_box).perform
        submit_box.click()

        #once logged in, go to the specified URL
        driver.get(url_to_go_to)
        time.sleep(1)
        return driver

    def __write_in_text_box(self, driver, text_box_id, text_to_enter):
        text_box = driver.find_element_by_id(text_box_id)
        action = ActionChains(driver)
        action.move_to_element(text_box).perform()
        text_box.click()
        text_box.clear()
        time.sleep(0.1)
        text_box.click()
        action.send_keys(text_to_enter).perform()
        time.sleep(0.2)
        return

    def __add_missing_data(self, news_classifications_dict, error_dict):
        fr_dict = {'VH': 'VERY HIGH', 'H': 'HIGH', 'MF': 'MOSTLY FACTUAL', 'M': 'MIXED', 'L': 'LOW', 'VL': 'VERY LOW', '': ''}
        cr_dict = {'H': 'HIGH CREDIBILITY', 'M': 'MEDIUM CREDIBILITY', 'L': 'LOW CREDIBILITY', '': ''}
        for news_title in error_dict:
            for error_str in error_dict[news_title]:
                if('classifications' in error_str):
                    print('\nNeed info for: ' + news_title + '   with bias rating: ' + news_classifications_dict[news_title]['Bias'])
                    factual_reporting = input('Factual Reporting (VH, H, MF, M, L, VL):')
                    while(factual_reporting not in fr_dict):
                        factual_reporting = input('Please enter a valid factual reporting (VH, H, MF, M, L, VL):')
                    news_classifications_dict[news_title]['Factual'] = fr_dict[factual_reporting]
                    credibility_rating = input('MBFC Credibility Rating (H, M, L, or blank if no rating):')
                    while(credibility_rating not in cr_dict):
                        credibility_rating = input('Please enter a valid MBFC Credibility Rating (H, M, L, or blank if no rating):')
                    news_classifications_dict[news_title]['Credibility'] = (cr_dict[credibility_rating])
                else:
                    print("\nNeed website url for: " + news_title)
                    url_to_use = input('URL to use: ')
                    while(len(url_to_use) == 0):
                        url_to_use = input('URL to use: ')
                    url_to_use = clean_url(url_to_use)
                    news_classifications_dict[news_title]['URL'] = url_to_use
        return(news_classifications_dict)

    def __output_classifications(self, news_classifications_dict, output_file):
        output_data = [['News Title', 'Domain', 'Bias', 'Factual Rating', 'Credibility Rating']]
        for news, news_data in news_classifications_dict.items():
            this_news_output = [news, '', '', '', '']
            if('URL' in news_data): this_news_output[1] = news_data['URL']
            if('Bias' in news_data): this_news_output[2] = news_data['Bias']
            if('Factual' in news_data): this_news_output[3] = news_data['Factual']
            if('Credibility' in news_data): this_news_output[4] = news_data['Credibility']
            output_data.append(this_news_output)
        file = open(output_file, 'w', newline ='')
        with file:    
            write = csv.writer(file)
            write.writerows(output_data)


    def __collect_urls_from_webpage(self, url_to_go_to, manual_corrections):
        url_dict = {}
        collected_counter = 0
        media_table_len = 100
        driver = None
        #go through each news org in the list and save its title and domain url
        while(len(url_dict) < media_table_len): 
            try:
                driver = self.__reset_browser(url_to_go_to, driver)
                media_table = driver.find_element_by_id('mbfc-table')
                media_table_len = len(media_table.find_elements_by_css_selector('a'))
                for media_index in range(media_table_len):
                    media_table = driver.find_element_by_id('mbfc-table')
                    media_elem = media_table.find_elements_by_css_selector('a')[media_index]
                    media_title = media_elem.text
                    if(media_title not in url_dict):
                        print(media_title)
                        media_url = get_url_from_news_title(media_title)
                        if (media_url == None):
                            try:
                                driver.execute_script("arguments[0].click();", media_elem)
                                time.sleep(1)
                                try: source_url = driver.find_element_by_xpath("//p[contains(text(), 'Source:')]")
                                except: source_url = driver.find_element_by_xpath("//span[contains(text(), 'Source:')]")
                                media_url = source_url.find_element_by_css_selector('a').text
                                media_url = clean_url(media_url)
                            except:
                                if(manual_corrections):
                                    print("\nNeed website url for: " + media_title)
                                    media_url = input('URL to use: ')
                                    media_url = clean_url(media_url)
                                else:
                                    media_url = ""
                            #go back from the news org page to the main page
                            driver.back()
                            time.sleep(1)
                        if(media_url != None):
                            url_dict[media_title] = media_url
            except:
                print("Restarting driver")
        driver.close()
        return url_dict

    def __output_urls_to_csv(self, url_dict, output_file, type_title):
        output_data = [['News Title', 'Domain', type_title]]
        for media_title, domain_url in url_dict.items():
            output_data.append([media_title, domain_url, 'True'])
        file = open(output_file, 'w', newline ='')
        with file:    
            write = csv.writer(file)
            write.writerows(output_data)
