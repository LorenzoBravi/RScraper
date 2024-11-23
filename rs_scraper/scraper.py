import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from functools import wraps
from selenium.common.exceptions import NoSuchElementException

def check_and_handle_popup(popup_selector, action_selector):
    """
    Decorator to check for a popup and perform an action (e.g., click a button) if it's present.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if getattr(func, "_bypass_popup", False):
                return func(self, *args, **kwargs)

            try:
                popup = self.driver.find_element(By.CSS_SELECTOR, popup_selector)
                action_element = self.driver.find_element(By.CSS_SELECTOR, action_selector)
                action_element.click()
            except NoSuchElementException:
                pass

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def apply_popup_handler(popup_selector, action_selector):
    """
    Class decorator to apply popup handling to all methods in a class.
    """
    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, check_and_handle_popup(popup_selector, action_selector)(attr_value))
        return cls
    return class_decorator

def bypass_popup_handling(func):
    """
    Mark a method to bypass popup handling logic.
    """
    func._bypass_popup = True
    return func

@apply_popup_handler(popup_selector="body", action_selector="button#rejectAll")
class RSWebScraper:
    def __init__(self, headless=True, regions_file="regions.json"):
        """
        Initialize the scraper with a WebDriver and load regions from JSON.
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

        with open(regions_file, "r") as file:
            self.regions = json.load(file)

        self.base_url = None

    def select_region(self, region_name):
        """
        Select a geographic region by name.
        """
        if region_name not in self.regions:
            raise ValueError(f"Invalid region name: {region_name}.")
        self.base_url = self.regions[region_name]
        self.open_page(self.base_url)

    def open_page(self, url):
        """
        Open a specified URL.
        """
        self.driver.get(url)

    def perform_search_with_button(self, search_term):
        """
        Enter a search term in the input field and click the search button.
        """
        search_input = self.driver.find_element(By.ID, "searchBarTextInput")
        search_input.clear()
        search_input.send_keys(search_term)
        search_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Search button']")
        search_button.click()

    @bypass_popup_handling
    def click_100_results_per_page(self):
        """
        Click the '100' button to set results per page to 100.
        """
        try:
            button_100 = self.driver.find_element(By.XPATH, "//button[span[text()='100']]")
            button_100.click()
            print("Clicked the '100' button to show 100 results per page.")
        except NoSuchElementException:
            print("'100' button not found.")

    @bypass_popup_handling
    def extract_product_links(self):
        """
        Extract product links from the search results.
        """
        links = []
        products = self.driver.find_elements(By.CSS_SELECTOR, ".product-title a")
        for product in products:
            links.append(product.get_attribute("href"))
        return links

    @bypass_popup_handling
    def extract_product_info(self):
        """
        Extract product information from the current page.
        """
        products = []
        product_tiles = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-tile-item']")
        
        for tile in product_tiles:
            try:
                title = tile.find_element(By.CSS_SELECTOR, "div[data-qa='product-tile-title']").text.strip()
                rs_part_no = tile.find_element(By.CSS_SELECTOR, "div[data-qa='product-tile-partno-value']").text.strip()
                mfr_part_no = tile.find_element(By.CSS_SELECTOR, "div[data-qa='product-tile-mftr-value']").text.strip()
                price = tile.find_element(By.CSS_SELECTOR, "div[data-qa='product-tile-price']").text.strip()
                url = tile.find_element(By.CSS_SELECTOR, "a[data-qa='product-tile-container']").get_attribute("href")
                products.append({
                    "Title": title,
                    "RS Part No.": rs_part_no,
                    "Manufacturer Part No.": mfr_part_no,
                    "Price": price,
                    "URL": url
                })
            except NoSuchElementException:
                continue
        
        return products

    def close(self):
        """
        Close the browser.
        """
        self.driver.quit()
