
# RS Web Scraper

`RSWebScraper` is a Python-based web scraping utility for extracting product information from the RS Components website using Selenium. This tool provides a clean and extensible interface for interacting with the website, managing popups, and scraping product data.

---

## Features

- **Popup Handling**: Automatically handles cookie or other popups using decorators.
- **Dynamic Region Selection**: Allows selecting a specific region to customize scraping for localized content.
- **Search Functionality**: Perform searches directly on the RS Components website.
- **Pagination Control**: Adjust results per page to show up to 100 products.
- **Data Extraction**: Extract detailed product information, including title, part numbers, price, and product links.
- **Headless Mode**: Supports headless browsing for use in automated pipelines.

---

## Installation

### Prerequisites
- Python 3.7+
- Google Chrome
- ChromeDriver compatible with your Chrome version

### Install Dependencies
```bash
pip install selenium
```

---

## Setup

1. **Download the Repository**:
   Clone or download the repository containing the `RSWebScraper` class.

2. **Prepare the `regions.json` File**:
   Create a `regions.json` file containing the base URLs for different regions, for example:
   ```json
   {
       "austria": "https://at.rs-online.com/",
       "germany": "https://de.rs-online.com/"
   }
   ```

---

## Usage

### Example Script

```python
from rs_scraper.scraper import RSWebScraper

# Setup scraper
scraper = RSWebScraper(headless=False, regions_file="data/regions.json")

try:
    # Select the geographic section for Austria
    scraper.select_region("austria")

    # Perform a search for "Arduino"
    scraper.perform_search_with_button("Arduino")

    # Set results per page to 100
    scraper.click_100_results_per_page()

    # Extract product information
    product_data = scraper.extract_product_info()
    for product in product_data:
        print(product)

finally:
    # Close the browser
    scraper.close()
```

---

## Methods

### `select_region(region_name)`
Select the geographic region using a name defined in `regions.json`.

### `perform_search_with_button(search_term)`
Enter a search term and click the search button.

### `click_100_results_per_page()`
Click the button to display 100 results per page.

### `extract_product_links()`
Extract product links from the search results.

### `extract_product_info()`
Extract detailed product data, including:
- Title
- RS Part Number
- Manufacturer Part Number
- Price
- Product URL

### `close()`
Close the browser session.

---

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Disclaimer

This tool is intended for educational and non-commercial use. Ensure compliance with the RS Components website's terms of service when scraping.
