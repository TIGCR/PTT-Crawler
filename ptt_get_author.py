# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 23:03:11 2022

@author: TIGCR
"""

import pandas as pd
import sys
from PyPtt import PTT
import nest_asyncio
import datetime
import string
import requests
import json
nest_asyncio.apply()
def get_location(x):
    ip_address = x.ip
    response = requests.get(f'https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data&ip={ip_address}').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country")}
    return location_data
def get_post_date(x):
    dates=x[4:]
    months={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    month=months[dates[0:3]]
    year=dates[-4:]
    day=dates[4:6]
    post_date=year+'-'+month+'-'+day
    post_date=post_date.replace(' ','0')
    post_date=datetime.datetime.strptime(post_date,"%Y-%m-%d")
    return post_date
def count_word(x):
    chinese=[]
    english=[]
    number=[]
    en=''
    num=''
    for i in list(x):

        if i in string.ascii_letters:
            en+=i
        elif i.isdigit():
            num+=i
        else:
            if en !='':
                english.append(en)
            if num!='':
                number.append(num)
            en=''
            num=''
            if i !=' ':
                chinese.append(i)
    words=len(english)+len(chinese)+len(number)
    return words


#ptt_bot.logout()
def get_author(name,password,test_board,start_date,until_date,index_range,push_bool):
    nest_asyncio.apply()
    ptt_bot = PTT.API(log_level=PTT.log.level.SILENT)
    try:
        ptt_bot.login(name, password,kick_other_login=True)
        print('Login succeeded.')
    except (PTT.exceptions.WrongIDorPassword, PTT.exceptions.WrongPassword):
        sys.stderr.write('Wrong password.\n')
        #sys.exit()
    except PTT.exceptions.NoSuchUser:
        sys.stderr.write('No such user.\n')
        #sys.exit()
    except PTT.exceptions.LoginTooOften:
        sys.stderr.write('Too much login.\n')
        #sys.exit()
    except:
        sys.stderr.write('Login failed for unknown reason.\n')
    ptt_bot.log('登入成功')
    
    if ptt_bot.unregistered_user:
        print('未註冊使用者')
    
        if ptt_bot.process_picks != 0:
            print(f'註冊單處理順位 {ptt_bot.process_picks}')
    
    if ptt_bot.registered_user:
        print('已註冊使用者')
    aut_list=[]
    comments_list=[]
    #test_board = 'Gossiping'
    #test_range = 10
    start_index = ptt_bot.get_newest_index(
        PTT.data_type.index_type.BBS,
        board=test_board)
    start_date=datetime.datetime.strptime(start_date,"%Y-%m-%d")-datetime.timedelta(days=1)
    until_date=datetime.datetime.strptime(until_date,"%Y-%m-%d")
    post_date=datetime.datetime.today()
    #start_index = newest_index - test_range + 1
    while post_date>start_date:
        post_infor=ptt_bot.get_post(
                test_board,
                post_index= start_index)
       
        try:
            post_date=get_post_date(post_infor.date)
        except:
            pass
        print(f'index:{start_index}\n date:{post_date}')
        start_index-=index_range
    while post_date<until_date:
        #print(start_index)
        post_infor=ptt_bot.get_post(
                    test_board,
                    post_index=start_index)
        
        start_index+=1 
        try:
            date=post_infor.date
        except:
            pass
        try:
            post_date=get_post_date(date)
        except:
            pass
        try:
            # 去除下列註解可用關鍵字過濾特定標題，如"高虹安"
            if  2>1:#'高虹安' in post_infor.title:
                author=post_infor.author
                #date=post_infor.date
                #start_index+=1
                try:
                    title=post_infor.title
                except:
                    title='NA'
                date=post_infor.date
                try:
                    post_date=get_post_date(date)
                except:
                    pass
                try:
                    push_number=post_infor.push_number
                except:
                    push_number='NA'
                try:
                    con=post_infor.content.replace('\n','')
                    words=count_word(con)
                except:
                    con='NA'
                    words='NA'
                try:
                    #time.sleep(0.5)
                    ip_data=get_location(post_infor.ip)
                    ip=ip_data['ip']
                    city=ip_data['city']
                    region=ip_data['region']
                    country=ip_data['country']
                except:
                    ip='NA'
                    city='NA'
                    region='NA'
                    country='NA'
                print(author)
                print(date)
                push_count = 0
                boo_count = 0
                arrow_count = 0
                push_list=[]
                boo_list=[]
                arrow_list=[]
                if push_bool==True :
                    #print(len(post_infor.push_list))
                    if len(post_infor.push_list)!=0:
                        for push_info in post_infor.push_list:
                            #com_author = push_info.author
                            #com_content = push_info.content
                            #com_ip= push_info.ip
                            #try:
                               #push_ip_data=get_location(push_info.ip)
                                #push_ip=push_ip_data['ip']
                                #push_city=ip_data['city']
                                #push_region=ip_data['region']
                                #push_country=ip_data['country']
                            #except:
                                #push_ip='NA'
                                #push_city='NA'
                                #push_region='NA'
                                #push_country='NA'

                            
                            if push_info.type == PTT.data_type.push_type.PUSH:
                                push_count += 1

                                push_list.append([start_index,push_info.author,'推',push_info.content])
                            if push_info.type == PTT.data_type.push_type.BOO:
                                boo_count += 1

                                boo_list.append([start_index,push_info.author,'噓',push_info.content])
                            if push_info.type == PTT.data_type.push_type.ARROW:
                                arrow_count += 1

                                arrow_list.append([start_index,push_info.author,'箭頭',push_info.content])
                print(start_index)
                print(author)
                aut_list.append([start_index-1,author,title,post_date,push_number,con,words,ip,city,region,country,push_count,boo_count,arrow_count])
                push_df=pd.DataFrame(push_list,columns=['文章ID','作者','類型','內文'])
                boo_df=pd.DataFrame(boo_list,columns=['文章ID','作者','類型','內文'])
                arrow_df=pd.DataFrame(arrow_list,columns=['文章ID','作者','類型','內文'])
                comments_list.append(push_df)
                comments_list.append(boo_df)
                comments_list.append(arrow_df)
                #print('comments')
        except:
            pass
    #print(len(aut_list))         
    df=pd.DataFrame(aut_list,columns=['文章ID','作者','標題','日期','推文數','內文','字數','ip','城市','地區','國家','推','噓','箭頭'])
    #df['日期']=df.日期.map(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df[df.日期>start_date]
    df2=pd.concat(comments_list)
    return df,df2
#ptt帳號
name='您的PTT帳號'
#ptt密碼
password='您的密碼'
#要爬的板
test_board='HatePolitics'
index_range=50#抓時間每次間閣，發文數越多的板建議越大
start_date='2022-11-15'
until_date='2022-11-16'

df1,df2=get_author(name,password,test_board,start_date,until_date,index_range,push_bool=True)

df1.to_csv('文章內容.csv',index=False)
df2.to_csv('推文內容.csv',index=False)
