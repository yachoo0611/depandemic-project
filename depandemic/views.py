from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


source_catch_lists = []
source_compare_lists = []
pattern = ""

source = ''
Content = {
    'keywords': {
        'text': [],
        'score': []
    },
    'entities': {
        'text': [],
        'score': []
    },
    'categories': {
        'text': [],
        'score': []
    },
}
semantic_roles = []


def index(request):
    #twieter 
    

    return render(request, 'depandemic/index.html')


def learn(request):

    try:
        authenticator = IAMAuthenticator('FZxffQMR704hKD0dgFXEC8T0L0FFkhWzNImrOWPG6ZVh')
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2019-07-12',
            authenticator=authenticator
        )
        natural_language_understanding.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

    except expression as identifier:
        print("Watson Api connection error!")

    textinput = request.POST.get('a')

    """Catch the code line!!!"""
    #input all languages functions/methods name here
    pattern = "getParameter"

    for i in sent_tokenize(textinput): 
        result_temp = KMPSearch(pattern, i)
        if result_temp is not None:
            source_catch_lists.append(result_temp)
    """Catch the code line!!! end"""


    response = natural_language_understanding.analyze(
        text=textinput,
        features=Features(
            entities=EntitiesOptions(
               emotion=False,
            ),
            categories=EntitiesOptions(
                emotion=False,
            ),
            semantic_roles=EntitiesOptions(
                emotion=False,
                sentiment=False,
            ),
            keywords=KeywordsOptions(
                emotion=False,
                sentiment=False,
            )
        )
    )

    re = response

    semantic_roles.append(json.dumps(re.result['semantic_roles'][0]['sentence']))
    for h in ['keywords','entities','categories']:
        for i in re.result[h]:
            try:
                try:
                    if (float(json.dumps(i['relevance'])) > 0.3):
                        Content[h]['text'].append(i['text'])
                        Content[h]['score'].append(i['relevance'])
                    else:
                        pass
                except:
                    if (float(json.dumps(i['relevance'])) > 0.3):
                        Content[h]['text'].append(i['label'])
                        Content[h]['score'].append(i['relevance'])
                    else:
                        pass
            except:
                try:
                    if (float(json.dumps(i['score'])) > 0.3):
                        Content[h]['text'].append(i['text'])
                        Content[h]['score'].append(i['score'])
                    else:
                        pass
                except:
                    if (float(json.dumps(i['score'])) > 0.3):
                        Content[h]['text'].append(i['label'])
                        Content[h]['score'].append(i['score'])
                    else:
                        pass

    count = Post.objects.count()
    count = count + 1
    post = Post(seq=count, keywords=Content['keywords']['text'][0], entities=Content['entities']['text'],
                categories=Content['categories']['text'],
                desc=semantic_roles[0].__str__().split('"'), source=source_catch_lists, method=pattern, etc='')
    post.save()
    print("saved!")
    reset(Content)
    cont = request.POST.get('a')
    return HttpResponse(source(cont))
