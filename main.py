import tkinter as tk
import yfinance as yf
import plotly.graph_objects as go
import kaleido
import PIL.Image
import PIL.ImageTk


def commas(number):
    '''Places commas in the appropriate places of a number and formats trillions and billions'''
    num = str(number)

    if number > 1000:
        num = str(format(number, ',d'))

        if len(num) > 11:
            num = num[0:-8]
            num = num + "T"
            num = num[0:-5] + "." + num[-4:]

        elif len(num) > 8:
            num = num[0:-4]
            num = num + "B"
            num = num[0:-5] + "." + num[-4:]

    return num


class Stock():
    '''The model of the program'''

    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)
        self.info = self.ticker.info
        self.price = self.info['currentPrice']
        self.previous_close = self.info['previousClose']
        self.eps = self.info['trailingEps']
        self.volume = self.info['volume']
        self.revenue = self.info['totalRevenue']
        self.open = self.info['open']
        self.dividend = self.info['dividendYield']
        self.market_cap = self.info['marketCap']
        self.pe_ratio = self.info['trailingPE']
        self.one_day = self.ticker.history('2d')
        self.five_day = self.ticker.history('5d')
        self.one_month = self.ticker.history('1mo')
        self.three_month = self.ticker.history('3mo')
        self.one_year = self.ticker.history('1y')
        self.five_year = self.ticker.history('5y')
        self.max = self.ticker.history('max')


class GUI:
    '''The GUI of the program'''

    def __init__(self):

        self.root = tk.Tk(className=" Stocks")
        self.root.config(bg='#CCCCD9')
        self.info_frame = tk.Frame(self.root, bg='#CCCCD9')
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)
        self.info_frame.pack()

        self.price = tk.Label(self.info_frame, text=f"Price: ", font=('Arial', 35), bg='#CCCCD9')
        self.price.grid(row=0, column=0, columnspan=2)

        self.previous_close = tk.Label(self.info_frame, text=f"Previous Close: ", font=('Arial', 25), bg='#CCCCD9')
        self.previous_close.grid(row=1, column=0)

        self.open = tk.Label(self.info_frame, text="Open: ", font=('Arial', 25), bg='#CCCCD9')
        self.open.grid(row=1, column=1)

        self.eps = tk.Label(self.info_frame, text="EPS(TTM): ", font=('Arial', 25), bg='#CCCCD9')
        self.eps.grid(row=4, column=1)

        self.dividend_yield = tk.Label(self.info_frame, text="Dividend Yield: ", font=('Arial', 25), bg='#CCCCD9')
        self.dividend_yield.grid(row=2, column=1)

        self.volume = tk.Label(self.info_frame, text="Volume: ", font=('Arial', 25), bg='#CCCCD9')
        self.volume.grid(row=3, column=0)

        self.market_cap = tk.Label(self.info_frame, text="Market Cap: ", font=('Arial', 25), bg='#CCCCD9')
        self.market_cap.grid(row=3, column=1)

        self.total_revenue = tk.Label(self.info_frame, text="Total Revenue: ", font=('Arial', 25), bg='#CCCCD9')
        self.total_revenue.grid(row=4, column=0)

        self.pe_ratio = tk.Label(self.info_frame, text="PE Ratio(TTM): ", font=('Arial', 25), bg='#CCCCD9')
        self.pe_ratio.grid(row=2, column=0)

        img = tk.PhotoImage(file="white.png")
        self.stock_graph = tk.Label(self.info_frame, image=img, width=700, height=500, bg='#CCCCD9')
        self.stock_graph.grid(row=0, column=3, rowspan=5, columnspan=8)

        self.alert = tk.Label(self.info_frame, text="", bg='#CCCCD9')
        self.alert.grid(row=7, columnspan=2)

        '''Updates the labels with the appropriate stock information'''

        def return_ticker():
            self.alert.config(text="")
            try:
                self.stock = Stock(self.tick.get())
                self.price.config(text="Price: $" + commas(self.stock.price))
                self.previous_close.config(text="Previous Close: $" + commas(self.stock.previous_close))
                self.eps.config(text="EPS(TTM): $" + commas(self.stock.eps))
                self.volume.config(text="Volume: " + commas(self.stock.volume))
                self.total_revenue.config(text=f"Total Revenue: $" + commas(self.stock.revenue))
                self.open.config(text=f"Open: $" + commas(self.stock.open))

                fig = go.Figure(
                    data=go.Scatter(x=self.stock.one_day.index, y=self.stock.one_day['Close'], mode='lines'))
                fig.write_image("graph.png")
                im = PIL.Image.open("graph.png")
                photo = PIL.ImageTk.PhotoImage(im)
                self.stock_graph.config(image=photo)
                self.stock_graph.image = photo
                try:
                    self.dividend_yield.config(
                        text=f"Dividend Yield: " + commas(round((self.stock.dividend * 100), 3)) + "%")
                except:
                    self.dividend_yield.config(text="Dividend Yield: 0%")
                self.market_cap.config(text=f"Market Cap: $" + commas(self.stock.market_cap))
                self.pe_ratio.config(text=f"PE Ratio(TTM): " + commas(round(self.stock.pe_ratio, 3)))

            except:
                self.alert.config(text="Stock not found.")

        self.ticker_frame = tk.Frame(self.info_frame, bg='#CCCCD9')
        self.ticker_frame.grid(row=5, column=0, columnspan=2, rowspan=2)

        self.ticker = tk.Label(self.ticker_frame, text="Ticker: ", font=('Arial', 25), bg='#CCCCD9')
        self.ticker.grid(row=0, column=0, sticky=tk.E)
        self.tick = tk.Entry(self.ticker_frame, highlightbackground="#CCCCD9")
        self.tick.grid(row=0, column=1)
        self.go_button = tk.Button(self.ticker_frame, text="Go", command=return_ticker, highlightbackground="#CCCCD9")
        self.go_button.grid(row=0, column=2)

        self.one_day_button = tk.Button(self.info_frame, text="1D", command=self.update_one_day,
                                        highlightbackground="#CCCCD9")
        self.one_day_button.grid(row=5, column=3, sticky=tk.E + tk.W)

        self.five_day_button = tk.Button(self.info_frame, text="5D", command=self.update_five_day,
                                         highlightbackground="#CCCCD9")
        self.five_day_button.grid(row=5, column=4, sticky=tk.W + tk.E)

        self.one_month_button = tk.Button(self.info_frame, text="1M", command=self.update_one_month,
                                          highlightbackground="#CCCCD9")
        self.one_month_button.grid(row=5, column=5, sticky=tk.W + tk.E)

        self.three_month_button = tk.Button(self.info_frame, text="3M", command=self.update_three_month,
                                            highlightbackground="#CCCCD9")
        self.three_month_button.grid(row=5, column=6, sticky=tk.W + tk.E)

        self.one_year_button = tk.Button(self.info_frame, text="1Y", command=self.update_one_year,
                                         highlightbackground="#CCCCD9")
        self.one_year_button.grid(row=5, column=7, sticky=tk.W + tk.E)

        self.five_year_button = tk.Button(self.info_frame, text="5Y", command=self.update_five_year,
                                          highlightbackground="#CCCCD9")
        self.five_year_button.grid(row=5, column=8, sticky=tk.W + tk.E)

        self.max_button = tk.Button(self.info_frame, text="MAX", command=self.update_max, highlightbackground="#CCCCD9")
        self.max_button.grid(row=5, column=9, sticky=tk.W + tk.E)

        self.root.mainloop()

    def update_one_day(self):
        try:
            fig = go.Figure(data=go.Scatter(x=self.stock.one_day.index, y=self.stock.one_day['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")


    def update_five_day(self):
        try:
            fig = go.Figure(data=go.Scatter(x=self.stock.five_day.index, y=self.stock.five_day['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")

    def update_one_month(self):
        try:
            fig = go.Figure(data=go.Scatter(x=self.stock.one_month.index, y=self.stock.one_month['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")

    def update_three_month(self):
        try:
            fig = go.Figure(
            data=go.Scatter(x=self.stock.three_month.index, y=self.stock.three_month['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")

    def update_one_year(self):
        try:
            fig = go.Figure(data=go.Scatter(x=self.stock.one_year.index, y=self.stock.one_year['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")

    def update_five_year(self):
        try:
            fig = go.Figure(data=go.Scatter(x=self.stock.five_year.index, y=self.stock.five_year['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")

    def update_max(self):
        try:
            fig = go.Figure(data=go.Scatter(x=self.stock.max.index, y=self.stock.max['Close'], mode='lines'))
            fig.write_image("graph.png")
            im = PIL.Image.open("graph.png")
            photo = PIL.ImageTk.PhotoImage(im)
            self.stock_graph.config(image=photo)
            self.stock_graph.image = photo
        except:
            self.alert.config(text="Stock not found.")


if __name__ == "__main__":
    gui = GUI()
