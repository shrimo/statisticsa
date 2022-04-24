#!/usr/bin/python
# -*- coding: utf8 -*-

#StatisticsA for sequences days

import pathlib
import json
import numpy as np 
import cyrtranslit
from collections import Counter
import matplotlib.pyplot as plt


city_list = ['L*vivs*ka', 'Kryvoriz*ka', 'Vinnyc*ka', 'Pervomajs*ka', 'Kyïvs*ka', 'Pokrovs*kyj', 'Zaporiz*ka', 'Xarkivs*ka'
, 'Xarkivs*ka', 'Ivano-Frankivs*ka', 'Žytomyrs*ka', 'Sums*ka', 'Dnipropetrovs*ka', 'Ternopil*s*ka', 'Kyïv', 'Mykolaïv', 'Černihivs*ka'
, 'Pervomajs*kyj', 'Xmel*nyc*ka', 'Voznesens*k', 'Odes*ka', 'Zakarpats*ka', 'Čerkas*ka', 'Velykonovosilkivs*ka', 'Donec*ka', 'Rivnens*ka'
, 'Južnoukraïns*k', 'Kryvyj', 'Mykolaïvs*ka', 'Baxmuts*kyj', 'Volyns*ka', 'Vuhledars*ka', 'Starokostjantyniv', 'Dobropil*s*ka', 'Konotop'
, 'Baštanka', '']

def parsing_stringa(stringa, data_time,list_main, out_list):
    # parsing and adding areas to the list
    latin_text = cyrtranslit.to_latin(stringa, 'ua').replace("'",'*')    
    if 'Povitrjana tryvoha' in latin_text:        
        for st in latin_text.split():           
            # print (st)
            if st in city_list: #check city list                
                if data_time in list_main.get('date'): #check data/time
                    out_list.append(st)
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
    # return dict(sorted(count_list.items(), key=lambda item: item[1]))    
    return dict(sorted(count_list.items()))

def export_sequences(data_time):
    count_list_sort_01 = export_data(data_time, 'result.json')
    plt.style.use('dark_background')
    plt.ylim(0,20)
    # plt.xlim(0,10)
    plt.rcParams["figure.figsize"] = (8, 7)
    plt.bar(*zip(*count_list_sort_01.items()), label = data_time)
    plt.xticks(rotation=90, fontsize=10, fontname='monospace')
    plt.subplots_adjust(bottom=0.36)
    plt.title('Data: '+data_time)
    # plt.legend()
    frame = data_time.split('-')[2]
    file_path = str(pathlib.Path(__file__).parent.resolve())+'/render/'
    plt.savefig('{p}test_1_{f}.png'.format(p=file_path, f=frame))
    plt.close('all')


for day in range(1,25):
    print ('frame: {}'.format(day))
    if day<10:
        sequences ='2022-04-0'+str(day)
        export_sequences(sequences)
    else:
        sequences ='2022-04-'+str(day)
        export_sequences(sequences)


