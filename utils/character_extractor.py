import os
import json
import xml.etree.ElementTree as ET
import gzip
import xmltodict
from tqdm import tqdm


def extract_corenlp_xml(filename):
    tree = ET.parse(gzip.open(filename))
    # xml to json
    xmlstr = ET.tostring(tree.getroot(), encoding="utf8", method="xml")
    data_dict = xmltodict.parse(xmlstr)
    return data_dict


def get_character_names(file):
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


def get_character_mentions(file):
    # clone characters
    characters = get_character_names(file)
    if (
        file.get("root") is None
        or file["root"].get("document") is None
        or file["root"]["document"].get("coreference") is None
    ):
        return characters
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
                if token not in characters:
                    break

            if not isinstance(characters, dict) or not isinstance(
                characters[token], dict
            ):
                break

            if characters[token].get("mentions") is None:
                characters[token]["mentions"] = [mention]
            else:
                characters[token]["mentions"].append(mention)

    return characters


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


def parse_dependencies(dependencies):
    for character in dependencies:
        actions_taken = []
        actions_received = []
        possessions = []
        descriptions = []

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
        dependencies[character] = {
            "actions_taken": actions_taken,
            "actions_received": actions_received,
            "possessions": possessions,
            "descriptions": descriptions,
        }
    return dependencies


def main():
    # Load and parse the XML file
    directory = "../dataset/"

    if not os.path.exists(directory + "characters"):
        os.makedirs(directory + "characters")

    # go through each file in the directory
    for file in tqdm(os.listdir(f"{directory}corenlp_plot_summaries/")):
        # file ends with .xml.gz
        if file.endswith(".xml.gz"):
            # get the movie id
            movie_id = file.split(".")[0]
        else:
            continue

        parsed_file = extract_corenlp_xml(directory + file)
        mentions = get_character_mentions(parsed_file)

        mention_inverse_map = get_mention_inverse_map(mentions)
        dependencies = get_dependencies(parsed_file, mentions, mention_inverse_map)
        dependencies = parse_dependencies(dependencies)

        with open(f"{directory}characters/{movie_id}.json", "w") as fp:
            json.dump(dependencies, fp)


if __name__ == "__main__":
    main()
