from selenium.webdriver.remote.webelement import WebElement
import uuid


class AutomationHelpers:
    @staticmethod
    def get_new_product_button(scraper):
        new_product_button = scraper.wait_until_elem_present("a[href='/products/new']")
        return AutomationHelpers.raiseIfNotElementExists(new_product_button, "a[href='/products/new']")

    @staticmethod
    def get_product_name_input(scraper):
        element = scraper.wait_until_elem_present("input[placeholder='Name of product']")
        return AutomationHelpers.raiseIfNotElementExists(element, "input[placeholder='Name of product']")
    
    @staticmethod
    def get_element(scraper, selector):
        element = scraper.wait_until_elem_present(selector)
        return AutomationHelpers.raiseIfNotElementExists(element, selector)
    
    @staticmethod
    def raiseIfNotElementExists(element, selection) -> WebElement:
        if not element:
            raise Exception("element with selector {selection} not found")
        return element
    
    @staticmethod
    def create_random_uuid():
        return str(uuid.uuid4())[:10]