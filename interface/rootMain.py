import logging
import tkinter as tk

from connectors.binance_future import BinanceFutureClient
from interface.loggingMain import Logging
from interface.strategyMain import StrategyEditor
from interface.styles import *
from interface.tradesMain import TradesWatch
from interface.watchlistMain import Watchlist

logger = logging.getLogger()


class Root(tk.Tk):
    def __init__(self, binance: BinanceFutureClient):
        super().__init__()
        self.title("Trading Bot")
        self.binance = binance
        self.configure(bg=BG_COLOR)

        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side=tk.LEFT)

        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side=tk.LEFT)

        self._watchlist_frame = Watchlist(self.binance.contracts, self._left_frame, bg=BG_COLOR)
        self._watchlist_frame.pack(side=tk.TOP)

        self.logging_frame = Logging(self._left_frame, bg=BG_COLOR)
        self.logging_frame.pack(side=tk.TOP)

        self._strategy_frame = StrategyEditor(self, self.binance, self._right_frame, bg=BG_COLOR)
        self._strategy_frame.pack(side=tk.TOP)

        self._trades_frame = TradesWatch(self._left_frame, bg=BG_COLOR)
        self._trades_frame.pack(side=tk.TOP)

        self._update_ui()

    def _update_ui(self):

        for log in self.binance.logs:
            if not log['displayed']:
                self.logging_frame.add_log(log['log'])
                log['displayed'] = True

        try:
            for b_index, strat in self.binance.strategies.items():
                for log in strat.logs:
                    if not log['displayed']:
                        self.logging_frame.add_log(log['log'])
                        log['displayed'] = True

                for trade in strat.trades:
                    if trade.time not in self._trades_frame.body_widget['Symbol']:
                        self._trades_frame.add_trade(trade)

                    #precision = trade.contract.price_decimals
                    pnl_str = round(trade.pnl,2)
                    self._trades_frame.body_widget['PNL_var'][trade.time].set(pnl_str)
                    self._trades_frame.body_widget['Status_var'][trade.time].set(trade.status.capitalize())


        except RuntimeError as e:
            logger.error("Error While Looping through watchlist dictionary: %s", e)

        try:
            for key, value in self._watchlist_frame.body_widget["Symbol"].items():
                symbol = self._watchlist_frame.body_widget["Symbol"][key].cget("text")
                exchange = self._watchlist_frame.body_widget["Exchange"][key].cget("text")

                if exchange == "Binance":
                    if symbol not in self.binance.contracts:
                        continue

                    if symbol not in self.binance.prices:
                        self.binance.get_bid_ask(self.binance.contracts[symbol])
                        continue
                    precision = self.binance.contracts[symbol].price_decimals

                    prices = self.binance.prices[symbol]

                else:
                    continue

                if prices['bid'] is not None:
                    prices_str = '{0:.{prec}f}'.format(prices['bid'], prec=precision)
                    self._watchlist_frame.body_widget["Bid_var"][key].set(prices_str)

                if prices['ask'] is not None:
                    prices_str = '{0:.{prec}f}'.format(prices['ask'], prec=precision)
                    self._watchlist_frame.body_widget["Ask_var"][key].set(prices_str)
        except RuntimeError as e:
            logger.error("Error While Looping through watchlist dictionary: %s", e)

        self.after(1000, self._update_ui)
