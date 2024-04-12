import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import User
from .algo import Nowcasting, Crawler
import tushare as ts
import requests
from datetime import datetime, timedelta


def entrance(request):
    if request.method == "GET":
        return render(request, 'explorer/login.html')


def login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            json_data = json.dumps({
                'response': "No"
            })
            return HttpResponse(json_data, content_type='application/json')
        json_data = json.dumps({
            'response': "OK",
            'ID': user.UserID,
            'name': user.Username
        })
        return HttpResponse(json_data, content_type='application/json')
    else:
        return HttpResponse("Bad request!")


def register(request):
    if request.method == "GET":
        return render(request, 'explorer/register.html')


def regist(request):
    if request.method == "POST":
        register_data = json.loads(request.body.decode('utf-8'))
        username = register_data.get('username')
        email = register_data.get('email')
        password = register_data.get('password')
        try:
            new_user = User(Username=username, password=password, email=email)
            new_user.save()
        except:
            json_data = json.dumps({
                'response': "No"
            })
            return HttpResponse(json_data, content_type='application/json')
        json_data = json.dumps({
            'response': "OK",
        })
        return HttpResponse(json_data, content_type='application/json')
    else:
        return HttpResponse("Bad request!")


def forgot(requests):
    return render(requests, "explorer/forgot-password.html")


def index(request):
    if request.method == "GET":
        # %% Hot news
        # try:
        #     scrape = Crawler()
        #     hot_news = scrape.get_latest_news(time=0, limit=2)
        #     news_ = {
        #         "title1": str(hot_news.loc[0, 'Title']),
        #         "content1": str(hot_news.loc[0, 'Summary']),
        #         "url1": str(hot_news.loc[0, 'URL']),
        #         "title2": str(hot_news.loc[1, 'Title']),
        #         "content2": str(hot_news.loc[1, 'Summary']),
        #         "url2": str(hot_news.loc[1, 'URL']),
        #     }
        # except:   # get last scrape news from data
        #     try:
        #         scrape = Crawler()
        #         hot_news = scrape.get_latest_news(time=1, limit=2)
        #         news_ = {
        #             "title1": str(hot_news.loc[0, 'Title']),
        #             "content1": str(hot_news.loc[0, 'Summary']),
        #             "url1": str(hot_news.loc[0, 'URL']),
        #             "title2": str(hot_news.loc[1, 'Title']),
        #             "content2": str(hot_news.loc[1, 'Summary']),
        #             "url2": str(hot_news.loc[1, 'URL']),
        #         }
        #     except:
        #         news_ = {
        #             "title1": "China's Shenzhou 16 astronauts hand over Tiangong space station to new crew",
        #             "content1": "China's space station has new occupants in charge.The departing Shenzhou 16 astronauts handed over control of the Tiangong space station to the newly arrived Shenzhou 17 crew during a short ceremony on Sunday (Oct. 29). On behalf of the Shenzhou 16 crew, I formally and solemnly hand over [the key] to the commander of the Shenzhou 17 mission, said Jing Haipeng, commander of the Shenzhou 16 mission.",
        #             "url1": "https://www.msn.com/en-us/news/world/china-s-shenzhou-16-astronauts-hand-over-tiangong-space-station-to-new-crew-video/ar-AA1jaJ0L?ocid=msedgntp&pc=CNNDDB&cvid=59bc87e896f84666b5be31891f9ad3a9&ei=19",
        #             "title2": "Russia Responds to Proposal for UN Alternative",
        #             "content2": "In an article to coincide with the Turkish government marking the 100th anniversary of the creation of the modern republic, Altun said Turkey is preparing to create a new international structure. The spokesman said this is because the UN Security Council",
        #             "url2": "https://www.msn.com/en-us/news/world/russia-responds-to-proposal-for-un-alternative/ar-AA1j9rds?ocid=msedgntp&pc=CNNDDB&cvid=59bc87e896f84666b5be31891f9ad3a9&ei=25"
        #         }

        news_ = {
            "title1": "China's Shenzhou 16 astronauts",
            "content1": "China's space station has new occupants in charge.The departing Shenzhou 16 astronauts handed over control of the Tiangong space station to the newly arrived Shenzhou 17 crew during a short ceremony on Sunday (Oct. 29).",
            "url1": "https://www.msn.com/en-us/news/world/china-s-shenzhou-16-astronauts-hand-over-tiangong-space-station-to-new-crew-video/ar-AA1jaJ0L?ocid=msedgntp&pc=CNNDDB&cvid=59bc87e896f84666b5be31891f9ad3a9&ei=19",
            "title2": "Russia Responds to Proposal for UN Alternative",
            "content2": "In an article to coincide with the Turkish government marking the 100th anniversary of the creation of the modern republic, Altun said Turkey is preparing to create a new international structure. ",
            "url2": "https://www.msn.com/en-us/news/world/russia-responds-to-proposal-for-un-alternative/ar-AA1j9rds?ocid=msedgntp&pc=CNNDDB&cvid=59bc87e896f84666b5be31891f9ad3a9&ei=25"
        }

        # %% index
        now = datetime.now()
        current_date = datetime.now()
        current_date_str = current_date.strftime("%Y%m%d")
        one_day_ago = current_date - timedelta(days=1)
        one_day_ago_str = one_day_ago.strftime("%Y%m%d")
        try:
            index_data_ = pd.read_csv("index_data.csv")
        except:
            ts.set_token('f75ac7a71ba8bf7118966e7fb1a0224dda2345fa0f54d1f7b010b91b')
            pro = ts.pro_api()
            index_data_ = pro.index_global(start_date=one_day_ago_str, end_date=current_date_str)
            index_data_.to_csv("index_data.csv")
        def get_index(name):
            sp500_data = index_data_[index_data_['ts_code'] == name].reset_index(drop=True)
            close_ = float(sp500_data['close'])
            change = float(sp500_data['change'])
            pct_chg = float(sp500_data['pct_chg'])
            if pct_chg >= 0:
                d1 = "text-danger"
                d2 = "fa fa-angle-up ml-5"
            else:
                d1 = "text-success"
                d2 = "fa fa-angle-down ml-5"
                pct_chg = -pct_chg

            tick_prepare = {
                'change': change,
                'value': close_,
                'pct_chang': pct_chg,
                "direction1": d1,
                'direction2': d2
            }
            return tick_prepare
        index_ = {
            'SP500': get_index("SPX"),
            'Dow': get_index("DJI"),
            'NASDAQ': get_index("IXIC"),
            'Nikkei': get_index("N225"),
            'RTS': get_index("RTS"),
            'SENSEX': get_index("SENSEX"),
            'FTSE': get_index("FTSE"),
        }

        # %% Macro
        factors = Nowcasting()
        now_ = factors.get_data()
        time_series = pd.to_datetime(now_['Time'], format="%b-%y")
        time_s = list(time_series.dt.strftime('%Y-%m'))
        growth = list(now_['growth'])
        growth = [round(x, 2) for x in growth]
        Economy = list(now_['Economy'])
        Economy = [round(x, 2) for x in Economy]
        Mood = list(now_['Mood'])
        Mood = [round(x, 2) for x in Mood]
        Price = list(now_['Price'])
        Price = [round(x, 2) for x in Price]
        Finance = list(now_['Price'])
        Finance = [round(x, 2) for x in Finance]
        macro_data = {
            'GDP_value': 233,
            'time_d': time_s,
            'grow_d': growth,
            'econ_d': Economy,
            'Mood_d': Mood,
            'p_d': Price,
            'f_d': Finance
        }
        return render(request, "explorer/index.html", {'news': news_, 'index': index_, 'macro': macro_data})


def settings(request):
    return render(request, "explorer/user-edit.html")


def chat(request):
    return render(request, "explorer/chat.html")


def chatterbot(request):
    data = json.loads(request.body.decode('utf-8'))
    content = data.get('content')
    # 请求头部信息
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }
    messages = [
        {"role": "user", "content": content},
    ]

    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0
    }
    url = 'https://api.openai.com/v1/chat/completions'
    response = requests.post(url=url, headers=headers, json=data, verify=False)
    response_data = response.json()
    json_data = json.dumps({
        'response': "OK",
        'content': response_data['choices'][0]['message']['content']
    })
    return HttpResponse(json_data, content_type='application/json')


def timeline(request):
    return render(request, "explorer/timeline.html")


def Analysis(request):
    return render(request, "explorer/ecommerce.html")


def json_data(request):
    with open('./relation.json', 'r') as file:
        json_data = json.load(file)
    return JsonResponse(json_data)


def perspective(request):
    return render(request, "explorer/blog-detail.html")


def inference(request):
    return render(request, "explorer/blog.html")


def portfolio(request):
    return render(request, "explorer/myportfolio.html")

