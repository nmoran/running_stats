#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 22:43:30 2017

Script to scrape the 2016 Dublin marathon results from the 
results website.

@author: nmoran
"""

import requests
import bs4
import pandas as pd

fields = ['place', 'name', 'country', 'category', 'place in cat.', '10km', '1sthalf', '30km', 'chip_time', 'finish_time']
all_data = list(map(lambda x: [], range(len(fields))))

#for x in [0, 10, 20]:
#x = 0
x = 10530
while True:
    print('From %d' % x)
    #r = requests.get('http://results.dublinmarathon.ie/results.php?search&race=78&sort=placeall&from=%d'%x)
    r = requests.get('http://results.dublinmarathon.ie/results.php?search&race=66&sort=placeall&from=%d'%x)
    if r.status_code != 200:
        break
 
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('table')
    if len(table) > 0:
        for i,row in enumerate(table[0].find_all('tr')):
            if i == 0: continue
            parts = row.find_all('td')
            for j in range(len(fields)):
                #print('Adding <%s> to column %d'%(parts[j].text.strip(), j))
                all_data[j].append(parts[j].text.strip())
            #for j, field in enumerate(row.find_all('td')):
            #    all_data[j].append(field.text)
    else:
        print('No table field: %s for from %d' % (r.content, x))
        break
    x += 10

data = dict(list(map(lambda x: [fields[x], pd.Series(all_data[x])], range(len(fields)))))
df = pd.DataFrame(data)
df.to_csv('marathon_results_2015_dublin_2.csv')