import json
import requests
import zipfile
from os import replace, remove, path
from math import radians, cos, sin, asin, sqrt

EARTH_RADIUS = 6371


def load_bars_data_from_json(json_file_name):
    if not path.exists(json_file_name):
        return None
    with open(json_file_name, 'r', encoding='cp1251') as file_handler:
        json_file = json.load(file_handler)
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
    return max(bars, key=lambda max_key: max_key['seats_count'])


def get_smallest_bar(bars):
    return min(bars, key=lambda min_key: min_key['seats_count'])


def distance_between_points(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    sub_result = sin(dlat / 2) ** 2 + cos(lat1) * \
        cos(lat2) * sin(dlon / 2) ** 2
    sub_result = 2 * asin(sqrt(sub_result))
    return sub_result * EARTH_RADIUS


def get_closest_bar(bars, longitude, latitude):
    distance = distance_between_points(longitude,
                                       latitude,
                                       bars[0]["longitude"],
                                       bars[0]["latitude"])
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
    bars = load_bars_data_from_json(input("Введите путь к json-файлу\n"))
    if bars:
        print("Самый большой бар : " + string_bar(get_biggest_bar(bars)))
        print("Самый маленький бар : " + string_bar(get_smallest_bar(bars)))
        answer = ""
        while answer != "n":
            answer = input(
                "Вы желаете узнать ближайший бар \
к заданным координатам? (y/n) :").lower()
            if answer == "y":
                try:
                    longitude = float(input("Введите долготу: "))
                    latitude = float(input("Введите широту: "))
                    closest_bar = get_closest_bar(bars,
                                                  longitude, latitude)
                    print("Ближайший бар :" + string_bar(closest_bar))
                except ValueError:
                    print("Ввод некорректен")
        else:
            print("Файл не найден")
