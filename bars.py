import json
from os import path
from math import radians, cos, sin, asin, sqrt


def load_bars_from_json(json_file_name):
    if not path.exists(json_file_name):
        return None
    with open(json_file_name, 'r', encoding='cp1251') as file_handler:
        json_file = json.load(file_handler)
    return json_file


def get_biggest_bar(bars):
    return max(bars, key=lambda max_key: max_key['SeatsCount'])


def get_smallest_bar(bars):
    return min(bars, key=lambda min_key: min_key['SeatsCount'])


def get_distance(longitude1, latitude1, longitude2, latitude2):
    radius_of_the_earth = 6371
    longitude1_in_radians, latitude1_in_radians, \
        longitude2_in_radians, latitude2_in_radians = map(
            radians, [longitude1, latitude1, longitude2, latitude2])
    subtracting_latitudes = latitude2_in_radians - latitude1_in_radians
    subtracting_longitudes = longitude2_in_radians - longitude1_in_radians
    distance = sin((subtracting_latitudes) / 2) ** 2 + \
        cos(latitude1_in_radians) * cos(latitude2_in_radians) * \
        sin((subtracting_longitudes) / 2) ** 2
    distance = 2 * asin(sqrt(distance))
    return distance * radius_of_the_earth


def get_closest_bar(bars, longitude, latitude):
    return min(bars, key=lambda x:
               get_distance(latitude, longitude,
                            x['geoData']['coordinates'][1],
                            x['geoData']['coordinates'][0]))


def get_string_bar(bar):
    string_bar = "{} с {} количеством посадочных мест по адресу {} \n \
широта: {}, долгота {}"
    return (string_bar.format(bar['Name'], bar["SeatsCount"], bar["Address"],
                              str(bar['geoData']['coordinates'][0]),
                              str(bar['geoData']['coordinates'][1])))


def input_user_coordinates():
    try:
        print("Поиск ближайшего бара:")
        longitude = float(input("Введите долготу: "))
        latitude = float(input("Введите широту: "))
        return longitude, latitude
    except ValueError:
        print("Ввод некорректен")
        return None


if __name__ == '__main__':
    print("Добро пожаловать!")
    json_file_name = input("Введите путь к json-файлу\n")
    bars = load_bars_from_json(json_file_name)
    if not bars:
        print("Файл не найден {}".format(json_file_name))
        exit()
    print("Самый большой бар : " + get_string_bar(get_biggest_bar(bars)))
    print("Самый маленький бар : " + get_string_bar(get_smallest_bar(bars)))
    user_coordinates = input_user_coordinates()
    if not user_coordinates:
        exit()
    closest_bar = get_closest_bar(bars, user_coordinates[0],
                                  user_coordinates[1])
    print("Ближайший бар :" + get_string_bar(closest_bar))
