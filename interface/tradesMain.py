import tkinter as tk
from models import *
import datetime
from interface.styles import *


class TradesWatch(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body_widget = dict()
        self._headers = ["Time", "Symbol", "Exchange", "Strategy", "Side", "Qauntity", "Status", "PNL"]

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)

        for idx, h in enumerate(self._headers):
            header = tk.Label(self._table_frame, text=h.capitalize(), bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0, column=idx)

        for h in self._headers:
            self.body_widget[h] = dict()
            if h in ['Status', 'PNL']:
                self.body_widget[h + "_var"] = dict()

        self._body_index = 1

    def add_trade(self, data: Trade):
        b_index = self._body_index

        t_index = data.time
        dt_str = datetime.datetime.fromtimestamp(data.time / 1000).strftime("%b %d %H:%M")
        self.body_widget["Time"][t_index] = tk.Label(self._table_frame, text=dt_str, bg=BG_COLOR, fg=FG_COLOR,
                                                     font=GLOBAL_FONT)
        self.body_widget["Time"][t_index].grid(row=b_index, column=0)

        self.body_widget["Symbol"][t_index] = tk.Label(self._table_frame, text=data.contract.symbol, bg=BG_COLOR, fg=FG_COLOR,
                                                       font=GLOBAL_FONT)
        self.body_widget["Symbol"][t_index].grid(row=b_index, column=1)

        self.body_widget["Exchange"][t_index] = tk.Label(self._table_frame, text="Binance", bg=BG_COLOR,
                                                         fg=FG_COLOR,
                                                         font=GLOBAL_FONT)
        self.body_widget["Exchange"][t_index].grid(row=b_index, column=2)

        self.body_widget["Strategy"][t_index] = tk.Label(self._table_frame, text=data.strategy, bg=BG_COLOR,
                                                         fg=FG_COLOR,
                                                         font=GLOBAL_FONT)
        self.body_widget["Strategy"][t_index].grid(row=b_index, column=3)

        self.body_widget["Side"][t_index] = tk.Label(self._table_frame, text=data.side, bg=BG_COLOR, fg=FG_COLOR,
                                                     font=GLOBAL_FONT)
        self.body_widget["Side"][t_index].grid(row=b_index, column=4)

        self.body_widget["Qauntity"][t_index] = tk.Label(self._table_frame, text=data.quantity, bg=BG_COLOR,
                                                         fg=FG_COLOR,
                                                         font=GLOBAL_FONT)
        self.body_widget["Qauntity"][t_index].grid(row=b_index, column=5)

        self.body_widget["Status_var"][t_index] = tk.StringVar()
        self.body_widget["Status"][t_index] = tk.Label(self._table_frame,
                                                       textvariable=self.body_widget["Status_var"][t_index],
                                                       bg=BG_COLOR,
                                                       fg=FG_COLOR, font=GLOBAL_FONT)
        self.body_widget["Status"][t_index].grid(row=b_index, column=6)

        self.body_widget["PNL_var"][t_index] = tk.StringVar()
        self.body_widget["PNL"][t_index] = tk.Label(self._table_frame,
                                                    textvariable=self.body_widget["PNL_var"][t_index], bg=BG_COLOR,
                                                    fg=FG_COLOR, font=GLOBAL_FONT)
        self.body_widget["PNL"][t_index].grid(row=b_index, column=7)

        self._body_index += 1
