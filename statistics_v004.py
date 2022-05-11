#!/usr/bin/python
# -*- coding: utf8 -*-

#StatisticsA. Single city

import json
import numpy as np 
import cyrtranslit
from collections import Counter
import matplotlib.pyplot as plt


# city_list = ['L*vivs*ka', 'Kryvoriz*ka', 'Vinnyc*ka', 'Pervomajs*ka', 'Kyïvs*ka', 'Pokrovs*kyj', 'Zaporiz*ka', 'Xarkivs*ka'
# , 'Xarkivs*ka', 'Ivano-Frankivs*ka', 'Žytomyrs*ka', 'Sums*ka', 'Dnipropetrovs*ka', 'Ternopil*s*ka', 'Kyïv', 'Mykolaïv', 'Černihivs*ka'
# , 'Pervomajs*kyj', 'Xmel*nyc*ka', 'Voznesens*k', 'Odes*ka', 'Zakarpats*ka', 'Čerkas*ka', 'Velykonovosilkivs*ka', 'Donec*ka', 'Rivnens*ka'
# , 'Južnoukraïns*k', 'Kryvyj', 'Mykolaïvs*ka', 'Baxmuts*kyj', 'Volyns*ka', 'Vuhledars*ka', 'Starokostjantyniv', 'Dobropil*s*ka', 'Konotop'
# , 'Baštanka', 'Luhans*ka']

city_list = ['Mykolaïvs*ka']

def parsing_stringa(stringa, data_time,list_main, out_list):
    # parsing and adding areas to the list
    latin_text = cyrtranslit.to_latin(stringa, 'ua').replace("'",'*')    
    if 'Povitrjana tryvoha' in latin_text:        
        for st in latin_text.split():
            # if 'L' in st:
            #     print (st)
            if st in city_list: #check city list
                if data_time in list_main.get('date'): #check data/time
                    out_list.append(list_main.get('date')[:10])
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


    # count_list = Counter(out_list)
    return Counter(out_list)
    # return dict(sorted(count_list.items(), key=lambda item: item[1]))    

data_time = ['2022-03', '2022-04', '2022-05']
for dt in data_time:
    count_list_sort_01 = export_data(dt, 'result.json')
    plt.bar(*zip(*count_list_sort_01.items()), label = dt)
    plt.title(city_list[0]+' - Data: '+dt)

plt.xticks(rotation=90, fontsize=8, fontname='monospace')
plt.subplots_adjust(bottom=0.36)
plt.legend()
plt.show()

