#!/usr/bin/python
# -*- coding: utf8 -*-

#StatisticsA. Single city (new test)

import json
import numpy as np 
from scipy.interpolate import interp1d
import cyrtranslit
from collections import Counter
import matplotlib.pyplot as plt
import torch


# city_list = ['L*vivs*ka', 'Kryvoriz*ka', 'Vinnyc*ka', 'Pervomajs*ka', 'Kyïvs*ka', 'Pokrovs*kyj', 'Zaporiz*ka', 'Xarkivs*ka'
# , 'Xarkivs*ka', 'Ivano-Frankivs*ka', 'Žytomyrs*ka', 'Sums*ka', 'Dnipropetrovs*ka', 'Ternopil*s*ka', 'Kyïv', 'Mykolaïv', 'Černihivs*ka'
# , 'Pervomajs*kyj', 'Xmel*nyc*ka', 'Voznesens*k', 'Odes*ka', 'Zakarpats*ka', 'Čerkas*ka', 'Velykonovosilkivs*ka', 'Donec*ka', 'Rivnens*ka'
# , 'Južnoukraïns*k', 'Kryvyj', 'Mykolaïvs*ka', 'Baxmuts*kyj', 'Volyns*ka', 'Vuhledars*ka', 'Starokostjantyniv', 'Dobropil*s*ka', 'Konotop'
# , 'Baštanka', 'Luhans*ka']

city_list = ['Kyïv']

class City_A:
    def __init__(self, city_name, data, time):
        self.city_name = city_name
        self.data = data
        self.time = time

def parsing_stringa(stringa, data_time,list_main, out_list):
    # parsing and adding areas to the list
    latin_text = cyrtranslit.to_latin(stringa, 'ua').replace("'",'*')    
    if 'Povitrjana tryvoha' in latin_text:        
        for st in latin_text.split():
            if st in city_list: #check city list                
                if data_time in list_main.get('date'): #check data/time
                    d_tmp = list_main.get('date')[:10]
                    t_tmp = list_main.get('date')[11:]
                    # out_list.append([st, d_tmp, t_tmp])
                    out_list.append(d_tmp)
    return True

def export_data(data_time, file_name):    
    out_list = []
    with open(file_name) as fp:
        data = json.load(fp)

    jdict = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

    for key in data.items():
        for i in key:        
            if type(i) is list:
                for list_main in i:
                    if list_main.get('type') == 'message':                        
                        text1 = list_main.get('text')                        
                        if type(text1[0]) is dict:
                            parsing_stringa(text1[0].get('text'), data_time, list_main, out_list)  
                        elif type(text1[0]) is str: # new date format          
                            parsing_stringa(text1[0], data_time, list_main, out_list)
    return out_list    

data_time = ['2022-03', '2022-04', '2022-05']
# data_time = ['2022-04']

def days(dt, day):
    out_days = ''
    if day<10:
        out_days = str(dt)+'-0'+str(day)
    else:
        out_days = str(dt)+'-'+str(day)
    return out_days



o_list = []
# print (export_data('2022-03', 'result.json'))
for dt in data_time:
    city_dict = Counter(export_data(dt, 'result.json'))    
    for i in range(1, 30):
        if not city_dict[days(dt, i)]:
            city_dict[days(dt, i)] = 0
    for i in range(len(city_dict)):
        o_list.append(city_dict[days(dt, i+1)])
        # o_list.append(np.linspace(0.01, city_dict[days(dt, i+1)]*0.1, num=10))
        # print (days(dt, i+1), city_dict[days(dt, i+1)])
                
# print (o_list[14:])

x = np.linspace(1, len(o_list[14:]), len(o_list[14:]))
y = np.asarray(o_list[14:])

cubic_interploation_model = interp1d(x, y, kind = "cubic")
X_=np.linspace(x.min(), x.max(), 1000)
Y_=cubic_interploation_model(X_)

plt.plot(X_, Y_)
plt.title(city_list[0])
plt.show()

# torch.save(np.asarray(o_list), open('traindata.pt', 'wb'))

    # plt.bar(*zip(*city_list.items()), label = dt)
    

# plt.xticks(rotation=90, fontsize=8, fontname='monospace')
# plt.subplots_adjust(bottom=0.36)
# plt.legend()
# plt.show()

