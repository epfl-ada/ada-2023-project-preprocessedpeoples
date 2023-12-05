import os
import json
import xml.etree.ElementTree as ET
import gzip
import xmltodict
from tqdm import tqdm
import argparse
import copy
import multiprocessing as mp



def extract_corenlp_xml(filename):
    tree = ET.parse(gzip.open(filename))
    # xml to json
    xmlstr = ET.tostring(tree.getroot(), encoding="utf8", method="xml")
    data_dict = xmltodict.parse(xmlstr)
    return data_dict


def get_characters(file):
    characters = {}  # Dictionary to hold character information

    for sentence in file["root"]["document"]["sentences"]["sentence"]:
        if not isinstance(sentence, dict) or sentence.get("tokens") is None:
            continue

        entities = sentence.get("tokens", {}).get("token", [])

        # Extract entities and classify them as characters
        for entity in entities:
            if (
                type(entity) is dict
                and entity.get("NER") is not None
                and entity["NER"] == "PERSON"
            ):
                char_name = entity["word"]
                if char_name not in characters:
                    characters[char_name] = {}
    return characters


isValidIndex = lambda l, i: -len(l) <= i < len(l)


def get_character_mentions(file, characters):
    mentions = copy.deepcopy(characters)
    # clone characters
    if (
        file.get("root") is None
        or file["root"].get("document") is None
        or file["root"]["document"].get("coreference") is None
    ):
        return mentions
    for coreference in file["root"]["document"]["coreference"]["coreference"]:
        # find token
        if not isinstance(coreference, dict) or coreference.get("mention") is None:
            continue
        for mention in coreference["mention"]:
            # get sentence associated with the mention , -1 because sentence index in mention start from 1
            if not isinstance(
                file["root"]["document"]["sentences"]["sentence"], list
            ) or not isValidIndex(
                file["root"]["document"]["sentences"]["sentence"],
                int(mention["sentence"]) - 1,
            ):
                break
            sentence = file["root"]["document"]["sentences"]["sentence"][
                int(mention["sentence"]) - 1
            ]

            if (
                mention.get("@representative") is not None
                and mention.get("@representative") == "true"
            ):
                # check if token at index exist
                if not isinstance(
                    sentence["tokens"]["token"], list
                ) or not isValidIndex(
                    sentence["tokens"]["token"], int(mention["head"]) - 1
                ):
                    break
                # check if mention is a character
                token = sentence["tokens"]["token"][int(mention["head"]) - 1]["word"]
                if token not in mentions:
                    break

            if not isinstance(mentions, dict) or not isinstance(
                mentions[token], dict
            ):
                break

            if mentions[token].get("mentions") is None:
                mentions[token]["mentions"] = [mention]
            else:
                mentions[token]["mentions"].append(mention)

    return mentions


def get_mention_inverse_map(mentions):
    mention_inverse_map = {}
    for mention in mentions:
        if mentions[mention].get("mentions") is None:
            continue
        for m in mentions[mention]["mentions"]:
            if mention_inverse_map.get(int(m["sentence"])) is None:
                mention_inverse_map[int(m["sentence"])] = {}
            mention_inverse_map[int(m["sentence"])][int(m["head"])] = mention
    return mention_inverse_map


def get_mentioned_character(mention_inverse_map, sentence_id, token_id):
    if mention_inverse_map.get(sentence_id) is None:
        return None
    character = mention_inverse_map[sentence_id].get(token_id)
    return character


def add_dep(dependencies, sentence, dep, type, character, other, is_dependent):
    if dependencies.get(character) is None:
        dependencies[character] = {}
    if dependencies[character].get(type) is None:
        dependencies[character][type] = {}
    role = "dependant" if is_dependent else "governor"
    if dependencies[character][type].get(role) is None:
        dependencies[character][type][role] = []
    dependencies[character][type][role].append(other)


def get_dependencies(
    file, mentions, mention_inverse_map, dep_alg="collapsed-ccprocessed-dependencies"
):
    # get all types of dependencies
    types = set()
    if (
        file.get("root") is None
        or file["root"].get("document") is None
        or file["root"]["document"].get("sentences") is None
        or file["root"]["document"]["sentences"].get("sentence") is None
    ):
        return {}

    for sentence in file["root"]["document"]["sentences"]["sentence"]:
        if (
            not isinstance(sentence, dict)
            or sentence.get(dep_alg) is None
            or sentence[dep_alg].get("dep") is None
        ):
            continue
        for dep in sentence[dep_alg]["dep"]:
            if isinstance(dep, dict):
                types.add(dep["@type"])

    dependencies = {}

    for t in types:
        for sentence in file["root"]["document"]["sentences"]["sentence"]:
            if sentence.get(dep_alg) is None:
                continue

            for dep in sentence[dep_alg]["dep"]:
                if not isinstance(dep, dict) or dep.get("@type") != t:
                    continue

                character = get_mentioned_character(
                    mention_inverse_map,
                    int(sentence["@id"]),
                    int(dep.get("dependent").get("@idx")),
                )
                if character is not None:
                    other = sentence["tokens"]["token"][
                        int(dep.get("governor").get("@idx")) - 1
                    ]["lemma"]
                    if other in mentions:
                        continue
                    add_dep(dependencies, sentence, dep, t, character, other, True)

                character = get_mentioned_character(
                    mention_inverse_map,
                    int(sentence["@id"]),
                    int(dep.get("governor").get("@idx")),
                )
                if character is not None:
                    other = sentence["tokens"]["token"][
                        int(dep.get("dependent").get("@idx")) - 1
                    ]["lemma"]
                    if other in mentions:
                        continue
                    add_dep(dependencies, sentence, dep, t, character, other, False)

    return dependencies


def add_words(charcters, dependencies):
    for character in charcters:
        actions_taken = []
        actions_received = []
        possessions = []
        descriptions = []

        if dependencies.get(character) is None:
            continue
        for type in dependencies[character]:

            for role in dependencies[character][type]:
                for other in dependencies[character][type][role]:
                    if (
                        type == "agent"
                        and role == "dependant"
                        or type == "nsubj"
                        and role == "dependant"
                    ):
                        actions_taken.append(other)
                    if (
                        type == "dobj"
                        and role == "dependant"
                        or type == "nsubjpass"
                        and role == "dependant"
                    ):
                        actions_received.append(other)
                    if type == "poss" and role == "dependant":
                        possessions.append(other)
                    if (
                        type == "amod"
                        and role == "governor"
                        or type == "nn"
                        and role == "governor"
                    ):
                        descriptions.append(other)

        charcters[character]["actions_taken"] = actions_taken
        charcters[character]["actions_received"] = actions_received
        charcters[character]["possessions"] = possessions
        charcters[character]["descriptions"] = descriptions


def add_number_of_mentions(characters, mentions):
    for character in mentions:
        if mentions[character].get('mentions') is None:
            characters[character]['occurrences'] = 1
        else:
            characters[character]['occurrences'] = len(mentions[character]['mentions']) + 1


def process_file(file, directory):
    if not file.endswith(".xml.gz"):
        return

    movie_id = file.split(".")[0]

    parsed_file = extract_corenlp_xml(f"{directory}/corenlp_plot_summaries/{file}")
    characters = get_characters(parsed_file)
    mentions = get_character_mentions(parsed_file, characters)

    add_number_of_mentions(characters, mentions)

    mention_inverse_map = get_mention_inverse_map(mentions)
    dependencies = get_dependencies(parsed_file, mentions, mention_inverse_map)

    add_words(characters, dependencies)

    with open(f"{directory}/characters/{movie_id}.json", "w") as fp:
        json.dump(characters, fp)

def process_file_wrapper(args):
    file, directory = args
    return process_file(file, directory)

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", "-d", type=str, default="../dataset")
    # Load and parse the XML file
    directory = parser.parse_args(args).directory

    if not os.path.exists(directory + "/characters"):
        os.makedirs(directory + "/characters")

    # go through each file in the directory
    files = os.listdir(f"{directory}/corenlp_plot_summaries/")
    file_directory_pairs = [(file, directory) for file in files]

    pool = mp.Pool(mp.cpu_count())

    # tqdm can be integrated with imap for progress tracking
    for _ in tqdm(pool.imap_unordered(process_file_wrapper, file_directory_pairs), total=len(files)):
        pass

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
