from time import sleep
import re
from datetime import datetime

# from lib.squeeze_object import full_ticker
from lib.yahoo_tools import get_ticker_info
from lib.reddit_tools import squeeze_reddit

###### TODO 
# Transférer le ticker_data dans full_ticker class
# Filtrer les news par date
# Faire un affichage qui fait du sens
# Couleurs pour les +- ?
# Ajoutez les shorts stats & week range
# Mettre des limits de # de submissions affiché ? 
# Mettre le nombre de submissions total ?



class ticker_data():
    def __init__(self, ticker_name, ticker_yf):
        self.ticker_name = ticker_name
        self.ticker_yf = ticker_yf
        self.submissions_list = []
        self.news_list = []
        self.seen_title = []

        self.calculate_daily_change()

    def calculate_daily_change(self):
        day_change_per = ( self.ticker_yf.fast_info['last_price'] -  self.ticker_yf.fast_info['regular_market_previous_close'] ) /  self.ticker_yf.fast_info['regular_market_previous_close'] * 100
        self.day_change = "%.2f" % day_change_per
        self.last_price = "%.2f" % self.ticker_yf.fast_info['last_price'] 

    def show_self(self):
        if float(self.day_change) > 0:
            self.sign = u'\u25b2'
        else:
            self.sign = u'\u25bc'
        print(f"\n=========== ${self.ticker_name} == {self.last_price}$ == {self.sign} {self.day_change}% ===========")

    def sort_submissions(self):
        self.submissions_list.sort(key= lambda x: x[1], reverse=True)



def scan_submissions_for_ticker(submissions_list):
    filtered_submissions = []
    for submission in submissions_list:
        title_word_list = submission.title.split(' ')
        for word in title_word_list:
            cleaned_word = re.sub('[^A-Za-z0-9]+', '', word)
            if cleaned_word.isupper() and len(cleaned_word) > 2:
                ticker_yf = get_ticker_info(cleaned_word)
                if ticker_yf:
                    submission.ticker_yf, submission.ticker_name = ticker_yf, cleaned_word
                    filtered_submissions.append(submission)
    
    return filtered_submissions

def create_tickers_object_list(submissions_list):
    tickers_object_list = []
    ticker_object_seen = []

    for submission in submissions_list:
        if submission.ticker_name not in ticker_object_seen:
            ticker_object_seen.append(submission.ticker_name)
            ticker_obj = ticker_data(submission.ticker_name, submission.ticker_yf)
            
            ticker_obj.submissions_list.append((submission.title, submission.score))
            ticker_obj.seen_title.append(submission.title)

            tickers_object_list.append(ticker_obj)
        else:
            for ticker_obj in tickers_object_list:
                if ticker_obj.ticker_name == submission.ticker_name:
                    if submission.title not in ticker_obj.seen_title:
                        if len(submission.title) > 1:
                            ticker_obj.submissions_list.append((submission.title, submission.score))
                            ticker_obj.seen_title.append(submission.title)
    return tickers_object_list

reddit = squeeze_reddit()

hot_submissions = list(reddit.client.subreddit("shortsqueeze").hot(limit=reddit.post_limit))
rising_submissions = list(reddit.client.subreddit("shortsqueeze").rising(limit=reddit.post_limit))
new_submissions = list(reddit.client.subreddit("shortsqueeze").new(limit=reddit.post_limit))



hot_tickers_submissions = scan_submissions_for_ticker(hot_submissions + rising_submissions + new_submissions)

tickers_object_list = create_tickers_object_list(hot_tickers_submissions)

for ticker_obj in tickers_object_list:
    ticker_obj.sort_submissions()
    ticker_obj.show_self()
    print(' - Reddit - ')
    for submission in ticker_obj.submissions_list:
        print(f'  | {submission[1]} | - {submission[0]}')
    print('')
    print(' - News - ')
    for news in ticker_obj.ticker_yf.news[0:2]:
        news_date = datetime.strftime(datetime.fromtimestamp(news['providerPublishTime']), '%Y-%m-%d %H:%M')
        news_title = news['title']
        print(f'  | {news_date} | - {news_title}')
print('\n\n')



