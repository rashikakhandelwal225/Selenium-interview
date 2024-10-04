from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://www.amazon.in/')
elem = driver.find_element(By.ID, "twotabsearchtextbox")
elem.clear()
elem.send_keys("Smartphone")
elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

def scraper(list1):
    product_data = []
    for product_url in list1:     #list1 has links of all the products
        name = product_url.find_element(By.ID, 'productTitle')
        price = product_url.find_element(By.CLASS_NAME, 'a-price-whole')
        url = product_url
        user_rating = product_url.find_element(By.CLASS_NAME, 'a-size-base a-color-base')
        ram_capacity = product_url.find_element(By.CLASS_NAME, 'a-size-base po-break-word')
        screen_size = product_url.find_element(By.CLASS_NAME, 'a-size-base po-break-word')

        product_data.append([name, price, url, user_rating, ram_capacity, screen_size])
    return product_data


list_of_all_products = []

for page in range(0, 4):
    list1 = []  # list of links of all the product of a page
    for i in driver.find_elements(By.CSS_SELECTOR, "a"):
        href_value = i.get_attribute("href")
        list1.append(href_value)
    print(list1)
    product_data=scraper(list1)     #calling scraper method , fetching each product details
    list_of_all_products.append(product_data)      #each page products are stored in this curated list
    try:
        next_page_link = driver.find_element(By.CLASS_NAME, "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")

        if next_page_link:
            next_page_link.click()
    except NoSuchElementException:
        print("No more pages available")
        break

driver.quit()


df = pd.DataFrame(list_of_all_products, columns=["Name", "Price", "URL", "Rating", "RAM", "Screen Size"])
df.to_excel("smartphones.xlsx", index=False)
