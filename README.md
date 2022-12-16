# PTT-Crawler
## 目的
本程式可爬取PTT特定版面文章內容與推文內容。


## 需求參數
需輸入PTT使用者的帳號密碼。
```
#ptt帳號
name=''
#ptt密碼
password=''
```
設定爬取的貼文發布時間。
```
start_date='2022-11-15'
until_date='2022-11-16'
```
設定爬取的貼文儲存檔名。
```
df1,df2=get_author(name,password,test_board,start_date,until_date,index_range,push_bool=True)
df1.to_csv('文章內容.csv',index=False)
df2.to_csv('推文內容.csv',index=False)
```

## 開發團隊
政治大學台灣政經傳播中心  大數據小組  
洪國智、丁家麒、呂修齊
