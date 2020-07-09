"""
import datetime 
from twitterscraper import query_tweets 

list_of_tweets = query_tweets('코로나바이러스', begindate=datetime.date(2020,7,6), enddate=datetime.date(2020,7,7), limit=5) 

for tweet in list_of_tweets: 
    print("screen_name: "+tweet.screen_name) #사용자아이디 
    print("username: "+tweet.username) #닉네임 
    print("timestamp: "+str(tweet.timestamp)) #날짜 
    print("text: "+tweet.text) #트윗내용
"""

from twitterscraper.query import query_tweets 
import csv 
import datetime 

keyword = '코로나바이러스' 
f = open(keyword+'.csv','w',encoding='utf-8-sig',newline='') 
w = csv.writer(f,delimiter=',') 
list_of_tweets = query_tweets(keyword, begindate=datetime.date(2020,7,1), enddate=datetime.date(2020,7,2), limit=5) 

for tweet in list_of_tweets: 
    w.writerow([tweet.timestamp, tweet.text]) 
f.close()
