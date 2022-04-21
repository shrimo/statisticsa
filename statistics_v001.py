#!/usr/bin/python
# -*- coding: utf8 -*-

#StatisticsA

import json
import cyrtranslit
from collections import Counter
import matplotlib.pyplot as plt
# from transliterate import translit, get_available_language_codes

city_list = ['L*vivs*ka', 'Kryvoriz*ka', 'Vinnyc*ka', 'Pervomajs*ka', 'Kyïvs*ka', 'Pokrovs*kyj', 'Zaporiz*ka', 'Xarkivs*ka'
, 'Xarkivs*ka', 'Ivano-Frankivs*ka', 'Žytomyrs*ka', 'Sums*ka', 'Dnipropetrovs*ka', 'Ternopil*s*ka', 'Kyïv', 'Mykolaïv', 'Černihivs*ka'
, 'Pervomajs*kyj', 'Xmel*nyc*ka', 'Voznesens*k', 'Odes*ka', 'Zakarpats*ka', 'Čerkas*ka', 'Velykonovosilkivs*ka', 'Donec*ka', 'Rivnens*ka']

# print (city_list)

out_list = []
data_time = '2022-03'

with open('result.json') as fp:
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
count_list_sort = dict(sorted(count_list.items(), key=lambda item: item[1]))

# print (count_list_sort)
plt.bar(*zip(*count_list_sort.items()))
plt.xticks(rotation=90, fontsize=10, fontname='monospace')
plt.subplots_adjust(bottom=0.35)
# print (dir(plt))
plt.title('Data: '+data_time)
plt.show()
# for k, v in count_list_sort.items():
#     print (k, v)
