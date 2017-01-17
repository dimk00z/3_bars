import json
import requests
import zipfile
from os import replace, remove, path
from math import radians, cos, sin, asin, sqrt


def download_bars_zip_from_opmosru(url, zip_file_name):
    req = requests.get(url)
    with open(zip_file_name, 'wb') as zip_file:
        for chunk in req.iter_content(100000):
            zip_file.write(chunk)
    if zip_file:
        return zip_file


def unzip_json(zip_file_name, json_file_name):
    if zipfile.is_zipfile(zip_file_name):
        zipfile.ZipFile(zip_file_name).extractall()
        replace(zipfile.ZipFile(zip_file_name).namelist()[0], json_file_name)
        remove(zip_file_name)
        return True


def load_json_from_file(filepath):
    if not path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='cp1251') as file_handler:
        return json.load(file_handler)


def load_bars_data_from_json(json_file_name):
    # try:
    json_file = load_json_from_file(json_file_name)
    bars = []
    for j_object in json_file:

        bars.append({'name': j_object['Name'],
                     'address': j_object['Address'],
                     'seats_count': j_object['SeatsCount'],
                     'longitude': j_object['geoData']['coordinates'][0],
                     'latitude': j_object['geoData']['coordinates'][1]
                     })

    return bars


def get_biggest_bar(bars):
    return max(bars, key=lambda d: d['seats_count'])


def get_smallest_bar(bars):
    return min(bars, key=lambda d: d['seats_count'])


def distance_between_points(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    result = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    result = 2 * asin(sqrt(result))
    earth_radius = 6371
    return result * earth_radius


def get_closest_bar(bars, longitude, latitude):
    distance = distance_between_points(longitude, latitude, bars[
                                       0]["longitude"], bars[0]["latitude"])
    closest_bar = bars[0]
    for bar in bars[1:]:
        distance_to_bar = distance_between_points(
            longitude, latitude, bar["longitude"], bar["latitude"])
        if distance_to_bar < distance:
            distance = distance_to_bar
            closest_bar = bar
    return closest_bar


def string_bar(bar):
    return (("{} с {} количеством посадочных мест по адресу {} \n" +
             "широта: {}, долгота {}").format(bar["name"],
                                              bar["seats_count"],
                                              bar["address"],
                                              str(bar["longitude"]),
                                              str(bar["latitude"])))


if __name__ == '__main__':
    print("Добро пожаловать!")
    print("Сейчас попробую загрузить бары с http://op.mos.ru")
    bars_zip = download_bars_zip_from_opmosru(
        'http://op.mos.ru/EHDWSREST/catalog/export/get?id=84505',
        "bars.zip")
    if bars_zip:
        unzip_json("bars.zip", "bars.json")
        bars_data = load_bars_data_from_json("bars.json")
        print(bars_data)
        if bars_data:
            biggest_bar = get_biggest_bar(bars_data)
            smallest_bar = get_smallest_bar(bars_data)
            print(biggest_bar)
            print("Самый большой бар : " + string_bar(biggest_bar))
            print("Самый мАленький бар : " + string_bar(smallest_bar))
            answer = ""
            while answer != "n":
                answer = input(
                    "Вы желаете узнать ближайший бар" +
                    " к заданным координатам? (y/n) :").lower()
                if answer == "y":
                    try:
                        longitude = float(input("Введите долготу: "))
                        latitude = float(input("Введите широту: "))
                        closest_bar = get_closest_bar(bars_data,
                                                      longitude, latitude)
                        print("Ближайший бар :" + string_bar(closest_bar))
                    except ValueError:
                        print("Возможно ввод некорректен")
    print("Много не пейте=)")
