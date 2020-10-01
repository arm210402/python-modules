import json
import requests
a=input('enter:')
tuck=a.lower()
url='https://api.edamam.com/api/food-database/parser'
dicto={'ingr':tuck,'app_id':'9da01eca','app_key':'ee8d4ab344a9cb51681a0e198d995433'}
group=requests.get(url,params=dicto)
got=json.loads(group.text)
get=got['hints']
for i in get:
    first=i['food']['label']
    if first.lower()==tuck:
        print(i['food']['nutrients']['ENERC_KCAL'])
        break