import requests
from bs4 import BeautifulSoup
import csv

def scrape(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        data = []

        h1_header = soup.find('h1')
        h1_text = h1_header.text.strip()
        data.append(h1_text)

        tables = soup.find_all('table')
        table = tables[3]

        rows = table.find_all('tr')
        for row in rows[:-1]:
            first_cell = row.find('td')
            first_cell = first_cell.text.strip()
            data.append(first_cell)

        return data

    else:
        print(f"Failed to retrieve the page. Error code: {response.status_code}")
        return None

data_rows = []

num_pokemon = 1010
for i in range(1, num_pokemon+1):
    url = f"https://pokemondb.net/pokedex/{i}"
    data = scrape(url)

    if data:
        data_rows.append(data)

csv_file = 'output_file.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_rows)

print(f"Data successfully exported to {csv_file}.")
