import json
import requests
import zipfile
from os import replace, remove
from math import radians, cos, sin, asin, sqrt


class BarClass(object):

    def __init__(self, name, adress, seats_count, longitude, latitude):
        self.name = name
        self.adress = adress
        self.seats_count = seats_count
        self.latitude = latitude
        self.longitude = longitude


def download_bars_zip_from_opmosru(url, zip_file_name):
    req = requests.get(url)
    file_bars = open(zip_file_name, 'wb')
    for chunk in req.iter_content(100000):
        file_bars.write(chunk)
    file_bars.close()
    if file_bars:
        return file_bars


def unzip_json(zip_file_name, json_file_name):
    if zipfile.is_zipfile(zip_file_name):
        zipfile.ZipFile(zip_file_name).extractall()
        # в архиве один файл, распаковываем и переименовываем его
        replace(zipfile.ZipFile(zip_file_name).namelist()[0], json_file_name)
        remove(zip_file_name)
        return True


def load_bars_data_from_json(json_file_name):
    bars = []
    try:
        json_file = json.loads(open(json_file_name).read())
        for j_object in json_file:
            bar = BarClass(j_object['Name'], j_object['Address'],
                           j_object['SeatsCount'],
                           j_object['geoData']['coordinates'][0],
                           j_object['geoData']['coordinates'][1])
            bars.append(bar)
        return bars
    except ValueError:
        return None


def get_biggest_bar(bars):
    biggest_bar = bars[0]
    for bar in bars:
        if bar.seats_count > biggest_bar.seats_count:
            biggest_bar = bar
    return biggest_bar


def get_smallest_bar(bars):
    smallest_bar = bars[0]
    for bar in bars:
        if bar.seats_count < smallest_bar.seats_count:
            smallest_bar = bar
    return smallest_bar


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
                                       0].longitude, bars[0].latitude)
    closest_bar = bars[0]
    for bar in bars[1:]:
        distance_to_bar = distance_between_points(
            longitude, latitude, bar.longitude, bar.latitude)
        if distance_to_bar < distance:
            distance = distance_to_bar
            closest_bar = bar
    return closest_bar

if __name__ == '__main__':
    print("Добро пожаловать!")
    print("Сейчас попробую загрузить бары с http://op.mos.ru")
    bars_zip = download_bars_zip_from_opmosru(
        'http://op.mos.ru/EHDWSREST/catalog/export/get?id=84505',
        "bars.zip")
    if bars_zip:
        unzip_json("bars.zip", "bars.json")
        bars_data = load_bars_data_from_json("bars.json")
        if bars_data:
            biggest_bar = get_biggest_bar(bars_data)
            smallest_bar = get_smallest_bar(bars_data)
            print()
            print("Самый большой бар : " + (biggest_bar.name) + " c " +
                  str(biggest_bar.seats_count) +
                  " количеством посадочных мест" +
                  "по адресу: " + biggest_bar.adress)
            print("Самый мАленький бар : " + (smallest_bar.name) + " c " +
                  str(smallest_bar.seats_count) +
                  " количеством посадочных мест" +
                  "по адресу: " + smallest_bar.adress)
            answer = ""
            while answer != "n":
                answer = input(
                    "Вы желаете узнать ближайший бар" +
                    " к заданным координатам? (y/n) :").lower()
                if answer == "y":
                    try:
                        longitude = float(input("Введите долготу: "))
                        latitude = float(input("Введите широту: "))
                        closest_bar = get_closest_bar(
                            bars_data, longitude, latitude)
                        print("Ближайший бар :" + closest_bar.name +
                              " по адресу: " + closest_bar.adress)
                        print(str(closest_bar.longitude) +
                              " " + str(closest_bar.latitude))
                    except Exception:
                        print("Возможно ввод некорректен")
    print("Много не пейте=)")
