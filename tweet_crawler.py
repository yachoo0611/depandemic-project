from twitterscraper.query import query_tweets 
import csv 
import datetime 
import json
#from ibm_watson import NaturalLanguageUnderstandingV1
#from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions
#from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
keyword = 'covid' 
f = open(keyword+'.csv','w',encoding='UTF-8-sig',newline='') 
w = csv.writer(f,delimiter=',') 
list_of_tweets = query_tweets(keyword, begindate=datetime.date(2020,7,27), enddate=datetime.date(2020,8,1), limit=100) 

for tweet in list_of_tweets: 
    w.writerow([tweet.timestamp, tweet.text]) 
f.close()

authenticator = IAMAuthenticator('Fuxoqi_ltW0gcE6PZkYT-lMS8zsY0Xtd7AfaKzqesa_W')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/f85b9cf9-3ab1-477c-8627-5dd173ced2c1')

f = open('covid.csv', 'r', encoding='UTF-8-sig', newline='')
rdr = csv.reader(f)
for line in rdr:
    with open(line[0][:10] + '.json', 'w', encoding='UTF-8-sig', newline='') as json_file:
        response = natural_language_understanding.analyze(text=line[1], features=Features(relations=RelationsOptions(),
                                                                                          entities=EntitiesOptions(
                                                                                              emotion=True,
                                                                                              sentiment=True, limit=2),
                                                                                          keywords=KeywordsOptions(
                                                                                              emotion=True,
                                                                                              sentiment=True, limit=2)),
                                                          language='en').get_result()
        json.dump(response, json_file, indent=2)
