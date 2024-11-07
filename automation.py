from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from pathlib import Path
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
import random
from dotenv import load_dotenv 
import os
from typing import List, Union
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriver
import shutil
from logger import Logger
from selenium.webdriver.remote.webelement import WebElement
import logging
from automation_helpers import AutomationHelpers as Ah

applog = Logger(level=logging.ERROR)

class SeleniumScraper:

    @staticmethod
    def setup_driver(headless = False, detached = False, driverPath = None) -> webdriver.Chrome:
        """
        Sets up the ChromeDriver which can be ran either headless or using your default chrome account

        Input Parameters
        ----
            headless
                a boolean stating whether the ChromeDriver should be headless or not (WIP)
        Return Value
        ----
            returns a ChromeDriver object
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument('--start-maximized')


        if detached:
            options.add_experimental_option('detach', True)

        if headless:
            options.add_argument('--headless=new')

        user_data_dir = str(Path.home()) + r'\AppData\Local\Google\Chrome\User Data' 
        options.add_argument('--user-data-dir=' + user_data_dir)
        options.add_argument('--profile-directory=Profile 2')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        
        if driverPath is None:
            driver = webdriver.Chrome(options=options)
            return driver
        else:
            service = Service(driverPath)
            driver = webdriver.Chrome(options=options, service=service)
            return driver

    def __init__(self, headless = False, detached = False, driverPath = None, raise_if_elements_missing = False):
        self.raise_if_elements_missing = raise_if_elements_missing
        try:
            self.driver = SeleniumScraper.setup_driver(headless=headless, detached=detached, driverPath=driverPath)
        except Exception as e:
            print(e)
            applog.error("Failed to setup driver with account: Make sure all chrome windows are closed")
            self.driver = webdriver.Chrome()
    
    def wait_until_elem_present(self, selection : str, mode: str = By.CSS_SELECTOR) -> WebElement | None:
        """
        A function that waits until an element is present and should be used as a buffer between actions so that code is not executed before
        an element is present

        Input Parameters
        -----
            mode
                the attribute that can be accessed by selenium which can be XPATH, ID, Class, etc
            selection
                the specific element on the webpage that can be accessed
        Return Value
        -----
            returns bool
        """
        try:
            element_present = EC.presence_of_element_located(
                (mode, selection)
            )
            WebDriverWait(self.driver, 12).until(element_present)
            element = self.driver.find_element(mode, selection)
            return self.raiseIfElementMissing(element, selection)
        except:
            return None
    
    def raiseIfElementMissing(self, element: WebElement, selector: str):
        if self.raise_if_elements_missing and element is None:
            raise Exception(f"Element with selector {selector} is missing")
        if not self.raise_if_elements_missing and element is None:
            return None
        else:
            return element
    
    def find_by_id(self, id: str):
        element = self.driver.find_element(By.ID, id)
        return self.raiseIfElementMissing(element, id)

    def find_by_x_path(self, x_path: str):
        element = self.driver.find_element(By.XPATH, x_path)
        return self.raiseIfElementMissing(element, x_path)
    
    def query_selector(self, selector: str):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        return self.raiseIfElementMissing(element, selector)

    def query_selector_all(self, selector: str):
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        return [self.raiseIfElementMissing(element, selector) for element in elements]
    
    def find_element_by_text_content(self, text: str):
        element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        return self.raiseIfElementMissing(element, text)
    
    @staticmethod
    def upload_file(filepath: str, fileInput: WebElement):
        fileInput.send_keys(filepath)
    
    @staticmethod
    def random_wait(num_seconds = 1):
        random_seconds = random.uniform(0.5, num_seconds)
        time.sleep(random_seconds)


def upload_cover(filename: str, cover_input: WebElement):
    cover_path = f"covers/{filename}"
    full_path = os.path.abspath(cover_path)
    SeleniumScraper.upload_file(full_path, cover_input)

def upload_thumbnail(filename: str, thumbnail_input: WebElement):
    thumbnail_path = f"thumbnails/{filename}"
    full_path = os.path.abspath(thumbnail_path)
    SeleniumScraper.upload_file(full_path, thumbnail_input)

def upload_sheet_music(filename: str, pdf_input: WebElement):
    pdf_path = f"sheetmusic/{filename}"
    full_path = os.path.abspath(pdf_path)
    SeleniumScraper.upload_file(full_path, pdf_input)

def main_loop():
    scraper.driver.get("https://app.gumroad.com/products/new")

    # 2. fill out product name
    # TODO: use AI here to generate a random product name
    product_name_input = scraper.wait_until_elem_present("input[placeholder='Name of product']")
    SeleniumScraper.random_wait()
    product_name_input.send_keys("Test Product")

    # 3. fill out product price
    price_input = scraper.wait_until_elem_present("input[placeholder='Price your product']")
    price_input.send_keys("2.99")

    # 4. fill out product description
    SeleniumScraper.random_wait()
    submit_button = scraper.wait_until_elem_present("button[type='submit']")
    submit_button.click()
    time.sleep(3)

    # 5. fill out product description
    # TODO:: use AI to generate a random description
    description_area = scraper.wait_until_elem_present(".rich-text").find_element(By.CSS_SELECTOR, "div")
    description_area.send_keys("This is my description")

    # 6. fill out product slug
    # TODO:: use AI to generate a random description
    SeleniumScraper.random_wait()
    slug_input = scraper.query_selector("main > form > section:nth-child(1) > fieldset:nth-child(3) > div > input")
    slug_input.send_keys(f"test-product-{Ah.create_random_uuid()}")
    SeleniumScraper.random_wait()


    # 7. upload cover and thumbnail ! holy shit it works
    prebutton = scraper.find_element_by_text_content(' Upload images or videos')
    prebutton.click()
    time.sleep(1)

    cover_file_input = scraper.query_selector("main > form > section:nth-child(2) > div > div > div > label > input[type=file]")
    thumbnail_file_input = scraper.query_selector("main > form > section:nth-child(3) > div.image-uploader > div.placeholder > label > input[type=file]")

    upload_cover("Avengers_Theme_-_Infinity_War_Arrangement__Piano_Tutorial.jpg", cover_file_input)
    time.sleep(2)
    upload_thumbnail("Avengers_Theme_-_Infinity_War_Arrangement__Piano_Tutorial.jpg", thumbnail_file_input)
    time.sleep(2)

    # 8. go to next section
    next_button = scraper.find_element_by_text_content("Save and continue")
    next_button.click()
    time.sleep(2)

    # 9. add some words of encouragement
    sell_textarea = scraper.query_selector("div.has-sidebar > div.rich-text > div[contenteditable='true']")
    sell_textarea.send_keys("""
        Thanks for buying this sheet music! I hope you enjoy playing it.
        If you have any questions or concerns, feel free to reach out to me.
        I try to make the sheet music at competitive pricing, far cheaper than anybody else!
    """)
    SeleniumScraper.random_wait()

    # 10. add pdf file of sheet music
    pdf_input = scraper.query_selector("div.rich-text-editor-toolbar > details:nth-child(10) > div > div > label > input[type=file]")
    upload_sheet_music("Avengers_Theme_-_Infinity_War_Arrangement__Piano_Tutorial.pdf", pdf_input)
    time.sleep(2)

    # 11. save changes
    save_button = scraper.find_element_by_text_content("Save changes")
    save_button.click()
    time.sleep(1)

    publish_button = scraper.find_element_by_text_content("Publish and continue")
    publish_button.click()
    time.sleep(1)

    # 12. put only in sheet music section
    switch = scraper.wait_until_elem_present("main > form > section:nth-child(2) > fieldset > label:nth-child(1) > input[type=checkbox]")
    switch.click()
    time.sleep(3)

    # 13. add tags
    tags = ["sheet music", "piano sheet music", "piano solo", "piano sheet", "piano tutorial"]
    [category_input, tags_input] = scraper.query_selector_all("input[role='combobox']")
    # tags_input = scraper.find_element_by_text_content("Begin typing to add a tag...") \
    #     .find_element(By.CSS_SELECTOR, "input")
    for tag in tags:
        tags_input.send_keys(tag)
        SeleniumScraper.random_wait()
        # time.sleep(2)
        scraper.wait_until_elem_present("datalist > div")
        scraper.driver.execute_script("""
            const datalist = document.querySelector("datalist");
            const first_element = datalist.querySelector("div");
            first_element.click();
        """)
        time.sleep(1)

    # 14. click gumroad discover
    SeleniumScraper.random_wait()
    discover_switch = scraper.query_selector("main > form > section:nth-child(3) > fieldset:nth-child(5) > details > summary > label > input[type=checkbox]")
    discover_switch.click()
    SeleniumScraper.random_wait()

    discover_fee_input = scraper.wait_until_elem_present("input[min='30']")
    discover_fee_input.clear()
    discover_fee_input.send_keys("50")

    # 15. get categories
    SeleniumScraper.random_wait()
    category_input.click()
    category_input.send_keys("Music & Sound Design > Sound Design > Sheet Music")
    SeleniumScraper.random_wait()
    scraper.wait_until_elem_present("datalist > div")
    scraper.driver.execute_script("""
        const datalist = document.querySelector("datalist");
        const first_element = datalist.querySelector("div");
        first_element.click();
    """)
    time.sleep(1)

    save_button = scraper.find_element_by_text_content("Save changes")
    save_button.click()
    time.sleep(1)

if __name__ == "__main__":
    scraper = SeleniumScraper(detached=True, raise_if_elements_missing=True)
    time.sleep(2)
    


    