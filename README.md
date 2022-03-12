# binance-history-download
A module to automatically download binance's historic data from spot and futures markets. This is a small part of a larger flask based app, that stores the historic trading date from binance in a local database and it allows retreiving the data via REST API.

# basic functionality
1. **Automatic downloading and processing historic data from https://data.binance.vision/**
2. Processing of historic data and storing into a local database (*not in the repo*)
3. Importing current data from binance websocket connection https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api (*not in the repo*)
4. Retreiving trading data via api (*not in the repo; see requests examples*)


# requests examples
1. 5minute klines of futures ETHUSDT pair  
`curl --location --request GET 'api.marketdata.kreacija.eu/klines' \
--header 'Authorization: Bearer very_secret_token_do_not_share' \
--header 'Content-Type: application/json' \
--data-raw '{"filter":[["symbol","==","FUETHUSDT"],["timeframe","==","5m"]],
"limit":500,
"order_by": "close_time"
        }'`
 2. sorted trending pairs with the biggest price changes       
`curl --location --request GET 'api.marketdata.kreacija.eu/trending_klines' \
--header 'Authorization: Bearer very_secret_token_do_not_share' \
--header 'Content-Type: application/json' \
--data-raw '{
        }'`
        
# files and folders
- **download_binance_price_history.py** - automatic downloading of history for chosen symbols (pairs). 
- **tmp_downloads/** - location where the historic data is downloaded

# use example
python download_binance_price_history.py
