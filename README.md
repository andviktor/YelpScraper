# Web scraper (Python, Selenium)

The parser is designed to collect data about companies from the website **yelp.com**.

## Input data
|Variable|Example  |
|--|--|
|**first_list_page_url** - url of the first page of search results on yelp.com|first_list_page_url = '**http://www.yelp.com/search?find_desc=lawyer&find_loc=San+Francisco%2C+CA**'|
|**proxy** - proxy settings|proxy  = { 'user': '**proxyuser**', '**password**': '**mypass**', '**host**': '1.1.1.1', '**port**': '80'}|
|**use_proxy** - enable proxy|use_proxy = **True**|


## Output
CSV file (table) with data about companies:

 1. Company name
 2. Website
 3. Phone
 4. Address

## Example
##### On site yelp.com, enter the keyword in the search bar:
![](https://raw.githubusercontent.com/andviktor/yelp-scraping-python/main/readme_images/Step-by-step-1.JPG)

##### Copy the address of the page with the search results:
![](https://raw.githubusercontent.com/andviktor/yelp-scraping-python/main/readme_images/Step-by-step-2.JPG)

##### Paste the copied address as the value of the ***first_list_page_url*** variable and specify proxy settings:
![](https://raw.githubusercontent.com/andviktor/yelp-scraping-python/main/readme_images/Step-by-step-3.JPG)
##### Specify proxy settings:

Start the process of collecting addresses of company profile pages:

```
python main.py getlist
```

##### Start the process of collecting contact information of organizations:
```
python main.py getcompanies
```

## Result of work
The script collects data in 2 files:

 - **/csv_output/links.txt** -- contains links to company profiles.
 - **/csv_output/companies.csv** -- contains the resulting table with the contact details of organizations.

### Collected data example
#### links.txt
![](https://github.com/andviktor/yelp-scraping-python/blob/main/readme_images/Profiles.JPG?raw=true)
#### companies.csv
![](https://github.com/andviktor/yelp-scraping-python/blob/main/readme_images/Result%20data.JPG?raw=true)
## Features

 - Proxy support 
 - Bypass protection against bots 
 - Support for collecting
   data for any keywords
  - Virtual environment included

## Technologies

 - [Selenium](https://www.selenium.dev/)
 - [SeleniumWire](https://pypi.org/project/selenium-wire/)
 - [Undetected Chromedriver v2](https://github.com/ultrafunkamsterdam/undetected-chromedriver)