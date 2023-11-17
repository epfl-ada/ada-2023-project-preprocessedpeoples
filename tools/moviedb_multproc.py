from multiprocessing import Pool,Process, Queue, log_to_stderr
import numpy as np
import pandas as pd
from imdb import Cinemagoer

import time
import shutil
import os

from dotenv import load_dotenv
load_dotenv()


import requests

def fetch_movie_data(imdb_id,access_token):
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json;charset=utf-8"
    }

    find_url = f"https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id"
    
    while True:
        response = requests.get(find_url, headers=headers)
        if response.status_code!=429:
            break
        time.sleep(1)

    if response.status_code != 200:
        print(f"Error fetching movie data: {response.status_code}, {response.text}")
        return None

    movie = response.json().get('movie_results', [{}])
    if not movie:
        print(f"No movie found for IMDb ID: {imdb_id}")
        return None
    movie_id = movie[0].get('id')

    if not movie_id:
        return None

    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    
    while True:
        credits_response = requests.get(credits_url, headers=headers)
        if credits_response.status_code!=429:
            break
        time.sleep(1)
    
    if credits_response.status_code != 200:
        print(f"Error fetching credits data: {credits_response.status_code}, {credits_response.text}")
        return None

    credits = credits_response.json()

    return {
        'title': movie[0].get('title'),
        'cast': credits.get('cast', []),
        'crew': credits.get('crew', [])
    }

def get_moviedb_data_process(df,k,access_token=None):
    if not access_token:
        access_token=os.environ.get("moviedb_access_token")
    results=[]
    for index,row in df.iterrows():
        try:
            results.append(fetch_movie_data(row["imdb_id"],access_token))
        except:
            results.append("Error: "+str(index))
    pd.to_pickle(results,f"moviedb_resp/moviedb_data_{k}.pkl")


def ret_moviedb_data_parallel(N=10,dataset=None,retrieve_with="title"):
    access_token=os.environ.get("moviedb_access_token")
    
    batches=list(np.array_split(dataset.index, N))
    processes=[]
    

    os.mkdir("moviedb_resp")
    for k in range(N):
        p = Process(target=get_moviedb_data_process, args=(dataset.loc[batches[k],:],k,access_token,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    results=[]
    for k in range(N):
        results=results+pd.read_pickle(f"moviedb_resp/moviedb_data_{k}.pkl")

    pd.to_pickle(results,"moviedb_responses.pkl")
    shutil.rmtree('moviedb_resp', ignore_errors=True)

    return results