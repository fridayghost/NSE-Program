from datetime import date, datetime, timedelta
from nsepy import get_history
import pandas as pd
import time
from yagmail_send import yagsend_nse
from add_remove_email import read_authorised_id
import os

def nse_data_mail():
    # finds and removes any previous NSE excel sheet
    cwd = os.getcwd()
    for parent, dirs, files in os.walk(cwd):
        for file in files:
            if ("NSE" in file) and ("xlsx" in file):
                print("Deleting file", file)
                os.remove(file)

    begin = time.time()

    mail_list = read_authorised_id()
    print("Authorised Mailing list : ", (", ".join(mail_list)))

    #Gets to year,month,day and from year,month,day
    to_ = date.today()
    from_ = to_ +  timedelta(days = -60)

    to_year = to_.year
    to_month = to_.month
    to_day = to_.day

    from_year = from_.year
    from_month = from_.month
    from_day = from_.day

    #Gets stocks names from the csv file as stores it in 'list'
    with open('stocks.csv', 'r') as f:
        list = f.read().strip().replace(',', '').split('\n')

    data_dict = {}
    for item in list:
        data_dict[f'{item}'] = get_history(symbol=item,
                                           start=date(from_year, from_month,from_day),
                                           end=date(to_year,to_month,to_day))

    # Iterates through the Individual stocks dataframes, performs caluclations and stores it in the 'final_list'
    final_list = []

    for item in list:
        deli_volume = data_dict[item].iloc[-1,12]

        last_close_price = data_dict[item].iloc[-1,7]

        df5 = data_dict[item].tail(5)
        five_days_deli_volume = df5['Deliverable Volume'].mean()

        df10 = data_dict[item].tail(10)
        ten_days_deli_volume = df10['Deliverable Volume'].mean()

        if deli_volume > five_days_deli_volume:
            x = 'Yes'
        else:
            x = 'No'

        temp_list = [item, deli_volume, last_close_price, five_days_deli_volume, ten_days_deli_volume, x]
        final_list.append(temp_list)

    df = pd.DataFrame(final_list)
    df.columns = ['Stock Name', 'Last Delivery Volume', 'Last Close Price', '5 Days Delivery Volume', '10 Days Delivery Volume', '1D > 5D']
    df.to_excel(f'NSE_{to_}.xlsx', index=False, freeze_panes=(1,1))

    for id in mail_list:
        yagsend_nse(id, f"NSE_Sheet_{to_}", f"Here is today's NSE sheet (Date : {to_}) ", f'NSE_{to_}.xlsx')

    end = time.time()
    time_taken = end - begin
    print(f"Time Taken : {time_taken}")

with open('trading_holidays.csv', 'r') as f:
    trading_holiday_list = f.read().split('\n')
    
#get today's date in string format to compare it with trading holiday list
today_str = date.today().strftime("%B %d, %Y")

# Returns the day as a number, from 0 to 6, with Sunday being 0 and Saturday being 6
today_day = date.today().strftime("%w")

if today_str not in trading_holiday_list:
    nse_data_mail()