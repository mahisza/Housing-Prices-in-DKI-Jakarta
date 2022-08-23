from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from bs4 import BeautifulSoup
import time

#Start the Webdriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def get_url():
    url = 'https://www.lamudi.co.id/jakarta/house/buy/?page={}'
    return url

def extract_record(item):
    atag = item.a
    
    #Get the URL of each listings
    url = atag.get('href')
    
    #Extract the price, building_area, and land_area for each listing, return '' if not found.
    try:
        price = item.get('data-price')
        building_area = item.get('data-building_size')
        land_area = item.get('data-land_size')
    except AttributeError:
        price = ''
        building_area = ''
        land_area = ''
    
    result = (url, price, building_area, land_area)
    return result

#Main Program
def main():    
    url = get_url()
    records = []
    driver.get(url)
    
    #Loop 101 pages of results and put the listings to records
    for page in range(101):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, "lxml")
        results = soup.find_all('div', {'class': 'ListingCell-AllInfo ListingUnit'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    
    #write the listings into a csv file
    with open('results_houses.csv', 'w', newline = '', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Url', 'Price', 'Building Area', 'Land Area'])
        writer.writerows(records)
    
    f.close()

