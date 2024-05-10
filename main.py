import websocket
import json
import time
import sys
import settings
import engine
import strategy
from datetime import datetime


is_candle_opened = True
in_position = False
take_and_stop_placed = False
errors = 0
count = 0


def on_message(ws, msg):
    global is_candle_opened, in_position, take_and_stop_placed, errors, count
    try:
        json_message = json.loads(msg)
        candle = json_message['k']
        is_candle_closed = candle['x']
        if is_candle_opened:
            if in_position is False:
                for k in settings.precisions.keys():  # Placing orders on tickers corresponding to the strategy
                    if k not in settings.takes or settings.takes[k] is None:
                        strategy.primitive_strategy(k, settings.INTERVAL, settings.DATA_RANGE)
                in_position = True

            if in_position is True and settings.orders:  # Order Status Checking and Take and Stop Placing
                with open('filled_orders.txt', 'r') as f:
                    lines = f.readlines()
                    print(lines)
                for line in lines:
                    for k in list(settings.orders.keys()):
                        if line == (str(settings.orders[k])):
                            print(datetime.now())
                            print(
                                f'{k} Long. Entry_price is {settings.symbols[k][0]},'
                                f' Take_price is {settings.symbols[k][2]}, Stop_price is {settings.symbols[k][3]}')
                            count += 1
                            settings.takes[k] = engine.take(k)
                            settings.stops[k] = engine.stop(k)
                            del settings.orders[k]
                            take_and_stop_placed = True

            if count > settings.limit:
                for ticker in settings.orders.keys():
                    engine.cancel_all_orders(symbol=ticker)
                count = 0

            if in_position is True and settings.takes:  # Order status checking for stop and take orders
                with open('filled_orders.txt', 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    for k in list(settings.stops.keys()):
                        if line == (str(settings.stops[k])):
                            print(datetime.now())
                            print(f"{k} is stopped.")
                            engine.cancel_all_orders(symbol=k)
                            del settings.takes[k]
                            del settings.stops[k]
                            count -= 1

                    for k in list(settings.takes.keys()):
                        if line == (str(settings.takes[k])):
                            print(datetime.now())
                            print(f"{k} is taken")
                            engine.cancel_all_orders(symbol=k)
                            del settings.takes[k]
                            del settings.stops[k]
                            count -= 1

        if is_candle_closed:
            print(datetime.now())
            if in_position:  # canceling orders after timeframe expiration
                for k in settings.orders.keys():
                    if k not in settings.takes:
                        engine.cancel_all_orders(symbol=k)
            in_position = False
            count = 0
            settings.orders = {}
            is_candle_opened = True
            time.sleep(3)

    # if the number of operational errors during th bot operation exceeds 10, the bot operation is interrupted
    except Exception as e:
        print("Websocket stream error: {}".format(e))
        errors += 1
        print(errors)
        if errors > 10:
            sys.exit()


ws = websocket.WebSocketApp(settings.SOCKET, on_open=engine.on_open, on_close=engine.on_close, on_message=on_message)
ws.run_forever()
