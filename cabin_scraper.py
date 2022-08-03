import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import pandas as pd
import smtplib, ssl
import googlemaps
from datetime import datetime
from creds import *

locations = ['jihocesky-kraj', 'stredocesky-kraj', 'kralovehradecky-kraj', 'liberecky-kraj']


def scrape():
    global estate_list
    estate_dict = {}
    estate_list = []

    for location in locations:
        basic_url = f'https://reality.idnes.cz/s/domy/chata-chalupa/{location}/'
        number_of_pages_response = requests.get(basic_url)
        basic_soup = BeautifulSoup(number_of_pages_response.content, 'html.parser')

        try:
            no_of_pages = basic_soup.find(class_='mb-10 font-regular pull-left color-grey pt-3 pb-4').text.split()
            if len(no_of_pages) > 2:
                no_of_pages = int(no_of_pages[0] + no_of_pages[1])
                no_of_pages = round(no_of_pages / 20)

            else:
                no_of_pages = int(no_of_pages[0])
                no_of_pages = round(no_of_pages / 20)


        except Exception:
            print(f'does not exist in the database')

        # no_of_pages = basic_soup.find(class_='btn btn--border paging__item').next_element

        for pg in range(1, no_of_pages + 1):
            url = f'{basic_url}?page={pg}'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            estates = soup.find_all(class_='c-products__item')

            for estate in estates:

                try:
                    location = estate.find(class_='c-products__info').text.split()[-1]
                    raw_street = estate.find(class_='c-products__info').text.split()
                    street = " ".join(raw_street).replace("okres", "").replace("  ", " ")
                    name = estate.find(class_='c-products__info').text.split()
                    price = estate.find(class_='c-products__price').strong.text.replace(' ', '').replace('Kč', '')
                    price = int(price)
                    m2 = title = estate.find(class_='text-capitalize').next_sibling.split()

                    try:
                        if int(m2[-2]) > 10:
                            m2 = int(m2[-3] + m2[-2])
                        else:
                            m2 = int(m2[-2])
                    except IndexError:
                        print('chybulka')
                        pass

                    try:
                        price_m2 = int(price / m2)
                    except ZeroDivisionError:
                        ZeroDivisionError

                    except TypeError:
                        pass

                    link = estate.find('a').get('href')

                    estate_dict = {
                        # 'name': name,
                        'street': street,
                        'location': location,
                        'price': price,
                        'm2': m2,
                        'price_m2': price_m2,
                        'link': link
                    }

                    estate_list.append(estate_dict)

                except AttributeError:
                    pass

                except ValueError:
                    price = 0

    return estate_list


scrape()

df = pd.DataFrame(estate_list)

cities = df['street']
city_dist_hrs_list = []
city_dist_mns_list = []
total_dist_list = []
api_key = 'AIzaSyD4lC0jhE_qmasp4iuJBsHvwMNgXMjH57g'
gmaps = googlemaps.Client(key=api_key)
for c in cities:
    city_dist = gmaps.distance_matrix('Praha', c)['rows'][0]['elements'][0]
    # filtered_dist = city_dist['duration']['text'].split()[0]
    # new_list = filtered_dist <= 1
    city_dist = city_dist['duration']['text'].split()
    if (len(city_dist)) > 2:
        city_dist_hrs = int(city_dist[0])
        city_dist_mins = int(city_dist[-2])
        total_dist = int(city_dist_hrs) + (int(city_dist_mins) / 60)
        total_dist_list.append(total_dist)
        city_dist_hrs_list.append(city_dist_hrs)
        city_dist_mns_list.append(city_dist_mins)

    else:
        city_dist_hrs = int(0)
        city_dist_mins = int(city_dist[-2])
        total_dist = int(city_dist_hrs) + (int(city_dist_mins) / 60)
        city_dist_hrs_list.append(city_dist_hrs)
        city_dist_mns_list.append(city_dist_mins)
        total_dist_list.append(total_dist)

df['distance_hrs'] =  city_dist_hrs_list
df['distance_mins'] =  city_dist_mns_list
df['total_dist'] = total_dist_list

filtered_df = df.loc[(df['distance_hrs'] <= 1) & (df['price'] <= 4000000)]
filtered_df = filtered_df.sort_values(by=['price', 'price_m2', 'total_dist'], ascending=True)

plt.style.use('seaborn-whitegrid')
fig, axes = plt.subplots(1, 4, figsize=(18, 10), sharey=True)
plt.xticks(rotation=90)
plt.suptitle('Pozemkys Comparison, Filtered price < 40000000, Distance, Sorted by Price')

# Distance
sns.lineplot(ax=axes[0], x='total_dist', y='street', color='green', data=filtered_df)
axes[0].set_title('Distance')

# M2
sns.barplot(ax=axes[1], x='m2', y='street', palette='crest', data=filtered_df)
axes[1].set_title('m2')
plt.xlim(left=200)
plt.xlim(right=3800)

# Price
sns.barplot(ax=axes[2], x='price', y='street', palette='mako', data=filtered_df)
axes[2].set_title('Price')

# Price m2
sns.barplot(ax=axes[3], x='price_m2', y='street', palette="magma", data=filtered_df)
axes[3].set_title('Price_m2')
plt.xlim(left=200)
plt.xlim(right=6000)

#plt.ylim(5, 10)
import io

img_format = 'png'

f = io.BytesIO()
plt.savefig(f, format=img_format)
f.seek(0)

img_data = f.read()

sender = sender
password = password
recipient = "v.tetour@gmail.com, zuzanak36@gmail.com"

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def email_new(data):
    message = MIMEMultipart()
    message['Subject'] = "Chalupy Srovnani < 2 hrs"
    message['From'] = sender
    message['To'] = recipient

    now = datetime.now()

    body = f'Aktualni scraping: {now}'

    html = MIMEText(data.to_html(index=False), "html")

    msgImage = MIMEImage(img_data)

    message.attach(MIMEText(body, "plain"))
    message.attach(html)
    message.attach(msgImage)

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.outlook.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())

    print('sending was succesful')


def data_get():
    return filtered_df


if __name__ == '__main__':
    data = data_get()
    email_new(data)
