import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search query from the form
        search_query = request.form['search_query']

        # Call a function to scrape data based on the search query
        scraped_data = scrape_data(search_query)

        return render_template('index.html', data=scraped_data)

    return render_template('index.html', data=[])


def scrape_data(search_query):
    product_names = []
    product_prices = []
    product_descriptions = []

    page_number = 1

    while True:
        url = f"https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_number}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Find all the product names on the page
        names = soup.find_all("div", class_="_4rR01T")
        prices = soup.find_all("div", class_="_30jeq3 _1_WHN1")
        descriptions = soup.find_all("div", class_="fMghEO")

        # If no more products are found on the page, break the loop
        if not names:
            break

        # Extract and append the text of each product name, price, and description to respective lists
        for name, price, desc in zip(names, prices, descriptions):
            product_names.append(name.text)
            product_prices.append(price.text)
            product_descriptions.append(desc.text)

        # Move to the next page
        page_number += 1

    # Return the scraped data as a dictionary
    scraped_data = {
        'product_names': product_names,
        'product_prices': product_prices,
        'product_descriptions': product_descriptions
    }

    return scraped_data


if __name__ == '__main__':
    app.run(debug=True)
