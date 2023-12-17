import requests
from bs4 import BeautifulSoup
import time
import csv

def get_product_urls(brand_url):
    page = 1
    product_urls = []
    print(f"Scraping brand URL: {brand_url}")

    while True:
        current_url = f"{brand_url}?page={page}"
        print(f"Processing page {page}...")
        response = requests.get(current_url)
        
        if response.url != current_url and page != 1:
            print("End of products reached.")
            page -= 1
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        product_containers = soup.find_all('div', class_='product-container')
        if product_containers:
            for container in product_containers:
                link = container.find('a', href=True)
                if link:
                    product_urls.append(link['href'])

        page += 1
        time.sleep(1)

    return product_urls

brand_urls = [
  "https://www.outlawpro.co.uk/brand/1507-abu-garcia",
  "https://www.outlawpro.co.uk/brand/1364-angling-technics",
  "https://www.outlawpro.co.uk/brand/1349-aqua",
  "https://www.outlawpro.co.uk/brand/1108-avid",
  "https://www.outlawpro.co.uk/brand/1496-baittech",
  "https://www.outlawpro.co.uk/brand/1509-berkley",
  "https://www.outlawpro.co.uk/brand/1109-browning",
  "https://www.outlawpro.co.uk/brand/1117-campingaz",
  "https://www.outlawpro.co.uk/brand/1478-carp-life",
  "https://www.outlawpro.co.uk/brand/1110-carp-spirit",
  "https://www.outlawpro.co.uk/brand/1490-cc-moore",
  "https://www.outlawpro.co.uk/brand/1489-cobb",
  "https://www.outlawpro.co.uk/brand/1103-coleman",
  "https://www.outlawpro.co.uk/brand/1118-cult-tackle",
  "https://www.outlawpro.co.uk/brand/1101-cygnet",
  "https://www.outlawpro.co.uk/brand/1084-daiwa",
  "https://www.outlawpro.co.uk/brand/1502-dam",
  "https://www.outlawpro.co.uk/brand/1119-deeper-fish-finder",
  "https://www.outlawpro.co.uk/brand/1075-drennan",
  "https://www.outlawpro.co.uk/brand/1121-duracell-batteries",
  "https://www.outlawpro.co.uk/brand/1122-dynamite",
  "https://www.outlawpro.co.uk/brand/1123-e-sox",
  "https://www.outlawpro.co.uk/brand/1356-enterprise-tackle",
  "https://www.outlawpro.co.uk/brand/1082-esp-carp",
  "https://www.outlawpro.co.uk/brand/1474-favorite",
  "https://www.outlawpro.co.uk/brand/1102-fortis",
  "https://www.outlawpro.co.uk/brand/1470-fox",
  "https://www.outlawpro.co.uk/brand/1471-fox-rage",
  "https://www.outlawpro.co.uk/brand/1344-frenzee",
  "https://www.outlawpro.co.uk/brand/1495-gaby",
  "https://www.outlawpro.co.uk/brand/1350-gardner",
  "https://www.outlawpro.co.uk/brand/1321-gator",
  "https://www.outlawpro.co.uk/brand/1484-go-fish",
  "https://www.outlawpro.co.uk/brand/1476-headbanger-lures",
  "https://www.outlawpro.co.uk/brand/1330-hinders-baits",
  "https://www.outlawpro.co.uk/brand/1508-imax",
  "https://www.outlawpro.co.uk/brand/1124-jag",
  "https://www.outlawpro.co.uk/brand/1077-jetboil",
  "https://www.outlawpro.co.uk/brand/1504-jprecison",
  "https://www.outlawpro.co.uk/brand/1492-jrc",
  "https://www.outlawpro.co.uk/brand/1083-korum",
  "https://www.outlawpro.co.uk/brand/1391-kumu",
  "https://www.outlawpro.co.uk/brand/1234-leech",
  "https://www.outlawpro.co.uk/brand/1482-leeda",
  "https://www.outlawpro.co.uk/brand/1342-lemco",
  "https://www.outlawpro.co.uk/brand/1392-liquirigs",
  "https://www.outlawpro.co.uk/brand/1475-lmab",
  "https://www.outlawpro.co.uk/brand/1436-magic-trout",
  "https://www.outlawpro.co.uk/brand/1500-map",
  "https://www.outlawpro.co.uk/brand/1472-matrix",
  "https://www.outlawpro.co.uk/brand/1238-maxima",
  "https://www.outlawpro.co.uk/brand/1477-molix",
  "https://www.outlawpro.co.uk/brand/1320-monkey-lures",
  "https://www.outlawpro.co.uk/brand/1481-munch-baits",
  "https://www.outlawpro.co.uk/brand/1494-n-brice",
  "https://www.outlawpro.co.uk/brand/1080-nash",
  "https://www.outlawpro.co.uk/brand/1126-navitas",
  "https://www.outlawpro.co.uk/brand/1431-okuma",
  "https://www.outlawpro.co.uk/brand/1440-pb-products",
  "https://www.outlawpro.co.uk/brand/1506-penn",
  "https://www.outlawpro.co.uk/brand/1106-preston-innovations",
  "https://www.outlawpro.co.uk/brand/1079-quantum",
  "https://www.outlawpro.co.uk/brand/1487-rapala",
  "https://www.outlawpro.co.uk/brand/1107-reuben-heaton",
  "https://www.outlawpro.co.uk/brand/1076-ridgemonkey",
  "https://www.outlawpro.co.uk/brand/1498-rippton",
  "https://www.outlawpro.co.uk/brand/1480-rozemeijer",
  "https://www.outlawpro.co.uk/brand/1483-salmo",
  "https://www.outlawpro.co.uk/brand/1505-savage-gear",
  "https://www.outlawpro.co.uk/brand/1501-shakespeare",
  "https://www.outlawpro.co.uk/brand/1074-shimano",
  "https://www.outlawpro.co.uk/brand/1499-skee-tex",
  "https://www.outlawpro.co.uk/brand/1444-skills-tackle",
  "https://www.outlawpro.co.uk/brand/1104-solar-tackle",
  "https://www.outlawpro.co.uk/brand/1094-sonik",
  "https://www.outlawpro.co.uk/brand/1128-sonubaits",
  "https://www.outlawpro.co.uk/brand/1479-spomb",
  "https://www.outlawpro.co.uk/brand/1111-sportex",
  "https://www.outlawpro.co.uk/brand/1129-sticky-baits",
  "https://www.outlawpro.co.uk/brand/1497-strike-king",
  "https://www.outlawpro.co.uk/brand/1491-sufix",
  "https://www.outlawpro.co.uk/brand/1078-summit",
  "https://www.outlawpro.co.uk/brand/1442-tails-up-bait",
  "https://www.outlawpro.co.uk/brand/1105-thinking-anglers",
  "https://www.outlawpro.co.uk/brand/1073-trakker",
  "https://www.outlawpro.co.uk/brand/1130-vass",
  "https://www.outlawpro.co.uk/brand/1488-westin",
  "https://www.outlawpro.co.uk/brand/1131-wolf",
  "https://www.outlawpro.co.uk/brand/1417-wychwood-carp",
  "https://www.outlawpro.co.uk/brand/1132-z-man"
]


all_product_urls = []
for brand_url in brand_urls:
    product_urls = get_product_urls(brand_url)
    all_product_urls.extend(product_urls)
    print(f"Completed scraping brand URL: {brand_url}")

# Save to CSV
with open('product_urls.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URLs'])
    for url in all_product_urls:
        writer.writerow([url])

print("All product URLs collected and saved to CSV.")
