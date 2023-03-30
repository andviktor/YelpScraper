# import modules
import seleniumwire.undetected_chromedriver.v2 as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import time, csv
from sys import argv, exit

# options
txt_output_links = './csv_output/links.txt'
csv_output_companies = './csv_output/companies.csv'
first_list_page_url = 'http://www.yelp.com/search?find_desc=lawyer&find_loc=San+Francisco%2C+CA'

proxy = {
        'user': 'andviktor',
        'password': 'YqUDR2c5kZ',
        'host': '185.228.195.247',
        'port': '59100'
    }

# function - setup webdriver
def setup_webdriver(proxy):

    seleniumwire_options = {
        'proxy': {
            'https': 'https://'+proxy['user']+':'+proxy['password']+'@'+proxy['host']+':'+proxy['port']
        },
        'page_load_strategy': 'eager'
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_experimental_option(
        'prefs', {
            'profile.managed_default_content_settings.images': 2,
            'javascript.enabled' : False,
            'disable-extensions' : True,
            }
    )
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    
    #chrome_options.add_argument('--headless')

    return(webdriver.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options, desired_capabilities=caps))

# function - alert no arguments
def alert_no_argv(argv):
    if len(argv) == 1:
        print('Arguments:')
        print('getlist - get companies profile links')
        print('getcompanies - get companies data')
        exit()

# function - check exists by xpath
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

# function - get xpath element
def get_element(driver, xpath):
    try:
        return(driver.find_element(By.XPATH, xpath))
    except:
        return(False)

# function - get company page data
def get_company_page_data(driver, company_page_url):
    driver.get(company_page_url)
    time.sleep(3)

    company_data = []

    if check_exists_by_xpath(driver, '//h1[contains(@class,"css-1se8maq")]'):
        company_data.append(get_element(driver, '//h1[contains(@class,"css-1se8maq")]').text)
    else:
        company_data.append('')
    
    if check_exists_by_xpath(driver, '//div[contains(@class,"css-1vhakgw")][1]'):
        company_data.append(get_element(driver, '//div[contains(@class,"css-1vhakgw")][1]').get_attribute('href'))
    else:
        company_data.append('')
    
    if check_exists_by_xpath(driver, '//div[contains(@class,"css-1vhakgw")][2]'):
        company_data.append(get_element(driver, '//div[contains(@class,"css-1vhakgw")][2]').text)
    else:
        company_data.append('')

    if check_exists_by_xpath(driver, '//address'):
        company_data.append(get_element(driver, '//address').text.replace('\n', ' '))
    else:
        company_data.append('')
    
    print('Collected: ' + company_data[0])
    return(company_data)

# function - get list page data
def get_list_page_data(driver, list_page_url):
    driver.get(list_page_url)
    time.sleep(5)

    if check_exists_by_xpath(driver, '//a[contains(@class,"next-link")]'):
        next_page_link = driver.find_element(By.XPATH, '//a[contains(@class,"next-link")]').get_attribute('href')
    else:
        next_page_link = None

    list_data = {
        'next_page_link': next_page_link,
        'companies_links': driver.find_elements(By.XPATH, '//h3[@class="css-1agk4wl"]/span/a')
    }
    return(list_data)

# function - write list to txt file
def write_txt(filename, data):
    try:
        with open(filename, 'a') as filehandle:  
            for listitem in data:
                filehandle.write('%s\n' % listitem)
        return True
    except:
        return False
    
# function - read list from txt file
def read_txt(filename):
    output = []
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            output.append(line)
    return output
    
# function - write dict to csv file
def write_csv(filename, data):
    try:
        with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data)
        return True
    except:
        return False

# main function
def main():

    # check arguments
    alert_no_argv(argv)

    # initialization
    driver = setup_webdriver(proxy)
    next_list_page_url = first_list_page_url

    # get companies links
    if 'getlist' in argv:
        try:
            list_count = 1
            while True:
                companies_links = []

                list_page_data = get_list_page_data(driver, next_list_page_url)

                for link in list_page_data['companies_links']:
                    companies_links.append(link.get_attribute('href'))

                write_txt(txt_output_links, companies_links)

                print(str(list_count) + '#: list downloaded: ' + next_list_page_url)
                list_count += 1

                if list_page_data['next_page_link'] != None:
                    next_list_page_url = list_page_data['next_page_link']
                else:
                    break
        
        except Exception as ex:
            print(ex)

    # get all companies data
    if 'getcompanies' in argv:
        try:
            for company_link in read_txt(txt_output_links):
                company_page_data = get_company_page_data(driver, company_link)

                write_csv(csv_output_companies, company_page_data)

        except Exception as ex:
            print(ex)


    # close webdriver
    print('Completed.')
    driver.close()
    driver.quit()        

if __name__ == '__main__':
    main()