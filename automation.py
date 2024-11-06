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
            options.add_argument('--no-sandbox')

        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        # options.add_argument(f'--user-agent={user_agent}')
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

    def __init__(self, headless = False, detached = False, driverPath = None):
        self.driver = SeleniumScraper.setup_driver(headless=headless, detached=detached, driverPath=driverPath)
    
    def wait_until_elem_present(self, selection : str, mode: str = By.CSS_SELECTOR) -> bool:
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
            return True
        except:
            return False
    
    def find_by_id(self, id: str):
        return self.driver.find_element(By.ID, id)

    def find_by_x_path(self, x_path: str):
        return self.driver.find_element(By.XPATH, x_path)
    
    def query_selector(self, selector: str):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def query_selector_all(self, selector: str):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)
    
    @staticmethod
    def random_wait(num_seconds = 1):
        random_seconds = random.uniform(0.5, num_seconds)
        time.sleep(random_seconds)


if __name__ == "__main__":
    load_dotenv()
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    # scraper = SeleniumScraper(driverPath="C:\\Users\\Waadl\\Documents\\aadildev\\chromedriver.exe")
    scraper = SeleniumScraper(detached=True)
    # scraper.random_wait()
    # scraper.driver.get("https://app.gumroad.com/products")
    time.sleep(5)
    scraper.driver.quit()


