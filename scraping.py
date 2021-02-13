#!/usr/bin/python3
#-*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup

def getTimes(URL_season):
    req = requests.get(URL_season)
    if req.status_code == 200: # Verifica se o site foi acessado com sucesso.
        soup = BeautifulSoup(req.text, 'html.parser')
        times_table = soup.find_all("table", class_="standard_tabelle") # Pega a tabela (table, em html) completa, pelo "chave" que é o nome da class.
        times_lines = str(times_table[0]).split("<tr>") # Quebra a string da tabela nos tr's (linhas da tabela).

        dict_names_url = {} # Dicionário cujo a chave é o nome do time e o valor é a url do mesmo.
        for column in times_lines: # Percorre as linhas da tabela e procura pelo nome do time e a url dele, após isso salva no dicionário acima.
            if "td align=\"center\"" in column:
                time_name = column.split("href=\"")[1].split("\">")[1].split("alt=\"")[1].split("\"")[0]
                time_url = column.split("href=\"")[1].split("\">")[0]
                dict_names_url[time_name] = time_url

        return dict_names_url

def getNotices(dict_names_url):
    URL_default = "https://www.worldfootball.net/"
    #cont = 1 #sadadasdasdas
    for time_url in dict_names_url:
        #if cont == 3: break  #sadadasdasdas
        dict_notices = {'date': [], 'hour': [], 'title': [], 'subtitle': [], 'text': []}
        news_table = True
        cont_page = 1
        while news_table != []:
            #if cont_page == 4: break #sadadasdasdas
            try:
                req = requests.get(URL_default+dict_names_url[time_url].replace("/teams/", "news/"+str(cont_page)+"/"))
                if req.status_code == 200:
                    soup1 = BeautifulSoup(req.text, 'html.parser')
                    news_table = soup1.find_all("div", class_="wfb-news-general")
                    soup_news_table = BeautifulSoup(str(news_table[0]), 'html.parser')
                    news_list = soup_news_table.find_all("div", class_="module module-newmon module-newmon-default")
                    soup_news_list = BeautifulSoup(str(news_list[0]), 'html.parser')
                    news_list1 = soup_news_list.find_all("div", class_="module-newmon-image")

                    news_urls = []
                    for news in news_list1:
                        soup_news_list1 = BeautifulSoup(str(news), 'html.parser')
                        news_url = soup_news_list1.find_all("a")
                        news_urls.append(str(news_url[0]).split("href=\"")[1].split("\"")[0])

                    for url in news_urls:
                        url_notice = url
                        req_notice = requests.get(URL_default+url_notice)
                        if req_notice.status_code == 200:
                            soup2 = BeautifulSoup(req_notice.text, 'html.parser')
                            news_box = soup2.find_all("div", class_="box")
                            # print(news_box)
                            soup_box = BeautifulSoup(str(news_box[0]), 'html.parser')
                            news_date = soup_box.find_all("div", class_="wfb-news-date")
                            news_date = str(news_date[0]).split("\n\t\t")[1].split("h\n\t")[0]
                            news_date, news_hour, _ = news_date.split(" ")
                            # print(news_date, news_hour)
                            news_title = soup_box.find_all("h1", class_="wfb-news-title")
                            news_title = str(news_title[0]).split("\">")[1].split("</h1>")[0]
                            # print(news_title)
                            news_content = soup_box.find_all("div", class_="wfb-news-content")
                            news_paragraphs = BeautifulSoup(str(news_content[0]), 'html.parser')
                            news_paragraphs = news_paragraphs.find_all("p")
                            # print(news_paragraphs)
                            news_subtitle = str(news_paragraphs[0]).split("<p>")[1].split("</p>")[0]
                            # print(news_subtitle)
                            news_text = ""
                            for paragraph in range(1,len(news_paragraphs)):
                                news_text += str(news_paragraphs[paragraph]).split("<p>")[1].split("</p>")[0]
                                news_text += " "

                            dict_notices['date'].append(news_date.replace(".", "/"))
                            dict_notices['hour'].append(news_hour)
                            dict_notices['title'].append(news_title)
                            dict_notices['subtitle'].append(news_subtitle)
                            dict_notices['text'].append(news_text.strip())
                            # print(dict_notices)
                    cont_page += 1
            except:
                cont_page += 1
                pass

        df = pd.DataFrame(dict_notices, columns=['date', 'hour', 'title', 'subtitle', 'text'])
        PATH = f'C:\\Users\\Peterson\\Desktop\\IC\\{time_url}.csv'
        df.to_csv(PATH)
        #cont += 1 #sadadasdasdas

if __name__ == "__main__":
    URL_season = "https://www.worldfootball.net/players/ita-serie-a-2020-2021/"
    dict_names_url = getTimes(URL_season)
    # print(dict_names_url)
    # dict_names_url = {}
    getNotices(dict_names_url)
