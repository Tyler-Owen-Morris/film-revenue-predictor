import requests
import pandas as pd
import numpy as np
import json
import time
import random
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

film_list = 'data/us2014_filmList-WORKING.csv'
title_file = pd.read_csv(film_list)['titleId'].values
out_file = 'data/IMDB_mine_data_2014.csv'

def fetch_film_data(title_code):
    print("Fetching film data for title: "+title_code)
    try:
        #scrape IMDB PRO
        url = 'https://pro.imdb.com/title/'+title_code+'/boxoffice'
        headers = {
            'Cookie':'''session-id=138-1311213-4138762; adblk=adblk_no; ubid-main=131-2177923-5330445; session-id-time=2218844129l; x-main="IS86HKXSJMigI0RnIigNqWd@Pu8ZQWgbXHTCS5NC44TGbsoydTDB4J3y0KW4qQJw"; at-main=Atza|IwEBILUkej479bl-hN19LhAyANxzITDWvKeBnZnnNNWk10j0SijTTrcP1xHYude5_tVJrzPsq30ehR12BnByawJoVpMhpgQ_hNpe0PYjxNHJTAQIAjOTF1wpOsTVFURmn8zA9cCV43yBuMIWlH9cQeyn7lV7Kdd47Hn--VPkHz_W88D4CZ-L1N-H-c-y65FUxELVH6R6EPnh830ssfLXG5L864QRO9hBDwKchx_d6hepwITlwuO8qetimWYabwo8Hty6QX5nZuKY2HNpCWmsakxByc50NIAp7Uy7_bZkvZW2sN8dK9kON4xPKIygVHhMWJQ6wh2-d0DykEh4BKAnSs8dTOaGBf2Wq33d5V4XKmz9RPhyup41DXR5DFVPQojnJoMGVNVo1hd_Xan63I94uYk1JEMN; sess-at-main="p9whlqJpRA5/kki0a+qwvIksIhZyceM2oTm2NUGUstA="; uu=BCYoQbsIiwfBoS5Z-9VBEM4GQeZlJd-x0dsY76F-NJiyuSyqzmSEMKbVSar_-kScSNRzLG9PNA9I%0D%0Ajdjov4ijeWrg0KYq7RquhDNrANLf2r_CKRWG40LVJlIVEtUtjfN7vlSPexThCyrlRCA6MaZXDAXU%0D%0APJiwN-Oy2Uileof_lGTBYNE%0D%0A; pa=BCYo5O3AftOw_UMyDZBOrkb5nNPu-MMicHEKRBry99NXBnJRqeW3prdQxa0PDs0tVA8QWusbH7tZ%0D%0Anraln_N9jpUhsHsZ_jxhsmPTLpuksiUytkmvL8ZfDM5RxRZzJUpLkDX6%0D%0A; session-token="FGBlsQXWFfNa1aXpisRWiZ24Zh7zfYgzF86EWr2infSQ/A6LyfZB++iPHpTBeYr2C2ZzH/C96D7YqEVAjt91KwKNDfhgKCBhgo3cwIzkZ9A2ZqntW/EE9MsAa8/KfK7XLvtj4lUy/nEmiyLVq9Gc2U6Exc1kovQN4H5GmkruH/ywN/ZwSmxBk1VEIqNKeSVbDDnA8JE2OJXuKQNPFsmu5kLk62fEK2cMJMb1pQZw6rU="; csm-hit=tb:FVQ9NP1114J2DT3PZ86C+s-WXASZQ2TS1F9RJ5CAPX5|1588207251592&t:1588207251592&adb:adblk_no"'''
        }
        resp = requests.request("GET", url, headers=headers) 
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", {"id": "box_office_summary"})
        bo = None
        if not div== None:
            bo = div.find_all("div",{"class":"a-column a-span5 a-text-right a-span-last"})
        div1 = soup.find("div", {"id": "contacts"})
        b = None
        if not div1== None:
            b = div1.find_all("span",{"class":"aok-align-center"})
        production = []
        if not b==None:
            for i in b:
                production.append(i.text)
        budget = None
        opening_wknd = None
        gross_dom = None
        gross_int = None
        
        if not bo == None:
            if len(bo) >= 1:
                print("got budget")
                budget = int(bo[0].text.replace(',','').replace('\n', '').replace('$', ''))
            if len(bo) >= 2:
                print("got opening weekend")
                opening_wknd = int(bo[1].text.replace(',','').replace('\n', '').replace('$', ''))
            else:
                #update the master-list that this title is complete.
                m_lis = pd.read_csv(film_list, index_col=0)
                m_lis = m_lis[m_lis['titleId'] != title_code]
                m_lis.to_csv(film_list)
                print("Title from the working list: "+title_code + " : "+ row['title'].values[0]+" discarded for lacking Box Office info")
                print("Progressing to next title....")
                return None
            if len(bo) >=3:
                gross_dom = int(bo[2].text.replace(',','').replace('\n', '').replace('$', ''))
            if len(bo) >= 4:
                gross_int = int(bo[3].text.replace(',','').replace('\n', '').replace('$', ''))
        else:
            #update the master-list that this title is complete.
            m_lis = pd.read_csv(film_list, index_col=0)
            m_lis = m_lis[m_lis['titleId'] != title_code]
            m_lis.to_csv(film_list)
            print("Title from the working list: "+title_code + " : "+ row['title'].values[0]+" discarded for lacking Box Office info")
            print("Progressing to next title....")
            return None
        print("IMDB pro scrape complete")


        #IMDB api meta-data
        url = "https://imdb8.p.rapidapi.com/title/get-meta-data"
        querystring = {"region":"US","ids":title_code}
        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': "cb8ae0789fmshd5f578d8c964ca6p18b81fjsn3f8341b9ef41"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        meta_json = json.loads(response.text)
        time.sleep(1)
        
        #IMDB api top-billed
        url = "https://imdb8.p.rapidapi.com/title/get-top-cast"
        querystring = {"tconst":title_code}
        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': "cb8ae0789fmshd5f578d8c964ca6p18b81fjsn3f8341b9ef41"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        actor_json = json.loads(response.text)
        time.sleep(1)
        
        #IMDB api top-crew
        url = "https://imdb8.p.rapidapi.com/title/get-top-crew"
        querystring = {"tconst":title_code}
        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': "cb8ae0789fmshd5f578d8c964ca6p18b81fjsn3f8341b9ef41"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        crew_json = json.loads(response.text)
        time.sleep(1)
        
        #pull that data together
        title = meta_json[title_code]['title']['title']
        if 'runningTimeInMinutes' in meta_json[title_code]:
            runtime = meta_json[title_code]['title']['runningTimeInMinutes']
        else:
            runtime = 0
        release_date = meta_json[title_code]['releaseDate']
        rating = meta_json[title_code]['certificate']
        if 'metaScore' in meta_json[title_code]:
            metaScore = meta_json[title_code]['metacritic']['metaScore']
        else:
            metaScore = 0
        if 'userScore' in meta_json[title_code]:
            metaUserScore = meta_json[title_code]['metacritic']['userScore']
        else:
            metaUserScore = 0
        if 'rating' in meta_json[title_code]:
            imdbRating = meta_json[title_code]['ratings']['rating']
        else:
            imdbRating = 0
        genre = []
        if isinstance(meta_json[title_code], dict):
            for g in meta_json[title_code]['genres']:
                genre.append(g)
                
        #principal actors        
        actor1 = None 
        actor2 = None
        actor3 = None
        actor4 = None
        actor5 = None
        actor6 = None
        actor7 = None
        actor8 = None
        actor9 = None
        actor10= None
        if not actor_json == None:
            if isinstance(actor_json, list):
                if len(actor_json) >= 1:
                    actor1 = actor_json[0]
                if len(actor_json) >= 2:
                    actor2 = actor_json[1]
                if len(actor_json) >= 3:
                    actor3 = actor_json[2]
                if len(actor_json) >= 4:
                    actor4 = actor_json[3]
                if len(actor_json) >= 5:
                    actor5 = actor_json[4]
                if len(actor_json) >= 6:
                    actor6 = actor_json[5]
                if len(actor_json) >= 7:
                    actor7 = actor_json[6]
                if len(actor_json) >= 8:
                    actor8 = actor_json[7]
                if len(actor_json) >= 9:
                    actor9 = actor_json[8]
                if len(actor_json) >= 10:
                    actor10 = actor_json[9]
        
        #pricipal crew
        directors = [] 
        for d in crew_json['directors']:
            directors.append(d['name'])
        writers = []
        for w in crew_json['writers']:
            writers.append(w['name'])
                
        #construct the dataframe
        cols = ['title_code','title', 'runtime', 'release_date',  'rating', 'prod_co','metaScore', 'metaUserScore',
        'imdb_rating', 'genre', 'actor1', 'actor2', 'actor3', 'actor4', 'actor5', 'actor6', 'actor7', 'actor8', 'actor9', 'actor10',
        'directors', 'writers', 'budget', 'opening_wknd', 'gross_dom', 'gross_int']
        df = pd.DataFrame(columns=cols)
        df.loc[0] = [title_code, title, runtime, release_date, rating, production, metaScore, metaUserScore, imdbRating, genre, actor1, actor2,
                    actor3, actor4, actor5, actor6, actor7, actor8, actor9, actor10, directors, writers, budget,
                    opening_wknd, gross_dom, gross_int]
        
        #return the DF
        return df
    except:
        #if there's an error return none
        print("Scrape Fail!")
        return None




# *****************
#    MAIN LOOP
# *****************

print("*********************************************************")
print("  |   .-')    .-') _      ('-.     _  .-')   .-') _     |")
print("  |  ( OO ). (  OO) )    ( OO ).-.( \( -O ) (  OO) )    |")
print("  | (_)---\_)/     '._   / . --. / ,------. /     '._   |")
print("  | /    _ | |'--...__)  | \-.  \  |   /`. '|'--...__)  |")
print("  | \  :` `. '--.  .--'.-'-'  |  | |  /  | |'--.  .--'  |")
print("  |  '..`''.)   |  |    \| |_.'  | |  |_.' |   |  |     |")
print("  | .-._)   \   |  |     |  .-.  | |  .  '.'   |  |     |")
print("  | \       /   |  |     |  | |  | |  |\  \    |  |     |")
print("  |  `-----'    `--'     `--' `--' `--' '--'   `--'     |")
print("*********************************************************")


c = 0 #counting which fast loop we're on
t = 5 #the number of fast loops we initilize
for title in title_file:
    #fetch the new row
    row = fetch_film_data(title)
    if not isinstance(row, pd.DataFrame):
        w = random.uniform(1.2, 2.1)
        print("Encountered an error on title: "+title)
        print("Waiting for {} seconds to try next title".format(w))
        print("**************************")
        print("  ___ _ __ _ __ ___  _ __ ")
        print(" / _ \ '__| '__/ _ \| '__|")
        print("|  __/ |  | | | (_) | |   ")
        print(" \___|_|  |_|  \___/|_|   ")
        print("**************************")
        time.sleep(w)
        continue  #If the function returns None, then there was a web error: wait 20 and go to the next title.
    #open outfile and append
    print("Appending retrieved information for: "+ row['title'].values[0])
    out_df = pd.read_csv(out_file, index_col=0)
    out_df.append(row).to_csv(out_file)
    print("Save to file succeeded. Current record stored count : " + str(out_df.shape[0]))

    #update the master-list that this title is complete.
    m_lis = pd.read_csv(film_list, index_col=0)
    m_lis = m_lis[m_lis['titleId'] != title]
    m_lis.to_csv(film_list)
    print("Successfully removed the title from the working list: "+title + " : "+ row['title'].values[0])
    print("Currenttotal records remaining to read : "+str(m_lis.shape[0]))


    print("*********************************")
    print(" ___ _   _  ___ ___ ___  ___ ___  ")
    print("/ __| | | |/ __/ __/ _ \/ __/ __| ")
    print("\__ \ |_| | (_| (_|  __/\__ \__ \ ")
    print("|___/\__,_|\___\___\___||___/___/ ")
    print("*********************************")


    #wait intelligently!
    wait_time = random.uniform(0.2, 1.5)
    print("********************")
    print("Beginning wait cycle for "+str(wait_time)+" seconds")
    time.sleep(wait_time)
    # c += 1
    # print("Short cycle complete")
    # print("********************")
    # if c >= t:
    #     print("Beginning long cycle wait")
    #     waiter = random.uniform(0.01, 3.2)
    #     c = 0
    #     t = random.randint(6, 16)
    #     print("will restart with "+str(t)+" more short loops after waiting for "+str(waiter*30)+" seconds")
    #     print("********************")
    #     time.sleep(waiter*30)

print("******************************************************************************")
print(" _____            _        _____                       _      _         _ _ _ ")
print("/  __ \          | |      /  __ \                     | |    | |       | | | |")
print("| /  \/_   _  ___| | ___  | /  \/ ___  _ __ ___  _ __ | | ___| |_ ___  | | | |")
print("| |   | | | |/ __| |/ _ \ | |    / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \ | | | |")
print("| \__/\ |_| | (__| |  __/ | \__/\ (_) | | | | | | |_) | |  __/ ||  __/ |_|_|_|")
print(" \____/\__, |\___|_|\___|  \____/\___/|_| |_| |_| .__/|_|\___|\__\___| (_|_|_)")
print("        __/ |                                   | |                           ")
print("       |___/                                    |_|                           ")
print("******************************************************************************")