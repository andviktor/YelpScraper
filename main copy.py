# import modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# options
first_list_page_url = 'https://www.yelp.com/search?find_desc=dentists&find_loc=San+Francisco%2C+CA'
next_list_page_url = first_list_page_url

# webdriver
driver = webdriver.Chrome(executable_path = './webdriver/chromedriver.exe')

# function - get xpath element
def get_element(xpath):
    try:
        return(driver.find_element(By.XPATH, xpath))
    except:
        return(False)

# function - get company page data
def get_company_page_data(company_page_url):
    driver.get(company_page_url)
    time.sleep(2)
    title = get_element('//h1[contains(@class,"css-1se8maq")]')
    website = get_element('//div[contains(@class,"css-1vhakgw")][1]')
    phone = get_element('//div[contains(@class,"css-1vhakgw")][2]')
    address = get_element('//address')
    company_data = {
        'title': title.text if title else '',
        'website': website.get_attribute('href') if title else '',
        'phone': phone.text if title else '',
        'address': address.text.replace('\n', ' ') if address else ''
    }
    return(company_data)

# function - get list page data
def get_list_page_data(list_page_url):
    driver.get(list_page_url)
    time.sleep(2)
    list_data = {
        'next_page_link': driver.find_element(By.XPATH, '//a[contains(@class,"next-link")]').get_attribute('href'),
        'companies_links': driver.find_elements(By.XPATH, '//h3[@class="css-1agk4wl"]/span/a')
    }
    return(list_data)

# get all companies links
companies_links = []
i = 1
while True:
    list_page_data = get_list_page_data(next_list_page_url)
    for link in list_page_data['companies_links']:
        companies_links.append(link.get_attribute('href'))
    next_list_page_url = list_page_data['next_page_link']
    i = i + 1
    if not next_list_page_url or i == 2:
        break
# ВНИМАНИЕ!!!! УБРАТЬ УСЛОВИЕ С BREAK!!!!

# get all companies data
companies_data = []
for company_link in companies_links:
    company_page_data = get_company_page_data(company_link)
    companies_data.append(company_page_data)

print(companies_data)