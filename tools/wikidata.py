import requests

def sparql_query(query):
    endpoint_url = 'https://query.wikidata.org/sparql'

    response = requests.get(endpoint_url, params={'query': query, 'format': 'json'})

    return response.json()
    
def get_imdbid(freebase_id):
    query=f'''
    SELECT DISTINCT ?imdbid WHERE {{
        ?qid wdt:P646 "{freebase_id}".
        OPTIONAL {{ ?qid wdt:P345 ?imdbid. }}
        }}
    LIMIT 1
    '''
    response=sparql_query(query)

    return response["results"]["bindings"][0]["imdbid"]["value"]

def get_additional_data(freebase_id):
    query=f'''
    SELECT DISTINCT ?directorLabel ?screenwriterLabel ?assessmentLabel ?outcomeLabel WHERE {{
        ?qid wdt:P646 "{freebase_id}".
        OPTIONAL {{ ?qid wdt:P57 ?director. }}
        OPTIONAL {{ ?qid wdt:P58 ?screenwriter. }}
        OPTIONAL {{
            ?qid p:P5021 ?assessmentStatement.
            ?assessmentStatement ps:P5021 ?assessment.
            ?assessmentStatement pq:P9259 ?outcome.
            }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
    '''
    response=sparql_query(query)
    
    return_data={
        "directors":set(),
        "screenwriters":set(),
        "assessments":set()
    }
    for res in response["results"]["bindings"]:
        return_data["directors"].add(res["directorLabel"]["value"])
        return_data["screenwriters"].add(res["screenwriterLabel"]["value"])
        return_data["assessments"].add((res["assessmentLabel"]["value"],res["outcomeLabel"]["value"]))
    
    return return_data