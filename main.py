import requests, json
from pprint import pprint
import pandas as pd
import gspread


def read_gsheet(key, sheet):
    gc=gspread.service_account(filename='creds.json')
    key_=key ### change to the sheets for regron
    ### Reading in the specific googles sheets file
    sh=gc.open_by_key(key_)
    sheet=sheet
    gs=sh.worksheet(sheet)
    #update_id = gs.cell(1, 2).value
    return gs

#### Reading the players list
players=pd.DataFrame(read_gsheet('16GZY3Di3UTQvk4ePKsiNNfpmbgyJvQbWRf_wXXXEF8U', 'Players').get_all_records())
print(players)


### taking list of ids
managers=list(players['entry'].astype(int))

all_=[]
for event in range(1, 39):
    for manager in managers:
        url=f'https://fantasy.premierleague.com/api/entry/{manager}/event/{event}/picks/'

        chips_used= requests.get(url).json().get('active_chip')
        s = requests.get(url).json().get('entry_history')
        if s==None:
            break
        s['chips']=chips_used
        s['player']=manager
        df=pd.json_normalize(s)
        all_.append(df)
df=pd.concat(all_)

df['weekly_net']=df['points']-df['event_transfers_cost']
df['month']=df['event']//4
df['monthly_points']=df.groupby([['player', 'month']])['weekly_net'].sum()
# df.to_excel("C:/Users/bisra/OneDrive/Desktop/_Scripts/_FPL_TG_integration/history_Fpl.xlsx")


### update the google sheet
data = [df.columns.values.tolist()] + df.values.tolist()

# Update Google Sheet
worksheet=read_gsheet('16GZY3Di3UTQvk4ePKsiNNfpmbgyJvQbWRf_wXXXEF8U', 'All_data')
worksheet.update("A1:" + gspread.utils.rowcol_to_a1(len(data), len(data[0])), data)


# ### Check 3

# ### points and transfers 
# manager_id=3143515
# url=f'https://fantasy.premierleague.com/api/entry/{manager_id}/history/'

# s = requests.get(url).json()['current']
# # print(s)


# ### chips ysed This is what I need
# manager_id=3143515
# event_id=2
# url=f'https://fantasy.premierleague.com/api/entry/{manager_id}/event/{event_id}/picks/'

# chips_used= requests.get(url).json().get('active_chip')
# s = requests.get(url).json().get('entry_history')

# print(chips_used)
# print(s)
# if s!=None:
#     df=pd.json_normalize(s)
#     df.to_excel("C:/Users/bisra/OneDrive/Desktop/_Scripts/_FPL_TG_integration/history_Fpl.xlsx")

##dfdf