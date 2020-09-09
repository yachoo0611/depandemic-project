import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import datetime
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, RelationsOptions
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from depandemic.models import Post

#API 키 등의 초기화는 최상단에 한번만 호출
consumer_key = 'WH7O98QsTNHInE7Osn9I6bjom'
consumer_secret = 'd16T80KdkQ7zB8TmAjcjOG2vtPryuA7i1R3KJ0oTfxt3PCxmJX'
atoken = '1295969346800345088-xYSWmzhn0zHj6BLeISi1SlGa5ufQ9t'
asecret = 'rdkj7OaQVK6xQKmscMVZGERJwjzzYRp53THTXOjiFI7F2'
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)

authenticator = IAMAuthenticator('Fuxoqi_ltW0gcE6PZkYT-lMS8zsY0Xtd7AfaKzqesa_W')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(
    'https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/f85b9cf9-3ab1-477c-8627-5dd173ced2c1')

def twitter_crwaler():
    
    send_data = {}
    end_data2 = []
    cursor = tweepy.Cursor(api.search, 
                        q='코로나',
                        since='2020-09-08', # 2020-09-08 이후에 작성된 트윗들로 가져옴
                        count=2  # 페이지당 반환할 트위터 수 1
                        ).items(100) #최대 100개 까지만
    for i, tweet in enumerate(cursor):
        #print("{}: {}".format(i, tweet.text))
        send_data['location'] = "Unknown"
        send_data['categorized'] = ""
        send_data['score'] = ""

        response = natural_language_understanding.analyze(
            text=tweet.text,
            features=Features(
                entities=EntitiesOptions(emotion=False),
                categories=EntitiesOptions(emotion=False, ),
                semantic_roles=EntitiesOptions(emotion=False, sentiment=False, ),
                keywords=KeywordsOptions(emotion=False, sentiment=False, )
            )
        ).get_result()

        for re in response['entities']:
            if re['type'] == "Location":
                send_data['location'] = re['text']
            else:
                send_data['location'] = "Unknown"

        for re1 in response['categories']:
            send_data['categorized'] = re1['label']
            send_data['score'] = re1['score']

        send_data['author'] = tweet.author.name
        send_data['title'] = tweet.author.id
        send_data['contents'] = tweet.text
        send_data['created'] = tweet.created_at
        send_data['published'] = datetime.datetime.now()

        dictionary_copy = send_data.copy()
        end_data2.append(dictionary_copy)
    # for tweet in tweepy.Cursor(api.search, q='코로나', since='2020-08-31', until='2020-09-07').items(10):
    #     response = natural_language_understanding.analyze(
    #         text=tweet.text,
    #         features=Features(
    #             entities=EntitiesOptions(emotion=False),
    #             categories=EntitiesOptions(emotion=False, ),
    #             semantic_roles=EntitiesOptions(emotion=False, sentiment=False, ),
    #             keywords=KeywordsOptions(emotion=False, sentiment=False, )
    #         )
    #     ).get_result()
    #     print(tweet)

    #     for re in response['entities']:
    #         if re['type'] == "Location":
    #             send_data['location'] = re['text']
    #             #print(re['text'])
    #     #print("===============")
    #     #print(response)
    #     send_data['author'] = tweet.author.name
    #     send_data['title'] = tweet.author.id
    #     send_data['contents'] = tweet.text
    #     send_data['created'] = tweet.created_at
    #     send_data['published'] = datetime.datetime.now()
    #     for re1 in response['categories']:
    #         send_data['categorized'] = re1['label']
    #         send_data['score'] = re1['score']
    #     dictionary_copy = send_data.copy()
    #     end_data2.append(dictionary_copy)
    return end_data2


if __name__=='__main__':
    data1 = twitter_crwaler()
    for x in data1:
        Post(author=x['author'],location=x['location'],title=x['title'],contents=x['contents'],created_date=x['created'],
             published_date=x['published'],categorized_contents=x['categorized'],score=x['score']).save()

