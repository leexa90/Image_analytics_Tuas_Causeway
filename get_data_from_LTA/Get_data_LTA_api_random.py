#!/usr/bin/env python
import pandas as pd
import json
import os
import datetime
import numpy as np
np.random.seed(1)
class generate:
    def __init__(self, seed,hour):
            self.seed = seed
            np.random.seed(seed)
            self.day = np.random.choice(range(1,28))
            self.hour = np.random.choice(range(24))
            self.minute = np.random.choice(range(60))
            self.month = np.random.choice(range(1,13))
            self.year = 2018
            self.hour = hour
            

currentDT = datetime.datetime.now()
for seed in range(1,1000):
    currentDT  = generate(seed,seed%24)
    try:
        day = str(currentDT.day)
        if int(day) < 10:
            day = '0'+day
        hour = str(currentDT.hour)
        if int(hour) < 10:
            hour = '0'+hour
        minute = str(currentDT.minute)
        if int(minute) < 10:
            minute = '0' + minute
        year = str(currentDT.year)
        month = str(currentDT.month)
        if int(month) < 10:
            month = '0'+month
        counter = 0
        y = '/usr/bin/curl -X GET \"https://api.data.gov.sg/v1/transport/traffic-images?date_time='+str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+'%3A'+str(minute)+'%3A41%2B08%3A00\" -H  \"accept: application/json\"'
        y = y+ '  > ./api_info/data%s \n' %(str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+'%3A'+str(minute))

        os.system(y)
        filename = './api_info/data' + str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+'%3A'+str(minute)
        data= json.load(open(filename,'r'))
        import time
        time.sleep(30)
        for item in data['items'][0]['cameras']:
                timestamp = item['timestamp']
                cam_id = item['camera_id']
                if cam_id !='4713':
                    continue
                else:
                    print (cam_id)
                image_link = item['image']
                if cam_id  not in [x for x in os.listdir('./') if os.path.isdir('./'+x)]:
                    os.mkdir('./'+cam_id)
                wget_image = '/usr/bin/wget '+str(image_link) + \
                          ' -O '+cam_id+'/'+timestamp+'.jpg'
                os.system(wget_image)
        time.sleep(30)
    except : time.sleep(30)
die
if False:
    counter = 2
    f1 = open('run_get_traffice_light','w')
    for day in range(21,28):
        day = str(day)
        for hour in range(0,24):
            hour = str(hour)
            if int(hour) < 10:
                hour = '0'+hour
            for minute in range(60):
                minute = str(minute)
                if int(minute) < 10:
                    minute = '0' + minute
                y = 'curl -X GET \"https://api.data.gov.sg/v1/transport/traffic-images?date_time=2018-12-'+str(day)+'T'+str(hour)+'%3A'+str(minute)+'%3A41%2B08%3A00\" -H  \"accept: application/json\"'
                y = y+ '  > data%s \n' %counter
                counter += 1
                f1.write(y)
    f1.close()
import sys
if True:
    data= json.load(open(sys.argv[1],'records'))

    
    for item in data['items'][0]['cameras']:
        timestamp = item['timestamp']
        cam_id = item['camera_id']
        if cam_id !='4713':
            continue
        else:
            print (cam_id)
        image_link = item['image']
        if cam_id  not in [x for x in os.listdir('./data') if os.path.isdir('./data/'+x)]:
            os.mkdir('./data/'+cam_id)        
        os.system('wget '+str(image_link) + \
                  ' -O ./data/'+cam_id+'/'+timestamp+'.jpg')
