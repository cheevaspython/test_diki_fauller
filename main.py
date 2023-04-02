import os
import binance
import pandas as pd
import time
from statsmodels.tsa.stattools import adfuller


client = binance.Client()

def take_stat_for_binance_eth() -> None:
    """
    take stats ETHUSDT, add to tmp_list, show messages
    """
    timer: int = 0
    tmp_eth_list: list[float] =  []
    hour_price: float = 0
    save_df_data: list = []

    try:
        while True:
            all_tick = pd.DataFrame(client.get_ticker())
            eth = all_tick[all_tick.symbol.str.startswith('ETHUSDT')]
            tmp_eth_list.append((float(eth.iloc[0][['lastPrice']][0])))

            os.system("clear")

            if timer == 0:
                hour_price = float(eth.iloc[0][['lastPrice']][0])
            timer += 1

            if timer % 3600 == 0:
                if hour_price / tmp_eth_list[-1] >= 0.00000001:
                    persent_change_for_one = 'Price change for one percent!!!'
                    print(f"Press ctrl+c to exit.   <<< {persent_change_for_one} >>>\n" + 
                          f"{eth[['lastPrice', 'priceChangePercent']]}", flush=True)
                    time.sleep(1)
                    tmp_eth_list = []  
                    continue

            if timer % 10 == 0:
                    df_test = adfuller(tmp_eth_list)
                    if df_test[0] < df_test[4]['5%']:
                        fauller_message = 'Единичных корней нет, ряд стационарен'
                        print(f"Press ctrl+c to exit.   <<< {fauller_message} >>>\n" + 
                            f"{eth[['lastPrice', 'priceChangePercent']]}", flush=True)
                        save_df_data.append(df_test)
                        time.sleep(1)
                        continue

            print(f"Press ctrl+c to exit. \n{eth[['lastPrice', 'priceChangePercent']]}", 
                flush=True)

            time.sleep(1)

    except KeyboardInterrupt:
        print('\n   Good bye.')


if __name__ == '__main__':
    take_stat_for_binance_eth()

