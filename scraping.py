from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import certifi
import requests


cxn_string = 'mongodb+srv://fikrialam099:HyperfoR54@cluster0.sf8bwya.mongodb.net/'
client = MongoClient(cxn_string, tlsCAFile=certifi.where())
db = client.dbsparta_plus_project3

driver = webdriver.Chrome()
driver.get("https://www.google.com")
url = "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"
driver.get(url)
sleep(5)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
sleep(5)

access_token = 'pk.eyJ1IjoiZmFkaGlsbHgiLCJhIjoiY2w4eTloOGM1MDZ0MjN2bGcwY3k5Y3pjeSJ9.X-eiCzScHwEqjoXJUF6AXg'
long = -122.420679
lat = 37.772537

start = 0

seen = {}

for _ in range(5):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    restaurants = soup.select('div[class*="arrange-unit__"]')
    for restaurant in restaurants:
        #mengambil nama restoran
        business_name = restaurant.select_one('div[class*="businessName__"]')
        if not business_name:
            continue
        name = business_name.text.split('.')[-1].strip()

        if name in seen:
            print('already seen!')
            continue

        seen[name] = True

        link = business_name.a['href']
        link = 'https://www.yelp.com/' + link

        #mengambil nama restoran nya
        categories_price_location = restaurant.select_one('div[class*="priceCategory__"]')
        spans = categories_price_location.select('span')
        categories = spans[0].text
        location = spans[-1].text

        geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={access_token}"
        geo_response = requests.get(geo_url)
        geo_json = geo_response.json()
        center = geo_json['features'][0]['center']
        print(name, ',', categories, ',', location, ',', link,',', center)
        doc = {
            'name': name,
            'categories': categories,
            'location': location,
            'link': link,
            'center': center,
        }
        db.restaurants.insert_one(doc)

        start += 10
        driver.get(f'{url}&start={start}')
        sleep(5)
driver.quit()