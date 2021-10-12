import requests
from bs4 import BeautifulSoup as bs

url = 'https://economictimes.indiatimes.com/markets/stocks/stock-market-holiday-calendar'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
r = requests.get(url, headers = headers)

soup = bs(r.text, 'html.parser')
rows = soup.find('tbody').find_all('tr')


trading_holiday_list = []
for row in rows[:-1]:
    td_list = row.find_all("td")
    trading_holiday_list.append(td_list[2].string)

with open("trading_holidays.csv", 'w') as f:
    f.write("\n".join(trading_holiday_list))