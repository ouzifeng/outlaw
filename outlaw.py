import requests
from bs4 import BeautifulSoup
import json
import tabulate
import re
import xml.etree.ElementTree as ET
import time
import csv

def is_variable_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    variant_div = soup.find('div', class_='product-variants-item row')
    return bool(variant_div)

def fetch_variation_details(url, variation_value):
    ajax_url = "https://www.outlawpro.co.uk/index.php"
    params = {
        'controller': 'product',
        'id_product': url.split('/')[-1].split('-')[0],
        'group[2]': variation_value,
        'ajax': '1',
        'action': 'refresh'
    }
    try:
        response = requests.post(ajax_url, data=params)
        if response.headers.get('Content-Type') == 'application/json':
            data = response.json()

            product_details_html = data.get("product_details", "")
            sku_match = re.search(r'itemprop="sku">([^<]+)<', product_details_html)
            sku = sku_match.group(1) if sku_match else "SKU not found"

            product_prices_html = data.get("product_prices", "")
            price_match = re.search(r'itemprop="price" content="([0-9.]+)"', product_prices_html)
            price = price_match.group(1) if price_match else "Price not found"

            # Check stock status
            stock_status = "In Stock"
            if "product-availability product-unavailable" in product_prices_html:
                stock_status = "Out of Stock"

            return price, sku, stock_status
        else:
            return "Non-JSON response", "SKU not found", "Out of Stock"
    except json.JSONDecodeError as e:
        return f"JSON decoding error: {e}", "SKU not found", "Out of Stock"
    except Exception as e:
        return f"Error: {e}", "SKU not found", "Out of Stock"



def scrape_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    h1_tag = soup.find('h1', itemprop='name')
    if not h1_tag:
        return None  # Skip this URL as it's not a product page

    name = h1_tag.text.strip()
    default_sku = soup.find('span', itemprop='sku').text.strip() if soup.find('span', itemprop='sku') else "SKU not found"

    product_info = {
        'Name': name,
        'Variations': []
    }

    if is_variable_product(url):
        select_element = soup.find('select', {'class': 'custom-select'})
        if select_element:
            options = select_element.find_all('option')
            for option in options:
                value = option['value']
                variation_detail = option.text.strip()
                returned_values = fetch_variation_details(url, value)

                # Handling different number of return values
                if len(returned_values) == 2:
                    variation_price, variation_sku = returned_values
                    variation_stock_status = "Check manually"  # Default text if stock status not returned
                else:
                    variation_price, variation_sku, variation_stock_status = returned_values

                product_info['Variations'].append({
                    'Variation Info': variation_detail,
                    'SKU': variation_sku,
                    'Price': variation_price,
                    'Stock Status': variation_stock_status
                })
    else:
        try:
            price = soup.find('span', itemprop='price').text.strip()
        except:
            price = "Price not found"
        stock_status = "In Stock"
        if soup.find('span', class_='product-availability product-unavailable alert alert-warning'):
            stock_status = "Out of Stock"
        product_info['Variations'].append({
            'Variation Info': '',
            'SKU': default_sku,
            'Price': price,
            'Stock Status': stock_status
        })

    return product_info




def save_to_csv(data, filename='outlaw_product_data.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Variation Info", "SKU", "Price", "Stock Status"])
        writer.writerows(data)


def main():
    start_time = time.time()

    # Read product URLs from the CSV file
    with open('product_urls.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        product_urls = [row[0] for row in reader]

    all_product_variations = []  # List to hold all product variations

    for i, url in enumerate(product_urls, start=1):
        print(f"Processing {i}/{len(product_urls)}: {url}")  # Feedback print statement
        product_details = scrape_product_info(url)
        if product_details:
            for variation in product_details['Variations']:
                all_product_variations.append([
                    product_details['Name'],
                    variation['Variation Info'],
                    variation['SKU'],
                    variation['Price'],
                    variation['Stock Status']
                ])

        # Optional: Add a delay between requests
        # time.sleep(2)

    save_to_csv(all_product_variations)

    end_time = time.time()  # End time
    total_time = (end_time - start_time) / 60  # Total execution time in minutes
    print(f"Total execution time: {total_time:.2f} minutes")

if __name__ == "__main__":
    main()