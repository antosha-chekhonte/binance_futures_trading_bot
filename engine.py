import settings
from datetime import datetime

def on_open(ws):
    print("Сonnection opened")


def on_close(ws):
    print(datetime.now())
    print("Connection closed")


def place_order(k, side):
    try:
        order = settings.client.futures_create_order(
            symbol=k,
            type='STOP',
            price=settings.symbols[k][1],
            stopPrice=settings.symbols[k][0],
            side=side,
            quantity=settings.symbols[k][5])
        print(order)
        order_id = order['orderId']
        settings.orders[k] = order_id

        return settings.orders

    except Exception as e:
        print("Place order error: {}".format(e))


def take(k):
    try:
        take_order = settings.client.futures_create_order(
            symbol=k,
            type='LIMIT',
            price=settings.symbols[k][2],
            side='SELL',
            timeInForce='GTC',
            reduceOnly=True,
            quantity=settings.symbols[k][5],
        )
        take_order_id = take_order['orderId']
        print("Take order info: {}".format(take_order))

        return take_order_id

    except Exception as e:
        print("Take order error: {}".format(e))


def stop(k):
    try:
        stop_order = settings.client.futures_create_order(
            symbol=k,
            type='STOP',
            price=settings.symbols[k][4],
            stopPrice=settings.symbols[k][3],
            side='SELL',
            reduceOnly=True,
            quantity=settings.symbols[k][5],
        )
        order_id = stop_order['orderId']
        print("Stop order info: {}".format(stop_order))

        return order_id

    except Exception as e:
        print("Stop order error: {}".format(e))


def cancel_all_orders(symbol): # cancels all orders for the ticker specified in argument
    try:
        result = settings.client.futures_cancel_all_open_orders(
            symbol=symbol)
        print(f"Canceling order {symbol}: {result}")

    except Exception as e:
        print(f"Cancel order error {symbol}: {e}")