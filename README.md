
# RSWebScraper

RSWebScraper is a Python-based web scraping utility designed to extract product data from the RS Components website.

## Features
- **Region Selection**: Select your desired geographic region.
- **Search Functionality**: Perform product searches directly on the website.
- **Extract Product Data**: Scrape detailed product information such as title, price, manufacturer, and stock number.
- **Pagination Support**: Configure results to display 100 items per page.
- **Popup Handling**: Automatically handles popups during navigation.

## Setup Instructions
1. Clone this repository.
2. Install the necessary dependencies with:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have the `regions.json` file in the `data/` directory, containing region-specific URLs.
4. Run the scraper using the example script provided.

## Example Usage

```python
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
    # Close the browser in case of errors
    scraper.close()
```

## Current Status
**This project is a work in progress**. Additional features and improvements are planned for future updates.

## Contributions
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

**Note**: This scraper is intended for educational and research purposes only. Please adhere to the terms and conditions of the website being scraped.
