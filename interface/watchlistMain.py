import tkinter as tk
import typing

from interface.styles import *
from models import *


class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str, Contracts], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binance_symbols = list(binance_contracts.keys())
        self._commands_frame = tk.Frame(self, bg=BG_COLOR)
        self._commands_frame.pack(side=tk.TOP)

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)

        self._binance_label = tk.Label(self._commands_frame, text='Binance', bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self._binance_label.grid(row=0, column=0)

        self._binance_entry = tk.Entry(self._commands_frame, justify=tk.CENTER)
        self._binance_entry.bind("<Return>", self._add_binance_symbol)
        self._binance_entry.grid(row=1, column=0)

        self.body_widget = dict()

        self._headers = ["Symbol", "Exchange", "Bid", "Ask", "Remove"]

        for idx, h in enumerate(self._headers):
            header = tk.Label(self._table_frame, text=h.capitalize(), bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0, column=idx)

        for h in self._headers:
            self.body_widget[h] = dict()
            if h in ['Bid', 'Ask']:
                self.body_widget[h + "_var"] = dict()

        self._body_index = 1

    def _add_binance_symbol(self, event):
        symbol = event.widget.get()
        if symbol in self.binance_symbols:
            self._add_symbol(symbol, "Binance")
            event.widget.delete(0, tk.END)

    def _remove_symbol(self, b_index: int):
        for h in self._headers:
            self.body_widget[h][b_index].grid_forget()
            del self.body_widget[h][b_index]

    def _add_symbol(self, symbol: str, exchange: str):
        b_index = self._body_index
        self.body_widget["Symbol"][b_index] = tk.Label(self._table_frame, text=symbol, bg=BG_COLOR, fg=FG_COLOR,
                                                       font=GLOBAL_FONT)
        self.body_widget["Symbol"][b_index].grid(row=b_index, column=0)

        self.body_widget["Exchange"][b_index] = tk.Label(self._table_frame, text=exchange, bg=BG_COLOR, fg=FG_COLOR,
                                                         font=GLOBAL_FONT)
        self.body_widget["Exchange"][b_index].grid(row=b_index, column=1)

        self.body_widget["Bid_var"][b_index] = tk.StringVar()
        self.body_widget["Bid"][b_index] = tk.Label(self._table_frame,
                                                    textvariable=self.body_widget["Bid_var"][b_index], bg=BG_COLOR,
                                                    fg=FG_COLOR, font=GLOBAL_FONT)
        self.body_widget["Bid"][b_index].grid(row=b_index, column=2)

        self.body_widget["Ask_var"][b_index] = tk.StringVar()
        self.body_widget["Ask"][b_index] = tk.Label(self._table_frame,
                                                    textvariable=self.body_widget["Ask_var"][b_index], bg=BG_COLOR,
                                                    fg=FG_COLOR, font=GLOBAL_FONT)
        self.body_widget["Ask"][b_index].grid(row=b_index, column=3)

        self.body_widget["Remove"][b_index] = tk.Button(self._table_frame, text="X", fg=BG_COLOR, bg=FG_COLOR,
                                                        font=GLOBAL_FONT, command=lambda: self._remove_symbol(b_index))
        self.body_widget["Remove"][b_index].grid(row=b_index, column=4)

        self._body_index += 1
