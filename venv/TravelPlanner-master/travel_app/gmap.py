#import pandas as pd, numpy as np
import requests
import json
import time
final_data = []
# Parameters
coordinates = ['-8.705833, 115.261377']
keywords = ['restaurant']
radius = '1000'
api_key = 'AIzaSyDF3scZqIFGSYQk__pXmgv1H0no97g2R64' #insert your Places API
for coordinate in coordinates:
    for keyword in keywords:
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+coordinate+'&radius='+str(radius)+'&keyword='+str(keyword)+'&key='+str(api_key)
        while True:
            print(url)
            respon = requests.get(url)
            jj = json.loads(respon.text)
            results = jj['results']
            for result in results:
                print(result)
                name = result['name']
                place_id = result ['place_id']
                lat = result['geometry']['location']['lat']
                lng = result['geometry']['location']['lng']
                rating = result['rating']
                types = result['types']
                vicinity = result['vicinity']
                #image=result['icon']
                #opening_hr=result['opening_hours']
                #photo=result['photos']
                data = [name, place_id, lat, lng, rating, types, vicinity]#,image,opening_hr,photo]
                final_data.append(data)
                time.sleep(5)
                if 'next_page_token' not in jj:
                    break
                else:
                    next_page_token = jj['next_page_token']
                url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+str(api_key)+'&pagetoken='+str(next_page_token)
                labels = ['Place Name','Place ID', 'Latitude', 'Longitude','rating', 'Types', 'Vicinity']#,'Image','Opening_hr','Photo']
                #export_dataframe_1_medium = pd.DataFrame.from_records(final_data, columns=labels)
                #with open('export_dataframe_1_medium.csv',mode='w'):
                    #export_dataframe_1_medium.to_csv('export_dataframe_1_medium.csv')
            