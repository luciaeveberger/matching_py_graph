import pandas as pd
from objects.UniversityGroups import UniversityGroups


def create_participants(participants_list):

    external_requests = pd.DataFrame(participants_list)

    university_list = []
    for index, row in external_requests.iterrows():
        university = UniversityGroups((row['id']), row['university'], int(row['capacity']))
        university_list.append(university)
    sorted_university = sorted(university_list, key=lambda x: x.get_participant_capacity(), reverse=True)
    return sorted_university
