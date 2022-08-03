import requests
from bs4 import BeautifulSoup
import json

car_logos = {}

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'} 
url = 'https://www.carlogos.org/car-brands/'

for i in range(1,9):
    if i == 1:
        results = requests.get(url, headers=headers)
    else:
        results = requests.get(url + f'page-{i}.html', headers=headers)

    soup = BeautifulSoup(results.text, 'html.parser')
    ul = soup.find('ul', class_ = 'logo-list')
    ul = ul.find_all("a")
    for li in ul:
        link = li.get("href")
        carts = requests.get('https://www.carlogos.org' + link, headers=headers)
        carts_source = BeautifulSoup(carts.text, 'html.parser')


        info = carts_source.find('div', class_='content')
        if carts_source.find('div', class_='content') is None:
            info2 = carts_source.find('div', class_='overview')
            p = info2.find_all('p')
            about_brand = {}

            for i in range(len(p)):
                if p[i].text.split()[0] in ['Founded:','Founder:','Owner:','Subsidiaries:','Headquarters:']:
                    about_brand[p[i].text.split()[0]] = ' '.join(p[i].text.split()[1:])
                if ' '.join(p[i].text.split()[0:2]) == 'Official Site:':
                    site_url = str(p[i].find('a').get('href'))
                    if site_url.startswith('https:') == True:
                        about_brand[' '.join(p[i].text.split()[0:2])] = p[i].find('a').get('href')
                    else:
                        about_brand[' '.join(p[i].text.split()[0:2])] = 'https:' + p[i].find('a').get('href')
            

                else:
                    continue
            about_brand['Overview'] = (carts_source.find('div', class_='info')).find('p').text.replace('\n','')
            logo_link = carts_source.find('p', class_ ='shadow')

            about_brand['Present Logo'] = 'https://www.carlogos.org' + logo_link.find('a').get('href')
            name = carts_source.find('div', class_ = 'title')
            car_logos[name.find('h1').text.replace('Logo', '')] = about_brand

        else:
            table = info.find('table')
            table_row = table.find_all('td')
            about_brand = {}

            logo_link2 = info.find('p')
            about_brand['Present Logo'] = 'https://www.carlogos.org' + logo_link2.find('img')['src']

            for i in range(len(table.find_all('td'))):
                if table_row[i].text in ['Founded','Owner','Markets','Name','Type','Slogan',
                'History','Headquarters','Parent']:
                    about_brand[table_row[i].text] = table_row[i+1].text
         
                if table_row[i].text == 'Official Site':
                    site_url2 = table_row[i+1].find('a').get('href')

                    if site_url2.startswith('https:') == True:
                        about_brand[table_row[i].text] = table_row[i+1].find('a').get('href')
                    else:
                        about_brand[table_row[i].text] = 'https:' + table_row[i+1].find('a').get('href') 
                    
                if table_row[i].text == 'Overview':
                    about_brand[table_row[i].text] = table_row[i+1].text.replace('\n','')
                else:
                    continue
            car_logos[table.find('th').text.split()[0]] = about_brand


with open("carlogos_file.json", "w", encoding='utf-16') as file:
    json.dump(car_logos, file, indent=4, ensure_ascii=False)

 