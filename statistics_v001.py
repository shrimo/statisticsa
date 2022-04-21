#!/usr/bin/python
# -*- coding: utf8 -*-

#StatisticsA

import json
import numpy as np 
import cyrtranslit
from collections import Counter
import matplotlib.pyplot as plt
# from transliterate import translit, get_available_language_codes

city_list = ['L*vivs*ka', 'Kryvoriz*ka', 'Vinnyc*ka', 'Pervomajs*ka', 'Kyïvs*ka', 'Pokrovs*kyj', 'Zaporiz*ka', 'Xarkivs*ka'
, 'Xarkivs*ka', 'Ivano-Frankivs*ka', 'Žytomyrs*ka', 'Sums*ka', 'Dnipropetrovs*ka', 'Ternopil*s*ka', 'Kyïv', 'Mykolaïv', 'Černihivs*ka'
, 'Pervomajs*kyj', 'Xmel*nyc*ka', 'Voznesens*k', 'Odes*ka', 'Zakarpats*ka', 'Čerkas*ka', 'Velykonovosilkivs*ka', 'Donec*ka', 'Rivnens*ka']

# print (city_list)

def export_data(data_time, file_name):
    out_list = []
    with open(file_name) as fp:
        data = json.load(fp)

    jdict = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

    for key in data.items():
        for i in key:        
            if type(i) is list:
                for l in i:
                    if l.get('type') == 'message':
                        # print ('data: '+l.get('date'))                                            
                        text1 = l.get('text')
                        latin_text = cyrtranslit.to_latin(text1[0].get('text'), 'ua').replace("'",'*')
                        # print (latin_text)
                        if 'Povitrjana tryvoha' in latin_text:
                            # print (latin_text)
                            for st in latin_text.split():
                                # print (st)
                                if st in city_list: #check city list
                                    if data_time in l.get('date'): #check data/time
                                        # print ('data: '+l.get('date')) 
                                        out_list.append(st)

    count_list = Counter(out_list)
    return dict(sorted(count_list.items(), key=lambda item: item[1]))

# print (count_list_sort)
data_time_01 = '2022-04'
data_time_02 = '2022-03'
count_list_sort_01 = export_data(data_time_01, 'result.json')
count_list_sort_02 = export_data(data_time_02, 'result.json')

# X_axis = np.arange(len(count_list_sort_01.keys()))

plt.bar(*zip(*count_list_sort_01.items()), label = '2022-04')
plt.bar(*zip(*count_list_sort_02.items()), label = '2022-03')

plt.xticks(rotation=90, fontsize=10, fontname='monospace')
plt.subplots_adjust(bottom=0.35)
# print (dir(plt))
plt.title('Data: '+data_time_01+' - '+data_time_02)
plt.legend()
plt.show()
# for k, v in count_list_sort.items():
#     print (k, v)
