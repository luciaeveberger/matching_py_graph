import pandas as pd
from objects.UniversityGroups import UniversityGroups


def create_participants(participants_list):
    print(participants_list)
    external_requests = pd.DataFrame(participants_list)
    print(external_requests)
    print('total people', sum(external_requests['capacity']))
    university_list = []
    for index, row in external_requests.iterrows():
        university = UniversityGroups(int(row['id']), row['university'], int(row['capacity']))
        university_list.append(university)
    sorted_university = sorted(university_list, key=lambda x: x.get_participant_capacity(), reverse=True)
    return sorted_university
