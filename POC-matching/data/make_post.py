import pandas as pd


def read_from_source():
    participants = pd.DataFrame.from_csv(
        '/Users/luciaeve/Documents/EMSE/code/matching_py_graph/POC-matching/data/participants.csv', encoding='latin-1',
        index_col=None, sep=';')
    return participants


def make_json():
    participants = read_from_source()
    print(participants)
    participant_list = []
    for index, row in participants.iterrows():
        demo = {"university": row['university'],
            "capacity": row['number']}
        participant_list.append(demo)
    print(participant_list)

if __name__ == "__main__":
    make_json()