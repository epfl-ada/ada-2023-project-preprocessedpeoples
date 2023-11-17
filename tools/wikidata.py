import requests
from multiprocessing import Process
import numpy as np
import pandas as pd
import time 

import shutil
import os


def sparql_query(query):
    endpoint_url = 'https://query.wikidata.org/sparql'

    response = requests.get(endpoint_url, params={'query': query, 'format': 'json'})

    return response
    
def get_imdbid(freebase_id):
    query=f'''
    SELECT DISTINCT ?imdbid WHERE {{
        ?qid wdt:P646 "{freebase_id}".
        OPTIONAL {{ ?qid wdt:P345 ?imdbid. }}
        }}
    LIMIT 1
    '''
    response=sparql_query(query).json()

    return response["results"]["bindings"][0]["imdbid"]["value"]

def get_assessment_data_imdb(imdb_id):
    query=f'''
    SELECT DISTINCT ?assessmentLabel ?outcomeLabel WHERE {{
        ?qid wdt:P345 "{imdb_id}".
        OPTIONAL {{
            ?qid p:P5021 ?assessmentStatement.
            ?assessmentStatement ps:P5021 ?assessment.
            ?assessmentStatement pq:P9259 ?outcome.
            }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
    '''

    while True:
        response = sparql_query(query)
        if response.status_code!=429:
            break
        time.sleep(1)
    if response.status_code!=200:
        raise Exception(f"status code: {response.status_code}")
    response=response.json()
    
    return_data={
        "assessments":set()
    }
    for res in response["results"]["bindings"]:
        return_data["assessments"].add((res["assessmentLabel"]["value"],res["outcomeLabel"]["value"]))
    
    return return_data


def get_wd_assessments_process(df,k):
    results=[]
    for index,row in df.iterrows():
        try:
            results.append(get_assessment_data_imdb(row["imdb_id"]))
        except Exception as e:
            results.append("Error: "+str(index)+" "+e.__str__())
    
    pd.to_pickle(results,f"wikidata_resp/wd_data_{k}.pkl")


def ret_wikidata_data_parallel(N=10,dataset=None):
    batches=list(np.array_split(dataset.index, N))
    processes=[]
    

    os.mkdir("wikidata_resp")
    for k in range(N):
        p = Process(target=get_wd_assessments_process, args=(dataset.loc[batches[k],:],k,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    results=[]
    for k in range(N):
        results=results+pd.read_pickle(f"wikidata_resp/wd_data_{k}.pkl")

    pd.to_pickle(results,"wikidata_responses.pkl")
    shutil.rmtree('wikidata_resp', ignore_errors=True)

    return results