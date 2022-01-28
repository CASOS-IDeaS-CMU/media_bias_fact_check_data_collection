# Media Bias Fact Check Data Collection
Functions for collecting data such as media bias and factual ratings from Media Bias Fact Check website.

## Overview
This code provides functions for scraping and standardizing media ratings and data from the 
Media Bias Fact Check website. Media Bias Fact Check provides bias, factual accuracy, 
and credibility ratings for over 2,000 news and political organizations (https://mediabiasfactcheck.com/about/).

This code was tested with Python 3.7. Required dependencies are selenium (3.141) and webdriver-manager (3.3).

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
collector.biased_based_collection(bias, outputfile='./bias_output.csv', manual_corrections=False)
```
bias: 'left', 'left-center', 'center', 'right-center', or 'right' <br />
Note that center is also referred to as least biased on the Media Bias Fact Check website.

### 2. All-Bias Collection
To collect all news organizations from all 5 of the bias categories, along with their domains and 
their bias, factual, and conspiracy ratings:
```
collector.all_biases_collection(outputfile='./all_bias_output.csv', manual_corrections=False)
```
### 3. Conspiracy/Pseudoscience Collection
To collect the Conspiracy/Pseudoscience websites listed (https://mediabiasfactcheck.com/conspiracy/):
```
collector.conspiracy_pseudoscience_collection(outputfile='./conspiracy_output.csv', manual_corrections=False)
```
### 4. Questionable/Fake Collection
To collect the Questionable/Fake news sources listed (https://mediabiasfactcheck.com/fake-news/):
```
collector.questionable_sources_collection(outputfile='./questionable_output.csv', manual_corrections=False)
```
