import requests
import sys


def get_coordinates(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_size = tuple(toponym["boundedBy"]["Envelope"].values())
    toponym_size = (tuple(map(float, toponym_size[0].split())), tuple(map(float, toponym_size[1].split())))
    toponym_size = (abs(toponym_size[0][0] - toponym_size[1][0]), abs(toponym_size[0][1] - toponym_size[1][1]))
    toponym_size = ",".join(map(str, toponym_size))
    toponym_coodrinates = toponym["Point"]["pos"]
    return toponym_coodrinates.split(" ")
