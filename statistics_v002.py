#!/usr/bin/python
# -*- coding: utf8 -*-

#StatisticsA v002 (distribution by time of day)

import json
import numpy as np 
import cyrtranslit
from collections import Counter
import matplotlib.pyplot as plt


city_list = ['L*vivs*ka', 'Kryvoriz*ka', 'Vinnyc*ka', 'Pervomajs*ka', 'Kyïvs*ka', 'Pokrovs*kyj', 'Zaporiz*ka', 'Xarkivs*ka'
, 'Xarkivs*ka', 'Ivano-Frankivs*ka', 'Žytomyrs*ka', 'Sums*ka', 'Dnipropetrovs*ka', 'Ternopil*s*ka', 'Kyïv', 'Mykolaïv', 'Černihivs*ka'
, 'Pervomajs*kyj', 'Xmel*nyc*ka', 'Voznesens*k', 'Odes*ka', 'Zakarpats*ka', 'Čerkas*ka', 'Velykonovosilkivs*ka', 'Donec*ka', 'Rivnens*ka'
, 'Južnoukraïns*k', 'Kryvyj', 'Mykolaïvs*ka', 'Baxmuts*kyj', 'Volyns*ka', 'Vuhledars*ka', 'Starokostjantyniv', 'Dobropil*s*ka']

def parsing_stringa(stringa, data_time,list_main, out_list):
    # parsing and adding areas to the list
    latin_text = cyrtranslit.to_latin(stringa, 'ua').replace("'",'*')    
    if 'Povitrjana tryvoha' in latin_text:
        if data_time in list_main.get('date'):
            out_list.append(latin_text.split()[1].split(':')[0])
        # for st in latin_text.split():            
        #     if st in city_list: #check city list
        #         if data_time in list_main.get('date'): #check data/time
        #             out_list.append(st)
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


    count_list = Counter(out_list)
    return dict(sorted(count_list.items()))

data_time = ['2022-03', '2022-04']

data_key = 0
count_list_sort_01 = export_data(data_time[data_key], 'result.json')
# print (count_list_sort_01)
# X_key_01 = list(count_list_sort_01.keys())
# Y_key_01 = list(count_list_sort_01.values())

data_key = 1
count_list_sort_02 = export_data(data_time[data_key], 'result.json')

# print (count_list_sort_02)
# X_key_02 = list(count_list_sort_02.keys())
# Y_key_02 = list(count_list_sort_02.values())

fig, axs = plt.subplots(2, 1)

axs[0].bar(*zip(*count_list_sort_01.items()),label = data_time[0])
axs[1].bar(*zip(*count_list_sort_02.items()),label = data_time[1])

# plt.bar(*zip(*count_list_sort_01.items()), label = data_time[data_key], width=0.3)
# plt.bar(*zip(*count_list_sort_02.items()), label = data_time[data_key])
# plt.xticks(rotation=90, fontsize=10, fontname='monospace')

# plt.subplots_adjust(bottom=0.36)
axs[0].set_title('distribution by time of day: '+data_time[0])
axs[0].set_xlabel('time of day')
axs[1].set_title('distribution by time of day: '+data_time[1])
axs[1].set_xlabel('time of day')
# plt.legend()
fig.tight_layout()
plt.show()

# for k, v in count_list_sort.items():
#     print (k, v)