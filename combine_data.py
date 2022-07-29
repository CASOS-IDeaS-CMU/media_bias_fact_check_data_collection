import json
import csv
import sys


def WriteDataToCSV(data_list, csv_name):
    file = open(csv_name, 'w', newline ='')
    with file:    
        write = csv.writer(file)
        write.writerows(data_list)

input_files = sys.argv[1:]
main_media_dict = {}

for file in input_files:
    with open(file, "r") as csvfile:
        is_header = True
        header_list = []
        filereader = csv.reader(csvfile, delimiter=',')
        for row in filereader:
            if(is_header): 
                header_list = row[1:]
                is_header = False
            else:
                media_title = row[0]
                if(media_title not in main_media_dict):
                    main_media_dict[media_title] = {}
                for index, data_field in enumerate(header_list):
                    if(data_field in main_media_dict[media_title]): assert(main_media_dict[media_title][data_field] == row[index + 1])
                    main_media_dict[media_title][data_field] = row[index + 1]


combined_properties_data = [['News Title', 'Domain', 'Bias', 'Factual Rating', 'Credibility Rating', 'Conspiracy/Pseudoscience', 'Questionable/Fake']]
for media_title in main_media_dict:
    this_domain_data = [media_title, '', '', '', '', '', '']
    this_collected_data = main_media_dict[media_title]
    if('Domain' in this_collected_data): this_domain_data[1] = this_collected_data['Domain']
    if('Bias' in this_collected_data): this_domain_data[2] = this_collected_data['Bias']
    if('Factual Rating' in this_collected_data): this_domain_data[3] = this_collected_data['Factual Rating']
    if('Credibility Rating' in this_collected_data): this_domain_data[4] = this_collected_data['Credibility Rating']
    if('Conspiracy/Pseudoscience' in this_collected_data): this_domain_data[5] = this_collected_data['Conspiracy/Pseudoscience']
    if('Questionable/Fake' in this_collected_data): this_domain_data[6] = this_collected_data['Questionable/Fake']

    combined_properties_data.append(this_domain_data)

WriteDataToCSV(combined_properties_data, 'combined_output.csv')


