import pandas as pd
import json

initial_list= list()
accommodations = pd.DataFrame.from_csv(
    '/Users/luciaeve/Documents/EMSE/code/matching_py_graph/POC-matching/data/WG.csv', encoding='latin-1',
    index_col=None, sep=',')
count = 520

for index, row in accommodations.iterrows():
    demo = {'_id':count, 'name': row['name'], 'address': row['name'], 'coordinates':'',
            'busZone':row['buz_zone'],'capacity': row['capacity'], 'isWG': 'true'}
    count = count + 1
    initial_list.append(demo)
print(json.dumps(initial_list))


