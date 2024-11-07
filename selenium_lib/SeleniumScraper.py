from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from pathlib import Path
import random
from selenium.webdriver.remote.webelement import WebElement
import uuid
from typing import Literal


class SeleniumScraper:
    @staticmethod
    def setup_driver(
        headless = False, 
        detached = False, 
        driverPath = None, 
        profile_dir : Literal["Profile 1"] | Literal["Profile 2"] | None = None
    ) -> webdriver.Chrome:
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

        """ 
        Open selenium already logged in to google account.
        If profile_dir is not specified, it will use your default google profile
        """
        user_data_dir = str(Path.home()) + r'\AppData\Local\Google\Chrome\User Data' 
        options.add_argument('--user-data-dir=' + user_data_dir)
        profile_dir and options.add_argument(f'--profile-directory={profile_dir}')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        
        if driverPath is None:
            driver = webdriver.Chrome(options=options)
            return driver
        else:
            service = Service(driverPath)
            driver = webdriver.Chrome(options=options, service=service)
            return driver

    def __init__(self, 
                 headless = False, 
                 detached = False, 
                 driverPath = None, 
                 raise_if_elements_missing = False, 
                 profile_dir : Literal["Profile 1"] | Literal["Profile 2"] | None = None
                ):
        self.raise_if_elements_missing = raise_if_elements_missing
        try:
            self.driver = SeleniumScraper.setup_driver(
                                    headless=headless, 
                                    detached=detached, 
                                    driverPath=driverPath,
                                    profile_dir=profile_dir
                                )
        except Exception as e:
            print(e)
            print("Failed to setup driver with account: Make sure all chrome windows are closed")
            self.driver = webdriver.Chrome()
    
    def wait_until_elem_present(self, selection : str, mode: str = By.CSS_SELECTOR, timeout = 12) -> WebElement | None:
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
            WebDriverWait(self.driver, timeout).until(element_present)
            element = self.driver.find_element(mode, selection)
            return self.raiseIfElementMissing(element, selection)
        except:
            return None
    
    def wait_until_elem_clickable(self, selection : str, mode: str = By.CSS_SELECTOR, timeout = 12) -> WebElement | None:
        try:
            element_present = EC.element_to_be_clickable(
                (mode, selection)
            )
            WebDriverWait(self.driver, timeout).until(element_present)
            element = self.driver.find_element(mode, selection)
            return self.raiseIfElementMissing(element, selection)
        except:
            return None
    
    def wait_until_elem_visible(self, selection : str, mode: str = By.CSS_SELECTOR, timeout = 12) -> WebElement | None:
        try:
            element_present = EC.visibility_of_element_located(
                (mode, selection)
            )
            WebDriverWait(self.driver, timeout).until(element_present)
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
    
    # region JAVASCRIPT

    def execute_javascript(self, script: str):
        self.driver.execute_script(script)
    
    def get_cookies(self):
        return self.driver.get_cookies()

    def add_cookies(self, cookies: dict[str, str]):
        # When you set a cookie sameSite attribute to Lax, 
        # the cookie will be sent along with the GET request initiated by third party website.
        self.driver.add_cookie({**cookies, 'sameSite': 'Lax'})
    
    def get_cookie(self, name: str):
        return self.driver.get_cookie(name)
    
    @staticmethod
    def upload_file(filepath: str, fileInput: WebElement):
        fileInput.send_keys(filepath)

class SeleniumWebElement:
    def __init__(self, element: WebElement, raise_if_elements_missing = False):
        self.element = element
        self.raise_if_elements_missing = raise_if_elements_missing
    
    def raiseIfElementMissing(self, element: WebElement, selector: str):
        if self.raise_if_elements_missing and element is None:
            raise Exception(f"Element with selector {selector} is missing")
        if not self.raise_if_elements_missing and element is None:
            return None
        else:
            return element
    
    def query_selector(self, selector: str):
        element = self.element.find_element(By.CSS_SELECTOR, selector)
        return self.raiseIfElementMissing(element, selector)
    
    def query_selector_all(self, selector: str):
        elements = self.element.find_elements(By.CSS_SELECTOR, selector)
        return [self.raiseIfElementMissing(element, selector) for element in elements]
    
    def find_element_by_text_content(self, text: str):
        element = self.element.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        return self.raiseIfElementMissing(element, text)
    
    def find_by_x_path(self, x_path: str):
        element = self.element.find_element(By.XPATH, x_path)
        return self.raiseIfElementMissing(element, x_path)
    
    def get_attribute(self, attribute: str):
        return self.element.get_attribute(attribute)
    
class ScraperUtils:
    @staticmethod
    def random_wait(num_seconds = 1):
        random_seconds = random.uniform(0.5, num_seconds)
        time.sleep(random_seconds)
    
    @staticmethod
    def create_random_uuid():
        return str(uuid.uuid4())[:10]

    @staticmethod
    def retry(func : function, max_attempts=3, delay=1):
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay)
