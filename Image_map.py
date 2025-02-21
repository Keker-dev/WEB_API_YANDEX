from io import BytesIO
import requests


def get_map(lat, lon, z):
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    map_params = {
        "ll": ",".join([lat, lon]),
        "z": z,
        "apikey": apikey,  # "pt": "{0},pm2dgl".format(f"{lat},{lon}"),
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        return
    return BytesIO(response.content)
