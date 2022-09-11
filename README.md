# tradingview-list
This website (https://tvdb.brianthe.dev) lists symbol, exchange, and screener supported by the python library [tradingview-ta](https://github.com/brian-the-dev/python-tradingview-ta). The database isn't complete, so please open an issue if you can't find your country. Please note that indices are not supported by tradingview-ta, this is a limitation from TradingView's API, not the library.

Before filing an issue, make sure that the symbol(s) you are requesting are NOT index/indices, such as BANKNIFTY and NIFTY50. This has been requested numerous times (#14, #29, #30, #38, #39); however, the limitation is solely related to TradingView rather than python-tradingview-ta.

Note (2022-06-27): This repo no longer serves the `tradingview.db` file as it is now generated during build. Please run `python update.py` locally if you need the database file.
