import requests
from bs4 import BeautifulSoup as bs

def is_holiday():
    url = 'https://economictimes.indiatimes.com/markets/stocks/stock-market-holiday-calendar'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    r = requests.get(url, headers = headers)

    soup = bs(r.text, 'html.parser')
    rows = soup.find('tbody').find_all('tr')

    trading_holiday_list = []
    for row in rows[:-1]:
        td_list = row.find_all("td")
        trading_holiday_list.append(td_list[2].string)
    trading_holiday_list[:2]

    from datetime import date, datetime

    #get today's date in string format to compare it with trading holiday list
    today_str = date.today().strftime("%B %d, %Y")

    # Returns the day as a number, from 0 to 6, with Sunday being 0 and Saturday being 6
    today_day = date.today().strftime("%w")

    if (today_day == "0") or (today_day == "6") or (today_str in trading_holiday_list):
        return 'Today is a Holiday'
    else:
        return 'Today is not a Holiday'

print(is_holiday())