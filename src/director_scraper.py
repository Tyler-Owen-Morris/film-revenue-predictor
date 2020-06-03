import requests
import pandas as pd
import numpy as np
import json
import time
import random
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

film_list = 'data/director_popularity_scrape_list.csv'
title_file = pd.read_csv(film_list)['title_code'].values
out_file = 'data/director_popularity_out.csv'

def fetch_director_data(title_code):
    try:
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

        dir_code = crew_json['directors'][0]['id']
        dir_name = crew_json['directors'][0]['name']
        
        #scrape IMDB PRO
        url = 'https://pro.imdb.com'+dir_code
        headers = {
            'Cookie':'''session-id=138-1311213-4138762; adblk=adblk_no; ubid-main=131-2177923-5330445; session-id-time=2218844129l; x-main="IS86HKXSJMigI0RnIigNqWd@Pu8ZQWgbXHTCS5NC44TGbsoydTDB4J3y0KW4qQJw"; at-main=Atza|IwEBILUkej479bl-hN19LhAyANxzITDWvKeBnZnnNNWk10j0SijTTrcP1xHYude5_tVJrzPsq30ehR12BnByawJoVpMhpgQ_hNpe0PYjxNHJTAQIAjOTF1wpOsTVFURmn8zA9cCV43yBuMIWlH9cQeyn7lV7Kdd47Hn--VPkHz_W88D4CZ-L1N-H-c-y65FUxELVH6R6EPnh830ssfLXG5L864QRO9hBDwKchx_d6hepwITlwuO8qetimWYabwo8Hty6QX5nZuKY2HNpCWmsakxByc50NIAp7Uy7_bZkvZW2sN8dK9kON4xPKIygVHhMWJQ6wh2-d0DykEh4BKAnSs8dTOaGBf2Wq33d5V4XKmz9RPhyup41DXR5DFVPQojnJoMGVNVo1hd_Xan63I94uYk1JEMN; sess-at-main="p9whlqJpRA5/kki0a+qwvIksIhZyceM2oTm2NUGUstA="; uu=BCYoQbsIiwfBoS5Z-9VBEM4GQeZlJd-x0dsY76F-NJiyuSyqzmSEMKbVSar_-kScSNRzLG9PNA9I%0D%0Ajdjov4ijeWrg0KYq7RquhDNrANLf2r_CKRWG40LVJlIVEtUtjfN7vlSPexThCyrlRCA6MaZXDAXU%0D%0APJiwN-Oy2Uileof_lGTBYNE%0D%0A; pa=BCYo5O3AftOw_UMyDZBOrkb5nNPu-MMicHEKRBry99NXBnJRqeW3prdQxa0PDs0tVA8QWusbH7tZ%0D%0Anraln_N9jpUhsHsZ_jxhsmPTLpuksiUytkmvL8ZfDM5RxRZzJUpLkDX6%0D%0A; session-token="FGBlsQXWFfNa1aXpisRWiZ24Zh7zfYgzF86EWr2infSQ/A6LyfZB++iPHpTBeYr2C2ZzH/C96D7YqEVAjt91KwKNDfhgKCBhgo3cwIzkZ9A2ZqntW/EE9MsAa8/KfK7XLvtj4lUy/nEmiyLVq9Gc2U6Exc1kovQN4H5GmkruH/ywN/ZwSmxBk1VEIqNKeSVbDDnA8JE2OJXuKQNPFsmu5kLk62fEK2cMJMb1pQZw6rU="; csm-hit=tb:FVQ9NP1114J2DT3PZ86C+s-WXASZQ2TS1F9RJ5CAPX5|1588207251592&t:1588207251592&adb:adblk_no"'''
        }
        resp = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        div = soup.find("div", {"id": "popularity_widget"})
        act = div.find("a", {"class": "a-size- a-align- a-link- clickable_share_link"})
        pop = int(act.text.replace('\n', '').replace(' ', '').replace(',', ''))
        time.sleep(1)
        
        #construct the dataframe
        cols = ['director','name','populairty']
        df = pd.DataFrame(columns=cols)
        df.loc[0] = [dir_code, dir_name, pop]
        
        #return the DF
        return df
    except:
        #if there's an error return none
        return None




# *****************
# MAIN LOOP
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



for title in title_file:
    #fetch the new row
    print("Fetching film data for title: "+title)
    row = fetch_director_data(title)
    if not isinstance(row, pd.DataFrame):
        w = random.uniform(1.2, 7.1)
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
    print("Appending retrieved information for: "+ row['director'].values[0])
    out_df = pd.read_csv(out_file, index_col=0)
    out_df.append(row).to_csv(out_file)
    print("Save to file succeeded. Current record stored count : " + str(out_df.shape[0]))

    #update the master-list that this title is complete.
    m_lis = pd.read_csv(film_list, index_col=0)
    m_lis = m_lis[m_lis['title_code'] != title]
    m_lis.to_csv(film_list)
    print("Successfully removed the title from the working list: "+title + " : "+ row['director'].values[0])
    print("Currenttotal records remaining to read : "+str(m_lis.shape[0]))


    print("*********************************")
    print(" ___ _   _  ___ ___ ___  ___ ___  ")
    print("/ __| | | |/ __/ __/ _ \/ __/ __| ")
    print("\__ \ |_| | (_| (_|  __/\__ \__ \ ")
    print("|___/\__,_|\___\___\___||___/___/ ")
    print("*********************************")


    #wait intelligently!
    wait_time = random.uniform(1.5, 4.5)
    print("********************")
    print("Beginning wait cycle for "+str(wait_time)+" seconds")
    time.sleep(wait_time)

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