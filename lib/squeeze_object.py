class full_ticker():
    def __init__(self, ticker_name):
        self.ticker_name = ticker_name
        self.ticker = None
        self.day_change = None
        self.last_price = None
        self.get_stock_info()
        self.calculate_daily_change()

    def get_stock_info(self):
        self.ticker = yf.Ticker(self.ticker_name)
        self.last_price = self.ticker.fast_info['last_price']
        
    def calculate_daily_change(self):
        day_change_per = ( self.ticker.fast_info['last_price'] -  self.ticker.fast_info['regular_market_previous_close'] ) /  self.ticker.fast_info['regular_market_previous_close'] * 100
        self.day_change = "%.2f" % day_change_per
        self.last_price = "%.2f" % self.ticker.fast_info['last_price'] 

    def show(self):
        if float(self.day_change) > 0:
            self.sign = u'\u25b2'
        else:
            self.sign = u'\u25bc'

        print(f'== ${self.ticker_name} == {self.last_price}$ == {self.sign} {self.day_change}% == ')
