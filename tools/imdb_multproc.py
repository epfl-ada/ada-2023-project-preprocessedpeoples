from multiprocessing import Process
import numpy as np
import pandas as pd
from imdb import Cinemagoer

import shutil
import os


def get_imdb_data_process(df,k):
    imdb_responses=[]
    ia = Cinemagoer()
    for index,row in df.iterrows():
        try:
            imdb_responses.append(ia.get_movie(row['IMDB ID']))
        except:
            imdb_responses.append("Err: "+str(row["IMDB ID"]))
    pd.to_pickle(imdb_responses,f"imdb_resp/imdb_data_{k}.pkl")

def search_imdb_data_process(df,k):
    imdb_responses=[]
    ia = Cinemagoer()
    for index,row in df.iterrows():
        title=row['Movie name']; year=str(row["Movie release date"])[:4]
        search_query=f"{title} ({year})"
        try:
            imdb_responses.append(ia.search_movie(search_query)[0])
        except:
            imdb_responses.append("Err: "+search_query)
    pd.to_pickle(imdb_responses,f"imdb_resp/imdb_data_{k}.pkl")

def ret_imdb_data_parallel(N=10,dataset=None,retrieve_with="title"):
    
    batches=list(np.array_split(dataset.index, N))
    processes=[]
    
    if retrieve_with=="title":
        target_process=search_imdb_data_process
    else:
        target_process=get_imdb_data_process
    os.mkdir("imdb_resp")
    for k in range(N):
        p = Process(target=target_process, args=(dataset.loc[batches[k],:],k,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    results=[]
    for k in range(N):
        results=results+pd.read_pickle(f"imdb_resp/imdb_data_{k}.pkl")

    pd.to_pickle(results,"imdb_responses.pkl")
    shutil.rmtree('imdb_resp', ignore_errors=True)

    return results