import pandas as pd
from objects.UniversityGroups import UniversityGroups


def create_participants():
    external_requests = pd.DataFrame.from_csv('/Users/luciaeve/Documents/EMSE/code/matching_py_graph/POC-matching/data/participants.csv', encoding='latin-1', index_col=None, sep=';')
    print('total people', sum(external_requests['number']))
    university_list = []
    for index, row in external_requests.iterrows():
        university = UniversityGroups(row.count(), row['university'], row['number'])
        university_list.append(university)
    sorted_university = sorted(university_list, key=lambda x: x.get_participant_capacity(), reverse=True)
    return sorted_university

#
# def create_replacement_participant(remainder_size):
#     UniversityGroups(200, )