import os
import requests
import pandas as pd
import numpy as np
import json
import time
import random
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

act_list = 'data/all_films.csv'
act_file = pd.read_csv(act_list)['title_code'].values
out_file = 'data/mined_producers.csv'

def fetch_producer_data(film_code):
    try:
        #scrape IMDB
        url = 'https://imdb.com/title/'+film_code+'/fullcredits'
        resp = requests.request("GET", url) 
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find_all("table", {"class":"simpleCreditsTable"})
        prod_list = []
        for row in div:
            tr = row.find_all("tr")
            for t in tr:
                td = t.find_all("td")
                try:
                    if 'produce' in td[2].get_text():
                        prod_list.append([td[0].get_text().replace("\n",''),td[2].get_text().replace("\n",'')])
                        #print(td[0].get_text().replace("\n",''), td[2].get_text().replace("\n",''))
                except:
                    pass
        p1 = []
        for p in prod_list:
            if 'producer' in p[1]:
                p1 = p[0]
                break
        ep = []
        for p in prod_list:
            if 'executive producer' in p[1]:
                ep = p[0]
                break
        df = pd.DataFrame(columns=['title','producer','executive'])
        df.loc[0] = [film_code, p1, ep]
        return df
    except:
        return None

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

c=0
for act in act_file:
    c+=1
    if c > 7:
        c=0
        #os.system('cls' if os.name == 'nt' else 'clear')
    print("Fetching actor data for title: "+act)
    row = fetch_producer_data(act)
    if not isinstance(row, pd.DataFrame):
        w = random.uniform(2.2, 7.1)
        print("Encountered an error on title: "+act)
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
    m_lis = pd.read_csv(act_list, index_col=0)
    m_lis = m_lis[m_lis['title_code'] != act]
    m_lis.to_csv(act_list)
    print("Successfully removed the title from the working list: "+act+ " : "+ row['title'].values[0])
    print("Currenttotal records remaining to read : "+str(m_lis.shape[0]))


    print("*********************************")
    print(" ___ _   _  ___ ___ ___  ___ ___  ")
    print("/ __| | | |/ __/ __/ _ \/ __/ __| ")
    print("\__ \ |_| | (_| (_|  __/\__ \__ \ ")
    print("|___/\__,_|\___\___\___||___/___/ ")
    print("*********************************")


    #wait intelligently!
    #wait_time = random.uniform(0.1, 0.5)
    #print("********************")
    #print("Beginning wait cycle for "+str(wait_time)+" seconds")
    #time.sleep(wait_time)
    #print("Short cycle complete")
    #print("********************")

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