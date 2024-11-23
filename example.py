from rs_scraper.scraper import RSWebScraper
from time import sleep
# Setup scraper
scraper = RSWebScraper(headless=False, regions_file="data/regions.json")

try:
    # Select the geographic section for Austria
    scraper.select_region("austria")
    # Perform a search for "Arduino"
    scraper.perform_search_with_button("Arduino")
    sleep(1)
    scraper.click_100_results_per_page()
    sleep(1)
    # Extract product information
    product_data = scraper.extract_product_info()
    
    scraper.go_to_product_url(product_data[0]['URL'])
    print(scraper.extract_product_details())




finally:
    # Close the browser
    scraper.close()
