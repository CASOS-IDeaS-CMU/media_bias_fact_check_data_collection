# Media Bias Fact Check Data Collection
Functions for collecting data such as media bias and factual ratings from Media Bias Fact Check website.

## Overview
This code provides functions for scraping and standardizing media ratings and data from the 
Media Bias Fact Check website. Media Bias Fact Check provides bias, factual accuracy, 
and credibility ratings for over 2,000 news and political organizations (https://mediabiasfactcheck.com/about/).

This code was tested with Python 3.7. Required dependencies are selenium (3.141) and webdriver-manager (3.3).

This tool was created by Isabel Murdock on 1/25/2022. Usage of this tool must comply with the Media Bias/Fact Check website's terms and conditions: https://mediabiasfactcheck.com/terms-and-conditions/.

## Initializing
To use this code, you must have an Ad-Free account 
with Media Bias Fact Check (https://mediabiasfactcheck.com/membership-account/membership-levels/).
```
from MediaBiasFactCheckCollection import MediaBiasFactCheckCollection
collector = MediaBiasFactCheckCollection("username", "password")
```
## Data Collection Functions
While these functions attempt to handle various inconsistencies in the formats of different pages on the 
Media Bias Fact Check website, there are a handful of news organizations that fail to have their
data automatically collected with these functions. Due to this, the user can set the manual_corrections
field to be False if they want to skip over the missing data or set the field to True to be prompted
to enter the missing data through prompts. 

### 1. Bias-Based Collection
To collect all news organizations listed under a particular bias page on Media Bias Fact Check, along 
with their domains and their bias, factual, and conspiracy ratings:
```
collector.biased_based_collection(bias, output_file='./bias_output.csv', manual_corrections=False)
```
**Inputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp; bias: 'left', 'left-center', 'center', 'right-center', or 'right' <br />
    &nbsp;&nbsp;&nbsp;&nbsp;output_file: output directory/filename to write the data to <br />
    &nbsp;&nbsp;&nbsp;&nbsp;manual_corrections: True to be prompted to add data by hand that couldn't be collected automatically, False to skip over missing data <br />
**Outputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp; CSV file with the news organizations' titles, domains, bias, factual rating, and credibility rating <br />
Note that center is also referred to as least biased on the Media Bias Fact Check website.

### 2. All-Bias Collection
To collect all news organizations from all 5 of the bias categories, along with their domains and 
their bias, factual, and conspiracy ratings:
```
collector.all_biases_collection(output_file='./all_bias_output.csv', manual_corrections=False)
```
**Inputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp;output_file: output directory/filename to write the data to <br />
    &nbsp;&nbsp;&nbsp;&nbsp;manual_corrections: True to be prompted to add data by hand that couldn't be collected automatically, False to skip over missing data <br />
**Outputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp; CSV file with the news organizations' titles, domains, bias, factual rating, and credibility rating <br />
Note that center is also referred to as least biased on the Media Bias Fact Check website.

### 3. Conspiracy/Pseudoscience Collection
To collect the Conspiracy/Pseudoscience websites listed on https://mediabiasfactcheck.com/conspiracy/:
```
collector.conspiracy_pseudoscience_collection(output_file='./conspiracy_output.csv', manual_corrections=False)
```
**Inputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp;output_file: output directory/filename to write the data to <br />
    &nbsp;&nbsp;&nbsp;&nbsp;manual_corrections: True to be prompted to add data by hand that couldn't be collected automatically, False to skip over missing data <br />
**Outputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp; CSV file with the news organizations' titles, domains, and conspiracy/pseudoscience classifications<br />

### 4. Questionable/Fake Collection
To collect the Questionable/Fake news sources listed on https://mediabiasfactcheck.com/fake-news/:
```
collector.questionable_sources_collection(output_file='./questionable_output.csv', manual_corrections=False)
```
**Inputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp;output_file: output directory/filename to write the data to <br />
    &nbsp;&nbsp;&nbsp;&nbsp;manual_corrections: True to be prompted to add data by hand that couldn't be collected automatically, False to skip over missing data <br />
**Outputs:** <br />
    &nbsp;&nbsp;&nbsp;&nbsp; CSV file with the news organizations' titles, domains, and questionable/fake classifications<br />
