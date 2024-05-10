import asyncio
from binance import AsyncClient, BinanceSocketManager
import settings


async def main():
    client = await AsyncClient.create(settings.api_key, settings.api_secret)
    bm = BinanceSocketManager(client,)
    # start any sockets here, i.e a trade socket
    ts = bm.futures_socket()
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)
            if res['e'] == 'ORDER_TRADE_UPDATE':
                order_info = res['o']
                id = order_info['i']
                status = order_info['X']
                if status == 'NEW':
                    with open('new_orders.txt', 'a') as f:
                        print(str(id), file=f)
                if status == 'FILLED':
                    with open('filled_orders.txt', 'a') as f:
                        print(str(id), file=f)


    await client.close_connection()

if __name__ == "__main__":
    print("Usertream opened")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())