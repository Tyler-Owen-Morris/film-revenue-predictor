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

act_list = 'data/actor_popularity_fetch_list.csv'
act_file = pd.read_csv(act_list)['actor'].values
out_file = 'data/actor_popularity_out.csv'

def fetch_actor_popularity(name_code):
    try:
        #scrape IMDB
        url = 'https://pro.imdb.com/'+name_code
        headers = {
            'Cookie':'''session-id=138-1311213-4138762; adblk=adblk_no; ubid-main=131-2177923-5330445; session-id-time=2218844129l; x-main="IS86HKXSJMigI0RnIigNqWd@Pu8ZQWgbXHTCS5NC44TGbsoydTDB4J3y0KW4qQJw"; at-main=Atza|IwEBILUkej479bl-hN19LhAyANxzITDWvKeBnZnnNNWk10j0SijTTrcP1xHYude5_tVJrzPsq30ehR12BnByawJoVpMhpgQ_hNpe0PYjxNHJTAQIAjOTF1wpOsTVFURmn8zA9cCV43yBuMIWlH9cQeyn7lV7Kdd47Hn--VPkHz_W88D4CZ-L1N-H-c-y65FUxELVH6R6EPnh830ssfLXG5L864QRO9hBDwKchx_d6hepwITlwuO8qetimWYabwo8Hty6QX5nZuKY2HNpCWmsakxByc50NIAp7Uy7_bZkvZW2sN8dK9kON4xPKIygVHhMWJQ6wh2-d0DykEh4BKAnSs8dTOaGBf2Wq33d5V4XKmz9RPhyup41DXR5DFVPQojnJoMGVNVo1hd_Xan63I94uYk1JEMN; sess-at-main="p9whlqJpRA5/kki0a+qwvIksIhZyceM2oTm2NUGUstA="; uu=BCYoQbsIiwfBoS5Z-9VBEM4GQeZlJd-x0dsY76F-NJiyuSyqzmSEMKbVSar_-kScSNRzLG9PNA9I%0D%0Ajdjov4ijeWrg0KYq7RquhDNrANLf2r_CKRWG40LVJlIVEtUtjfN7vlSPexThCyrlRCA6MaZXDAXU%0D%0APJiwN-Oy2Uileof_lGTBYNE%0D%0A; pa=BCYo5O3AftOw_UMyDZBOrkb5nNPu-MMicHEKRBry99NXBnJRqeW3prdQxa0PDs0tVA8QWusbH7tZ%0D%0Anraln_N9jpUhsHsZ_jxhsmPTLpuksiUytkmvL8ZfDM5RxRZzJUpLkDX6%0D%0A; session-token="FGBlsQXWFfNa1aXpisRWiZ24Zh7zfYgzF86EWr2infSQ/A6LyfZB++iPHpTBeYr2C2ZzH/C96D7YqEVAjt91KwKNDfhgKCBhgo3cwIzkZ9A2ZqntW/EE9MsAa8/KfK7XLvtj4lUy/nEmiyLVq9Gc2U6Exc1kovQN4H5GmkruH/ywN/ZwSmxBk1VEIqNKeSVbDDnA8JE2OJXuKQNPFsmu5kLk62fEK2cMJMb1pQZw6rU="; csm-hit=tb:FVQ9NP1114J2DT3PZ86C+s-WXASZQ2TS1F9RJ5CAPX5|1588207251592&t:1588207251592&adb:adblk_no"'''
        }
        resp = requests.request("GET", url, headers=headers) 
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", {"id": "popularity_widget"})
        act = div.find("a", {"class": "a-size- a-align- a-link- clickable_share_link"})
        df = pd.DataFrame(columns=['actor','popularity'])
        df.loc[0] = [name_code, int(act.text.replace('\n', '').replace(' ', '').replace(',', ''))]
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

#c=0
for act in act_file:
    # c+=1
    # if c > 7:
    #     c=0
    #     os.system('cls' if os.name == 'nt' else 'clear')
    print("Fetching actor data for title: "+act)
    row = fetch_actor_popularity(act)
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
    print("Appending retrieved information for: "+ str(row['popularity'].values[0]))
    out_df = pd.read_csv(out_file, index_col=0)
    out_df.append(row).to_csv(out_file)
    print("Save to file succeeded. Current record stored count : " + str(out_df.shape[0]))

    #update the master-list that this title is complete.
    m_lis = pd.read_csv(act_list, index_col=0)
    m_lis = m_lis[m_lis['actor'] != act]
    m_lis.to_csv(act_list)
    print("Successfully removed the title from the working list: "+act+ " : "+ str(row['popularity'].values[0]))
    print("Currenttotal records remaining to read : "+str(m_lis.shape[0]))

    print('''  .-')                                       ('-.    .-')     .-')    
 ( OO ).                                   _(  OO)  ( OO ).  ( OO ).  
(_)---\_) ,--. ,--.     .-----.   .-----. (,------.(_)---\_)(_)---\_) 
/    _ |  |  | |  |    '  .--./  '  .--./  |  .---'/    _ | /    _ |  
\  :` `.  |  | | .-')  |  |('-.  |  |('-.  |  |    \  :` `. \  :` `.  
 '..`''.) |  |_|( OO )/_) |OO  )/_) |OO  )(|  '--.  '..`''.) '..`''.) 
.-._)   \ |  | | `-' /||  |`-'| ||  |`-'|  |  .--' .-._)   \.-._)   \ 
\       /('  '-'(_.-'(_'  '--'\(_'  '--'\  |  `---.\       /\       / 
 `-----'   `-----'      `-----'   `-----'  `------' `-----'  `-----'  ''')


print("  .-')              _  .-')             _ (`-.  .-') _                                 _   .-')      _ (`-.              ('-.   .-') _     ('-.  ,---. ")
print(" ( OO ).           ( \( -O )           ( (OO  )(  OO) )                               ( '.( OO )_   ( (OO  )           _(  OO) (  OO) )  _(  OO) |   | ")
print("(_)---\_)   .-----. ,------.  ,-.-')  _.`     \/     '._          .-----.  .-'),-----. ,--.   ,--.)_.`     \ ,--.     (,------./     '._(,------.|   | ")
print("/    _ |   '  .--./ |   /`. ' |  |OO)(__...--''|'--...__)        '  .--./ ( OO'  .-.  '|   `.'   |(__...--'' |  |.-')  |  .---'|'--...__)|  .---'|   | ")
print("\  :` `.   |  |('-. |  /  | | |  |  \ |  /  | |'--.  .--'        |  |('-. /   |  | |  ||         | |  /  | | |  | OO ) |  |    '--.  .--'|  |    |   | ")
print(" '..`''.) /_) |OO  )|  |_.' | |  |(_/ |  |_.' |   |  |          /_) |OO  )\_) |  |\|  ||  |'.'|  | |  |_.' | |  |`-' |(|  '--.    |  |  (|  '--. |  .' ")
print(".-._)   \ ||  |`-'| |  .  '.',|  |_.' |  .___.'   |  |          ||  |`-'|   \ |  | |  ||  |   |  | |  .___.'(|  '---.' |  .--'    |  |   |  .--' `--'  ")
print("\       /(_'  '--'\ |  |\  \(_|  |    |  |        |  |         (_'  '--'\    `'  '-'  '|  |   |  | |  |      |      |  |  `---.   |  |   |  `---..--.  ")
print(" `-----'    `-----' `--' '--' `--'    `--'        `--'            `-----'      `-----' `--'   `--' `--'      `------'  `------'   `--'   `------''--'  ")