import aiohttp_jinja2
import jinja2
from pathlib import Path

import requests as req
from bs4 import BeautifulSoup

import json

# own import
from views import *
from services.html_parser import myhtmlparser
import services.savingData as saving

here = Path(__file__).resolve().parent

htmlParser = myhtmlparser()


@aiohttp_jinja2.template('./views/home/home.html')
def home_handler(request):
    with open('./dataStorage/games/games.json', 'r') as read_file:
        data = json.load(read_file)
    print(data)

    links = []
    index = 0
    for i in data['games']:
        print(i['getfrom'])
        links.append(i['getfrom'])
        index += 1
        if(index >= 3):
            break

    hrefs = ['/titanfall2', '/stardewvalley', '/skyrim']

    return {
        'name': 'bogya',

        'link1': '/game'+links[0],
        'href1': '/game'+hrefs[0],
        
        'link2': '/game'+links[1],
        'href2': '/game'+hrefs[1],

        'link3': '/game'+links[2],
        'href3': '/game'+hrefs[2]
    }


@aiohttp_jinja2.template('./views/data/weather.html')
def weather_handler(request):
    res = req.get(
        'https://www.weather.com/weather/today/l/dd84dd441f663487afaade828274ccc19d18e3f7a14f1e3078a60f9693db4d36')

    # htmlParser.start(res.text)
    getpage_soup = BeautifulSoup(res.text, 'html.parser')

    all_class_topsection = getpage_soup.findAll(
        'span', {'data-testid': 'TemperatureValue', 'class': 'CurrentConditions--tempValue--3KcTQ'})
    tmp = tuple(all_class_topsection[0].string)
    temperatureF = ''
    for i in tmp:
        if(i.isdigit() == True):
            temperatureF += i
    temperatureC = float((int(temperatureF)-32) * float(5/9))

    town = getpage_soup.findAll(
        'h1', {'class': 'CurrentConditions--location--1Ayv3'})
    town_name = town[0].string

    return {'city': town_name, 'temperature': '{0}° F || {1}° C'.format(temperatureF, temperatureC)}


@aiohttp_jinja2.template('./views/data/send/game/game.json')
def response_json_game_data(request):
    with open('./dataStorage/games/games.json', 'r') as read_file:
        data = json.load(read_file)
    print(data)

    result = {
        'getfrom': '',
        'name': '',
        'url': '',
        'discription': '',
        'views': ''
    }

    for i in data['games']:
        # print(request.rel_url)
        # print(i['getfrom'])
        print(i)
        if(str(i['getfrom']) == str(request.rel_url)):
            result['getfrom'] = i['getfrom']
            result['name'] = i['name']
            result['url'] = i['url']
            result['discription'] = i['discription']
            result['views'] = i['views']
            break

    # print(result)
    return {
        'getfrom': result['getfrom'],
        'name': result['name'],
        'url': result['url'],
        'discription': result['discription'],
        'views': result['views']
    }


@aiohttp_jinja2.template('./views/data/send/game/game_many.json')
def response_many_json_data(request):

    print(request.rel_url.query['name'])
    with open('./dataStorage/games/games.json', 'r') as read_file:
        data = json.load(read_file)
    # print(data)

    res_full = []

    result = {
        'getfrom': '',
        'name': '',
        'url': '',
        'discription': '',
        'views': ''
    }

    for i in data['games']:
        print(i['url'])
        if(i['url']):
            result['getfrom'] = i['getfrom']
            result['name'] = i['name']
            result['url'] = i['url']
            result['discription'] = i['discription']
            result['views'] = i['views']

            res_full.append(result)
            break

    print(res_full)

    with open('./views/data/send/game/game_many.json', 'w', encoding='utf-8') as f:
        json.dump(res_full, f, ensure_ascii=False, indent=4)

    # return {'result': json_res}
    return {}
    # return json_res


def response_file(request):

    return


@aiohttp_jinja2.template('./views/response/result.json')
def storage_weather(request):
    print('begin')
    res = req.get(
        'https://www.weather.com/weather/today/l/dd84dd441f663487afaade828274ccc19d18e3f7a14f1e3078a60f9693db4d36')

    # htmlParser.start(res.text)
    getpage_soup = BeautifulSoup(res.text, 'html.parser')

    all_class_topsection = getpage_soup.findAll(
        'span', {'data-testid': 'TemperatureValue', 'class': 'CurrentConditions--tempValue--3KcTQ'})
    tmp = tuple(all_class_topsection[0].string)
    temperatureF = ''
    for i in tmp:
        if(i.isdigit() == True):
            temperatureF += i
    temperatureC = float((int(temperatureF)-32) * float(5/9))

    town = getpage_soup.findAll(
        'h1', {'class': 'CurrentConditions--location--1Ayv3'})
    town_name = town[0].string

    saving.saveWeather(str(town_name), str(temperatureF))

    print('success')
    return {'result': 'done'}


def setup_routes(app):
    # app.router.add_get('/', index)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(here)))

    app.router.add_get('/', home_handler)

    app.router.add_get('/weather', weather_handler)

    app.router.add_get('/game/{name}', response_json_game_data)

    app.router.add_get('/game', response_many_json_data)

    app.router.add_get('/download/{name}', response_file)

    app.router.add_get('/accumulation/weather', storage_weather)
