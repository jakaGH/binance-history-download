""" Module for downloading trading history from binance
# https://data.binance.vision/?prefix=data/
# https://github.com/binance/binance-public-data"""

import os
from datetime import datetime
import requests

# location of the temporary downloads folder
CONSTANTS = {}
CONSTANTS['downloads'] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'tmp_downloads/')


class SymbolHistory:
    """generic SymbolHistory (pair) object with methods to download
    historic data."""

    symbol_prefix = ''  # to differentiate between spot and 2 futures markets.
    market_string = ''  # market based part of the string in url

    def __init__(self,  name):
        self.name = name
        self._url_monthly_kline = 'https://data.binance.vision/data/'\
            + f'{self.market_string}/monthly/'\
            + f'klines/{name.upper()}/'+'{inr}'+f'/{name.upper()}'\
            + '-{inr}-{yr}-{mn}.zip'
        self._url_daily_kline = self._url_monthly_kline.format(
            inr='{inr}', yr=datetime.now().year, mn=str(datetime.now().month).
            zfill(2)).replace('monthly', 'daily').replace('.zip', '-{da}.zip')
        self._url_monthly_agg_trade = "https://data.binance.vision/data/"\
            + f"{self.market_string}/monthly/aggTrades"\
            + f"/{name.upper()}/{name.upper()}"\
            + "-aggTrades-{yr}-{mn}.zip"
        self._url_daily_agg_trade = self._url_monthly_agg_trade.format(
            inr='{inr}', yr=datetime.now().year, mn=str(datetime.now().month).
            zfill(2)).replace('monthly', 'daily').replace('.zip', '-{da}.zip')

    @staticmethod
    def month_year_iter(start_month, start_year):
        """generator iterator from start month/year to current month"""
        end_month = datetime.now().month
        end_year = datetime.now().year
        ym_start = 12*start_year + start_month - 1
        ym_end = 12*end_year + end_month - 1
        for year_month in range(ym_start, ym_end):
            year, month = divmod(year_month, 12)
            yield year, month + 1

    def download_file(self, url):
        """method for downloading files from url"""
        download_folder = CONSTANTS['downloads']
        file_original = self.symbol_prefix + url.split('/')[-1]

        local_filename = os.path.join(download_folder, file_original)
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as req:
            req.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in req.iter_content(chunk_size=8192):
                    file.write(chunk)
        return local_filename

    def download_historic_data(self, intervals, start_month, start_year,
                               url_monthly, url_daily):
        """method for dowloading the whole history from start month/year"""

        def get_monthly_url(url, interval, year, month):
            """formating of monthly url"""
            return url.format(inr=interval, yr=year, mn=str(month).zfill(2))

        def get_daily_url(url, interval, day):
            """formating of daily url"""
            return url.format(inr=interval, da=str(day).zfill(2))

        for interval in intervals:
            # download all data up to this month
            for year, month in SymbolHistory.month_year_iter(start_month,
                                                             start_year):
                try:
                    url = get_monthly_url(url_monthly, interval, year, month)
                    print(year, month, interval, url)
                    self.download_file(url)
                except Exception as exception:
                    print(exception)

            # download this month's data (today's not included)
            for day in range(1, datetime.now().day):
                try:
                    url = get_daily_url(url_daily, interval, day)
                    print(day, interval, url)
                    self.download_file(url)
                except Exception as exception:
                    print(exception)

    def download_klines(self, intervals, start_month, start_year):
        """method for dowloding klines"""
        self.download_historic_data(intervals, start_month, start_year,
                                    self._url_monthly_kline,
                                    self._url_daily_kline)

    def download_agg_trade(self, start_month, start_year):
        """method for dowloding agg trades"""
        self.download_historic_data([1], start_month, start_year,
                                    self._url_monthly_agg_trade,
                                    self._url_daily_agg_trade)

    def download_trades(self, start_month, start_year):
        """method for dowloding trades"""
        url_monthly = self._url_monthly_agg_trade.replace(
            "aggTrades", "trades")
        url_daily = self._url_daily_agg_trade.replace(
            "aggTrades", "trades")

        self.download_historic_data([1], start_month, start_year,
                                    url_monthly, url_daily)


class FuturesHistory(SymbolHistory):
    """Futures market object"""

    symbol_prefix = ''
    market_string = ''

    def download_mark_price_klines(self, intervals, start_month, start_year):
        """method for dowloding klines"""
        url_monthly = self._url_monthly_kline.replace(
            "/klines/", "/markPriceKlines/")
        url_daily = self._url_daily_kline.replace(
            "/klines/", "/markPriceKlines/")

        self.download_historic_data(intervals, start_month, start_year,
                                    url_monthly, url_daily)

    def download_premium_index_klines(self, intervals, start_month, start_year):
        """method for dowloding klines"""
        url_monthly = self._url_monthly_kline.replace(
            "/klines/", "/premiumIndexKlines/")
        url_daily = self._url_daily_kline.replace(
            "/klines/", "/premiumIndexKlines/")

        self.download_historic_data(intervals, start_month, start_year,
                                    url_monthly, url_daily)


class SpotHistory(SymbolHistory):
    """Spot market object"""

    symbol_prefix = 'SP'
    market_string = 'spot'


class FuturesUHistory(FuturesHistory):
    """Futures usdt object"""

    symbol_prefix = 'FU'
    market_string = 'futures/um'

    def download_index_price_klines(self, intervals, start_month, start_year):
        """method for downloding index_price_klines"""
        url_monthly = self._url_monthly_kline.replace(
            "/klines/", "/indexPriceKlines/")
        url_daily = self._url_daily_kline.replace(
            "/klines/", "/indexPriceKlines/")

        self.download_historic_data(intervals, start_month, start_year,
                                    url_monthly, url_daily)


class FuturesCHistory(FuturesHistory):
    """Futures coin object"""

    symbol_prefix = 'FC'
    market_string = 'futures/cm'


if __name__ == '__main__':

    spot_test = SpotHistory("BCHUSDT")
    futures_u_test = FuturesUHistory("BCHUSDT")
    futures_c_test = FuturesCHistory("BCHUSD_PERP")

    spot_test.download_klines(['12h'], 2, 2022)
    futures_u_test.download_klines(['12h'], 2, 2022)
    futures_c_test.download_klines(['12h'], 2, 2022)

    spot_test.download_agg_trade(2, 2022)
    futures_u_test.download_agg_trade(2, 2022)
    futures_c_test.download_agg_trade(2, 2022)

    spot_test.download_trades(2, 2022)
    futures_u_test.download_trades(2, 2022)
    futures_c_test.download_trades(2, 2022)

    # only available in FuturesUHistory
    futures_u_test.download_index_price_klines(['12h'], 2, 2022)

    # not available in SpotHistory
    futures_u_test.download_mark_price_klines(['12h'], 2, 2022)
    futures_c_test.download_mark_price_klines(['12h'], 2, 2022)

    # not available in SpotHistory
    futures_u_test.download_premium_index_klines(['12h'], 2, 2022)
    futures_c_test.download_premium_index_klines(['12h'], 2, 2022)
