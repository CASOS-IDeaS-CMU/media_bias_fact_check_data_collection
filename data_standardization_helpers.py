def clean_url(url):
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    url = url.replace('www.', '')
    if(url[-1] == '/'):
        url = url[:-1]
    return url.lower()

def get_url_from_news_title(news_title):
    if('(' in news_title and ')' in news_title):
        #use rfind in case news title includes abbreviation (example: Agence France-Presse (AFP) (www.afp.com))
        start = news_title.rfind('(')
        end = news_title.rfind(')')
        url_to_use = news_title[start+1: end]
        url_to_use = clean_url(url_to_use)
        #run this check to make sure it is url not just abbreviation or city
        if('.' in url_to_use):
            return url_to_use
    return None

def get_bias_fact_cred(report_list, bias):
    recognized_terms = {'CENTER': 'Bias', 'FAR LEFT': 'Bias', 'LEFT': 'Bias', 'LEFT-CENTER': 'Bias', 'RIGHT-CENTER': 'Bias', 'RIGHT': 'Bias', 'FAR RIGHT': 'Bias',
                    'VERY HIGH': 'Factual', 'HIGH': 'Factual', 'MOSTLY FACTUAL': 'Factual', 'MIXED': 'Factual', 'LOW': 'Factual', 'VERY LOW': 'Factual',
                    'HIGH CREDIBILITY': 'Credibility', 'MEDIUM CREDIBILITY': 'Credibility', 'LOW CREDIBILITY': 'Credibility'}
    mapping_terms = {'LEAST BIASED': 'CENTER', 'FAR-LEFT': 'FAR LEFT', 'LEFT BIASED': 'LEFT'}

    terms_output = {}
    for term in report_list:
        term = term.strip()
        if(term in mapping_terms):
            term = mapping_terms[term]
        if(term in recognized_terms):
            term_type = recognized_terms[term]
            if(term_type in terms_output):
                #if run into instance where have parsed out multiple biases, keep the more specific/extreme bias
                if(terms_output[term_type] == 'LEFT' and term == 'FAR LEFT'):
                    terms_output[term_type] = term
                elif(terms_output[term_type] == 'RIGHT' and term == 'FAR RIGHT'):
                    terms_output[term_type] = term
                elif(terms_output[term_type] == 'FAR RIGHT' and term == 'RIGHT' or terms_output[term_type] == 'FAR LEFT' and term == 'LEFT'):
                    pass
                else:
                    assert(terms_output[term_type] == term)
            else:
                terms_output[term_type] = term
    if('Bias' not in terms_output):
        terms_output['Bias'] = bias
    return terms_output


def get_bias_fact_cred_conspiracy_pseudo(report_list):
    recognized_terms = {'CENTER': 'Bias', 'FAR LEFT': 'Bias', 'LEFT': 'Bias', 'LEFT-CENTER': 'Bias', 'RIGHT-CENTER': 'Bias', 'RIGHT': 'Bias', 'FAR RIGHT': 'Bias',
                    'VERY HIGH': 'Factual', 'HIGH': 'Factual', 'MOSTLY FACTUAL': 'Factual', 'MIXED': 'Factual', 'LOW': 'Factual', 'VERY LOW': 'Factual',
                    'HIGH CREDIBILITY': 'Credibility', 'MEDIUM CREDIBILITY': 'Credibility', 'LOW CREDIBILITY': 'Credibility'}
    mapping_terms = {'LEAST BIASED': 'CENTER', 'FAR-LEFT': 'FAR LEFT', 'LEFT BIASED': 'LEFT', 'RIGHT CONSPIRACY/PSEUDOSCIENCE': 'RIGHT',  'RIGHT-PSUEDOSCIENCE': 'RIGHT',
                    'RIGHT CONSPIRACY- PSEUDOSCIENCE': 'RIGHT', 'EXTREME RIGHT CONSPIRACY': 'FAR RIGHT', 'RIGHT-CONSPIRACY-PSEUDOSCIENCE': 'RIGHT', 'RIGHT CONSPIRACY': 'RIGHT',
                    'LEFT – PSEUDOSCIENCE': 'LEFT', 'EXTREME RIGHT': 'FAR RIGHT', 'RIGHT-CONSPIRACY': 'RIGHT', 'FAR-RIGHT CONSPIRACY-PSEUDOSCIENCE': 'FAR RIGHT', 
                    'RIGHT PSEUDOSCIENCE': 'RIGHT', 'LEFT CONSPIRACY-PSEUDOSCIENCE': 'LEFT', 'LEFT-CONSPIRACY/PSEUDOSCIENCE': 'LEFT', 'RIGHT-CONSPIRACY/PSEUDOSCIENCE': 'RIGHT',
                    'LEFT-PSEUDOSCIENCE': 'LEFT', 'VERY-LOW': 'VERY LOW', 'RIGHT-PSEUDOSCIENCE': 'RIGHT', 'RIGHT – CONSPIRACY': 'RIGHT', 'RIGHT CONSPIRACY – PSEUDOSCIENCE': 'RIGHT',
                    'FAR RIGHT CONSPIRACY-PSEUSDOSCIENCE': 'FAR RIGHT', 'PSEUDOSCIENCE RIGHT BIASED': 'RIGHT', 'LEFT PSEUDOSCIENCE': 'LEFT', 'RIGHT – CONSPIRACY AND PSEUDOSCIENCE': 'RIGHT',
                    'RIGHT CONSPIRACY-PSEUDOSCIENCE': 'RIGHT'}
    terms_output = {}
    for term in report_list:
        term = term.strip()
        if(term in mapping_terms):
            term = mapping_terms[term]
        if(term in recognized_terms):
            term_type = recognized_terms[term]
            if(term_type in terms_output):
                #if run into instance where have parsed out multiple biases\fact ratings, keep the more specific/extreme bias
                if(terms_output[term_type] == 'LEFT' and term == 'FAR LEFT'):
                    terms_output[term_type] = term
                elif(terms_output[term_type] == 'RIGHT' and term == 'FAR RIGHT'):
                    terms_output[term_type] = term
                elif(terms_output[term_type] == 'LOW' and term == 'VERY RIGHT'):
                    terms_output[term_type] = term
                elif(terms_output[term_type] == 'FAR RIGHT' and term == 'RIGHT' or terms_output[term_type] == 'FAR LEFT' and term == 'LEFT'):
                    pass
                elif(terms_output[term_type] == 'VERY LOW' and term == 'LOW'):
                    pass
                else:
                    assert(terms_output[term_type] == term)
            else:
                terms_output[term_type] = term
    return terms_output

def add_to_error_list(news_title, error_str, error_list):
    if(news_title not in error_list):
        error_list[news_title] = []
    error_list[news_title].append(error_str)
    return error_list
