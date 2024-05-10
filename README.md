# Trading bot for binance futures

The trading strategy is as simple as possible:
- place a buy order at the high price of the previous bar, if the two previous bars are green and the bar before them is red;
- place a stop order at the minimum price of the previous bar;
- place a take order at the entry price + 1%;

The strategy can be applied to any number of trading pairs. Their list is presented in a variable. You can extend this list with any number of trading pairs: you just need to specify precision(the number of decimal places in the ticker price) and quantity_precision (the number of decimal places in the lot size) from the specification of trading pairs on Binance.

The limit on the number of simultaneously open positions can be changed in the variable 'limit' in the file 'settings.py'.
Trading is carried out with a fixed lot of 100 USDT. Can be changed in the `quantity` variable in the file 'settings.py'.

You can replace this strategy with your own or modify it in the file 'strategy.py'

What you need for work:
- install all dependencies from the `requirements.txt` file;
- register on the exchange [https://www.binance.com], get keys for the api and fill in the global variables `api_key` and `api_secret`;
- run the files 'userstream.py' and 'main.py'.

Minimal control of continuous operation is implemented. If the number of errors during operation exceeds a certain limit (can be changed in the variable 'errors' in file 'main.py'), the bot terminates its work.