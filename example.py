from rs_scraper.scraper import RSWebScraper

# Setup scraper
scraper = RSWebScraper(headless=False, regions_file="data/regions.json")

try:
    # Select the geographic section for Austria
    scraper.select_region("austria")

    # Perform a search for "Arduino"
    scraper.perform_search_with_button("Arduino")

    scraper.click_100_results_per_page()

    # Extract product information
    product_data = scraper.extract_product_info()
    for product in product_data:
        print(product)

    # Close the browser
    scraper.close()
finally:
    # Close the browser
    scraper.close()
