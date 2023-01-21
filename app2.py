import streamlit as st
import pandas as pd
import requests 
import sqlalchemy as db
#import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import branca
#import os
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import streamlit as st

import logging

import numpy as np
from PIL import Image

#logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

options_form2 = st.sidebar.form('options_form2')
option2 = options_form2.radio('Моля изберете къде живеете', ('Сливен', 'Гергевец', 'Камен', 'Крушаре', 'Сотиря', 'Чинтулово'))

def choose_string(option2):
    if option2 == 'Сливен':
        return '1MnLgg3IPC9ImxAc4URmzj4ST_qhg19Xy'
    elif option2 == 'Гергевец':
        return '1ZLqv9Aq14xMK7bn7NP7eK6T1FyfoI4DT'
    elif option2 == 'Камен':
        return '1VJSQSJL5ElijRtNNyYedM0ziHejIzwXm'
    elif option2 == 'Крушаре':
        return '1sJJYT3b2uEFHMIfKikNvhk2q0ZA-mR7E'
    elif option2 == 'Сотиря':
        return '1-Z7dfUaCd4VqHoUUpswohFLwS3Gk379h'
    elif option2 == 'Чинтулово':
        return '1hO7AXY3NfNzT5V6gkJVz9sDl5W3nfmj_'
    
my_drive = choose_string(option2)

# To list all files in your google drive at the root folder
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(my_drive)}).GetList()









img_file_buffer = options_form2.camera_input("Снимай")

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Check the type of img_array:
    # Should output: <class 'numpy.ndarray'>
    name = options_form2.text_input('Въведете име на снимката')
    im = Image.fromarray(img_array)
    button2 = options_form2.form_submit_button('Зареди снимката')
    if button2 and name is not None:
 
        im.save(f"{name}.png")
        image_string = f'{name}.png'
        gfile = drive.CreateFile({'parents': [{'id': my_drive}]})
        gfile.SetContentFile(image_string)
        gfile.Upload()
        options_form2.write('Снимката беше успешно заредена!')
options_form2.form_submit_button("Потвърди")

web_links = []
title = []

for file in file_list:
    url = f"https://drive.google.com/uc?export=view&id={file['id']}"
    web_links.append(url)
    title.append(file['title'])

my_dict = {
    'url': web_links,
    'title': title
}

data = pd.DataFrame(my_dict)

thumbnails = []
for index,row in data.iterrows():
    s = row['url']
    thumbnail_url = f"<img src='{s}' width='100px'>"
    thumbnails.append(thumbnail_url)
    
data['thumbnail'] = thumbnails

html = ''
for t in data['thumbnail']:
    html += t


    

engine = create_engine(
    "shillelagh://",
     adapters=["gsheetsapi"],
     adapter_kwargs={
         "gsheetsapi": {
             "service_account_info": {
                 "type": "service_account",
                 "project_id": "hidden-will-368520",
                 "private_key_id": "e0858ae3051e13ab0fa8a2d89e1eecd8a7eebe8b",
                 "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCq94AuGOXhE3lf\nrGEJCIGITC03umixgwKizmOkBSsLzmthnKSzGLFBih2YyYtHtVp3reYOY1qXyngS\nNjGLNN1E9LfauBSULuz/E1QyCEb0/avEN/uRG3QpsCu+zlvR8uYgY2t4uNLQ0rmI\n3JZATCgPUEUdaJ1LL7ouF6aOIwoKCNWtqhB3jUqdXDrlbmKLG9H6mnfTCtem4OUz\n1v1acxfwqo2MAMnixNIYPTO+ByiTecFkHBhTQ/LN76fxLfJRtgZjTS0w1fLkp6MH\nLXkBlH/2wPsL0diok8YEG6jNEwbjJ6eZ+9yEba3e+eIbp2SW4kTQsgNedFgwSNIS\n+zdN4/CVAgMBAAECggEABALl8ARHiH4OJU+Ea1OBbog9sLFf+XeVx+odw7XB/8yV\nD7zpebDvn8EKLBE2gl/f7S+YVpLAMmWJZwFR15lNmRZA0LyW8a8e17vwCB3SRGHw\noMb2Jmka0vY+NdjeUKZpUy3h/KV21M13lZ16AleHF8I4t5WXyIbTJc0KQbV9a896\nwy2T0FqjSRO+UJlgYK3HdzNNcukN9kAq1f0fZNwBEMXdUVMQiQCi9VJIDX9SpqzM\n2x8CJTPF5AKWWym0OHt5EJVffcjjf/M0+Ys7O4Ak4JNpsO7g7jAyrMssbn/4NhzC\n2zkxcM9bAuX8640hPkafJManfZwEaMr8S3Mug7A9oQKBgQDaRzP4+NvtiZpdE3Y6\n2MZC98y0mfEzF+P4Vq7kl5djZKs8xEesBMUbVBd7jeARAdK1K88gJ7SLsXAzcMx4\n9CPumDQZ/47uHMD5UyoaqGK9OGRRWIkc68BzQss6UF97Rj6kqggEktfUoT2tcY8o\nTudbSI3d4dHc7xkW8NWGtul0iQKBgQDIgzTxDEwWz+G2B0vYjRIblYQ78gmucP+9\nuOzRyR5P6lnebaViOe0S83HoZRaV0jq+UUvQrYs5pCjusDUuMZ0oC0nl/jbEREJo\nwnaPAcgzgFNLlAA5QcVcd90TJAIswfxUPZUO0/wZy6MKgloIGn8WeOnjLnfboEuT\nNxnDpXKwrQKBgQDJKlwEtd2CgpGn/Bq3SzcVWujm/QUlEHyCT+kpNWhJKusBuudO\n6qp5cDugG/YH1oVJgRGH0e/72lDMp8VaJ67B4rYJy9P/MLLMVU/1d4BgYQtbSNw8\nsi0QTNudZ5tHskpjWWzAQlD1XpDIO2MzQ9zG7QwKFGdkVVrrIJO5bvOi+QKBgF5t\n7DDZKbxUime/Z+jEBxMWhv/0LLsKXGZtAJqLrMrWAxzNZmWsAgo6vBpGASztpNyc\nTKgqErdCqERAl8r5cpm5N0QpRIGJ4/ySGGOg4zfd51xghvpwDxJNIMAy5RNPCBZk\nKh6hlshPLql0WhIW6GMc7okfCTNVekIKYQfSkwDBAoGAOpE8LY+sBOifg6xjl5ua\nj1l658V4tPOROJ14KjswHS3p4wLxlH7/rj1O7BvJnjQB+oFQPVLuUMHga3oGO4Sl\nP/GIpsgfIBOLenSoEx5nTKCvoiKQK/JH4AurKgKwTY3H5xR9ho5sa/zBsMBryzzB\nT364lLAwBWbVwf6Z7nzj7NM=\n-----END PRIVATE KEY-----\n",
                 "client_email": "drerrrr@hidden-will-368520.iam.gserviceaccount.com",
                 "client_id": "112223709029329197118",
                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                 "token_uri": "https://oauth2.googleapis.com/token",
                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                 "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/drerrrr%40hidden-will-368520.iam.gserviceaccount.com"
            },
             "catalog":
             {
                 "Interactive_class": "https://docs.google.com/spreadsheets/d/12f3o40DyzQpMo2wkbAxqldaA_HI81gk8Md0kJmyN_HE/edit#gid=1747533781"
             }
         },
     },
)

st.title('Интерактивна карта')
st.markdown('Това е вашият интерактивен час')

address = st.text_input('Местоположение: ')

option1 = st.radio('Моля изберете една от следните опции', ('Снимки', 'Графика'))

base = declarative_base()
class My_object(base):
    __tablename__ = 'Interactive_class'
    #id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    address = Column(String)
    temperature = Column(Integer)
    date = Column(String)


mine = sessionmaker(bind=engine)
session = mine()

df = pd.read_sql_query(sql = db.select([My_object.name, My_object.address, My_object.temperature, My_object.date,
                                        ]), con=engine)

def convert_data(df):
    l = []
    for column in df:
        if column == 'address':
            for value in df[column].values:
                if ' ' in value:
                    value = value.replace(' ', '')
                    l.append(value)
                else:
                    l.append(value)
    l1 = []        
    for value in l:
        if 'С.' in value:
            value = value.replace('С.', '')
            l1.append(value)
        else:
            l1.append(value)
        
    df['address'] = l1
    return df
df = convert_data(df)


ORS_API_KEY = st.secrets['ORS_API_KEY']

def geocode(query):
    parameters = {'api_key': ORS_API_KEY, 'text': query}

    response = requests.get('https://api.openrouteservice.org/geocode/search', params=parameters)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            x, y = data['features'][0]['geometry']['coordinates']
            return (y, x)

location = geocode(address)
select_address = df[df['address'].isin([address])]

hoover_text = []
for index, row in select_address.iterrows():
    hoover_text.append(('<b>{address}</b><br><br>'+
                       'Температура: {temperatura}<br>'+
                       'Дaта: {date}<br>'+
                       'Име: {name}<br>').format(address=row['address'],
                                                 temperatura=row['temperature'],
                                                 date=row['date'],
                                                 name=row['name']))
select_address['text'] = hoover_text


def make_plot(m):
    fig1=make_subplots()

    fig1.add_trace(
        go.Scatter(
            x=m['date'],
            y=m['temperature'],
            name="Измерена температура",
            #mode='lines',
            #color = m['name'],
            #symbol = m['name'],
            text=m['text'],               
            hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
            line = dict(color='firebrick', width=3)                 #Hide the hoverinfo
              ),
    
        )
        #secondary_y=False               #The bar chart uses the primary y-axis (left)
    
    fig1.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light gray
             title_text="Измерена температура на зададеното местоположение", #Add a chart title
             title_font_family="Times New Roman",
             title_font_size = 20,
             title_font_color="darkblue", #Specify font color of the title
             title_x=0.5, #Specify the title position
             xaxis=dict(
                    tickfont_size=10,
                    tickangle = 45,
                    showgrid = True,
                    zeroline = True,
                    showline = True,
                    showticklabels = True,
                    #dtick="M1", #Change the x-axis ticks to be monthly
                    #tickformat='%d %B %Y' # (%a)<br>
                    title = 'Дата',
                    titlefont = dict(
                     family = 'Arial, sans-serif',
                     size = 18),
                
                    tickfont = dict(
                     family = 'Old Standard TT, serif',
                     size = 14,
                     color = 'black'),
                    tickmode = 'array',
                    tickvals = m['date'],
                    ticktext = [d.strftime('%d-%m-%Y') for d in m['date'].values]
                    ),
             legend = dict(orientation = 'h', xanchor = "center", x = 0.72, y= 1), #Adjust legend position
             #yaxis_title='Измерена температура',
             yaxis = dict(
                 showgrid = True,
                 zeroline = True,
                 showline = True,
                 gridcolor = '#bdbdbd',
                 gridwidth = 2,
                 zerolinecolor = '#969696',
                 zerolinewidth = 2,
                 linecolor = '#636363',
                 linewidth = 2,
                 title = 'Измерена температура',
                 titlefont = dict(
                     family = 'Arial, sans-serif',
                     size = 18,
                     color = 'lightgrey'),
                 showticklabels = True,
                 #tickangle = 45,
                 tickfont = dict(
                     family = 'Old Standard TT, serif',
                     size = 14,
                     color = 'black'),
                 tickmode = 'linear',
                 tick0 = 0,
                 dtick = 1
   )
             )

    return fig1
legend_dict = {
    'Tree cover': '006400',
    'Shrubland': 'ffbb22',
    'Grassland': 'ffff4c',
    'Cropland': 'f096ff',
    'Built-up': 'fa0000',
    'Bare, sparse vegetation ': 'b4b4b4',
    'Snow and ice': 'f0f0f0',
    'Permanent water bodies': '0064c8',
    'Herbaceous wetland': '0096a0',
    'Mangroves': '00cf75',
    'Moss and lichen': 'fae6a0'
}

result = []
if address:
    results = geocode(address)
    result.append(results)
    if results:
        st.write('Geocoded Coordinates: {}, {}'.format(results[0], results[1]))
        
        m = leafmap.Map(location=results, layers_control=True, draw_control=False, measure_control=True, fullscreen_control=True, zoom=10)
        m.add_wms_layer(url = "https://services.terrascope.be/wms/v2", layers = "WORLDCOVER_2020_MAP", name = "ESA Worldcover 2020", format = "image/png", shown=True)
        m.add_legend(title='NLCD Land Cover Classification', legend_dict=legend_dict)
        if option1 == 'Графика':
            fig = make_plot(select_address)
            #fig.write_html('fig'+str(1)+".html") 
            #n = 'fig2.html'
            #html="""<iframe src=\"""" + str(n) + """\" width="850" height="400"  frameborder="0">"""
            #popup = leafmap.folium.Popup(leafmap.folium.Html(html, script=True))
            st.plotly_chart(fig, use_container_width=True)
            m.add_marker(location=results, popup=address)
        if option1 == 'Снимки':
            iframe = leafmap.folium.IFrame(html=html, width=500, height=300)
            popup = leafmap.folium.Popup(iframe, max_width=2650)
            m.add_marker(location=results, popup=popup)
        m_streamlit = m.to_streamlit(800, 800)
    else:
        st.error('Request failed. No results.')

options_form = st.sidebar.form('options_form')
name1 = options_form.text_input('Име')
address1 = options_form.text_input('Адрес')
temperature1 = options_form.number_input('Температура', min_value=-20.0, max_value=40.0, step=1.0)
date1 = options_form.date_input('Дата')

add_data = options_form.form_submit_button('Потвърди')

if add_data:
    new_rec = My_object(name=name1, address=address1, temperature=temperature1, date=date1)
    session.add(new_rec)
    session.commit()
    options_form.write('Успешно заредихте данните. Благодаря!')
    
