from django.http import JsonResponse
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from django.conf import settings
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from .models import PhoneNumbers


class PhoneNumScraper():

    def __init__(self):
        options = ChromeOptions()
        
        if not settings.FIRST_TIME_SETUP:
            options.add_argument("--headless=new")
        options.page_load_strategy = 'eager'
        options.add_argument(f"user-data-dir=/home/amirsameh/Junkyard")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1024, 768)


    def setup(self, search_city, search_param):
        search_url = settings.URL + "/s/" + search_city + f"?q={search_param}"
        self.driver.get(search_url)


    # Scrolling divar page
    def scroll_to_end(self):

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # while True:

        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #     time.sleep(2)

        #     new_height = self.driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break

        #     last_height = new_height
        time.sleep(0.5)


    def get_urls(self, search_city, search_param, search_count):
        
        self.setup(search_city, search_param)

        hrefs = []
        print(search_count)
        count = 0

        while count < search_count :

            poster_elements = self.driver.find_elements(By.CLASS_NAME, "post-list__widget-col-c1444 > a")
            time.sleep(1)
            for i in poster_elements:

                href_value = i.get_attribute("href")
                print(href_value)
                hrefs.append(href_value)
                count += 1
                if count == search_count:
                    break

            self.scroll_to_end()


        return hrefs
    


    def crawl_nums(self, hrefs):
            
            phone_numbers = []
            button_fails = 0
            num_fails = 0

            for url in hrefs:
                # Open a new tab or window
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[-1])

                # Navigate to the URL
                self.driver.get(url)

                # Wait for the page to load (optional)
                time.sleep(0.5)
                try:
                    contact_button = self.driver.find_element(By.CSS_SELECTOR, "button.kt-button.kt-button--primary.post-actions__get-contact")
                    contact_button.click()
                    time.sleep(1)
                    try:
                        phone_link_xpath = "//div[@class='kt-base-row__end kt-unexpandable-row__value-box']/a[@class='kt-unexpandable-row__action kt-text-truncate' and starts-with(@href, 'tel:')]"
                        phone_link_element = self.driver.find_element(By.XPATH, phone_link_xpath)
                        href_value = phone_link_element.get_attribute("href")
                        phone_number = href_value.split(":")[-1]
                        phone_numbers.append(phone_number)
                    except:
                        print("failed to crawl numbers")
                        num_fails += 1
                        pass
                except:
                    print("failed to click on button")
                    button_fails += 1
                    pass

                # Close the tab or window
                self.driver.close()

                # Switch back to the main window
                self.driver.switch_to.window(self.driver.window_handles[0])

            print(phone_numbers)
            return phone_numbers, button_fails, num_fails
    

    def save_nums(self, phone_numbres, search_city, search_param):

        for phone_number in phone_numbres:
            num_obj = PhoneNumbers(
                phone_number = phone_number,
                city=search_city,
                search_param=search_param
            )
            num_obj.save()
