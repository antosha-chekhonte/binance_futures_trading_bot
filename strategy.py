import pandas as pd
import engine
import settings


def primitive_strategy(k, interval, data_range):
    try:
        precision = settings.precisions[k][0]
        quantity_precision = settings.precisions[k][1]
        df = pd.DataFrame(settings.client.futures_historical_klines(k, interval, data_range))
        df = df.drop([0, 5, 6, 7, 8, 9, 10, 11], axis=1)
        df = df.rename({1: 'Open', 2: 'High', 3: 'Low', 4: 'Close'}, axis=1)
        df = df.astype({'Open': float, 'High': float, 'Low': float, 'Close': float})

        if df.iat[-4, 0] > df.iat[-4, 3] and df.iat[-3, 0] < df.iat[-3, 3] and df.iat[-2, 0] < df.iat[-2, 3]:
            entry_price = round((df.iat[-2, 1] + 2 / (10 ** precision)), precision)
            price = round(entry_price + 1 / (10 ** precision), precision)
            price_for_stop = round((df.iat[-2, 2] - 2 / (10 ** precision)), precision)
            price_for_stop_limit = round((price_for_stop - 1 / (10 ** precision)), precision)
            price_for_take = round((entry_price + entry_price * 0.01), precision)
            quantity = round(settings.quantity / entry_price, quantity_precision)

            settings.symbols[k] = [entry_price, price, price_for_take, price_for_stop, price_for_stop_limit,
                                   quantity]
            settings.orders = engine.place_order(k, 'BUY')

        return settings.orders, settings.symbols

    except Exception as e:
        print("get price error: {}".format(e))