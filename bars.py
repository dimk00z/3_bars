import json
import requests
import zipfile
from os import replace,remove
from math import radians, cos, sin, asin, sqrt

class Bar(object):
    def __init__(self, Name, Adress, SeatsCount,Longitude,Latitude):
        self.Name = Name
        self.Adress = Adress
        self.SeatsCount = SeatsCount
        self.Latitude = Latitude
        self.Longitude = Longitude
Bars = []


def load_data():
    url = 'http://op.mos.ru/EHDWSREST/catalog/export/get?id=84505'
    #загружаем архив
    fileName = 'bars.zip'
    req = requests.get(url)
    file = open(fileName, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()
    bars = []
    if zipfile.is_zipfile('bars.zip'):
       zipfile.ZipFile('bars.zip').extractall()
       #в архиве один файл, распаковываем и переименовываем его
       replace(zipfile.ZipFile('bars.zip').namelist()[0],"bars.json")
       remove('bars.zip')
       json_file=json.loads(open("bars.json").read())
       for jObject in json_file:
           bar = Bar(jObject['Name'],jObject['Address'],jObject['SeatsCount'],
                      jObject['geoData']['coordinates'][0],
                      jObject['geoData']['coordinates'][1] )
           bars.append(bar)
    print("--------------------------------------")
    print("Загруженно " +str(len(bars)) +" баров!")
    return bars

def get_biggest_bar(bars):
    biggest_bar = bars[0]
    for bar in bars:
        if bar.SeatsCount > biggest_bar.SeatsCount:
            biggest_bar = bar
    return biggest_bar



def get_smallest_bar(bars):
    smallest_bar = bars[0]
    for bar in bars:
        if bar.SeatsCount<smallest_bar.SeatsCount:
            smallest_bar = bar
    return smallest_bar


def distance_between_points(lon1, lat1, lon2, lat2):
   # Формула "гаверсинуса"
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r

def get_closest_bar(bars, longitude, latitude):
    distance = distance_between_points(longitude,latitude,bars[0].Longitude,bars[0].Latitude)
    closest_bar = bars[0]
    for bar in bars[1:]:
        distance_to_bar=distance_between_points(longitude,latitude,bar.Longitude,bar.Latitude)
        if distance_to_bar<distance:
            distance = distance_to_bar
            closest_bar = bar
    return closest_bar

def main():
    print("Добро пожаловать!")
    print("Сейчас попробую загрузить бары с http://op.mos.ru")
    Bars = load_data()
    biggest_bar = get_biggest_bar(Bars)
    smallest_bar =get_smallest_bar(Bars)
    print()
    print("Самый большой бар : "+(biggest_bar.Name)+" c "+str(biggest_bar.SeatsCount)
           +" количеством посадочных мест"+ "по адресу: "+ biggest_bar.Adress)
    print("Самый мАленький бар : "+(smallest_bar.Name)+" c "+str(smallest_bar.SeatsCount)
           +" количеством посадочных мест"+ "по адресу: "+ smallest_bar.Adress)
    answer=""
    while answer!="n":
        answer=input("Вы желаете узнать ближайший бар к заданным координатам? (y/n) :" ).lower()
        if answer=="y":
            try:
                longitude = float(input("Введите долготу: "))
                latitude = float(input("Введите широту: "))
                closest_bar=get_closest_bar(Bars, longitude, latitude)
                print("Ближайший бар :"+closest_bar.Name+" по адресу: "+ closest_bar.Adress)
                print(str(closest_bar.Longitude)+" "+str(closest_bar.Latitude))
            except Exception:
                print("Возможно ввод некорректен")
    print("Много не пейте=)")

if __name__ == '__main__':
    main()
