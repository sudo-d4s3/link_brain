#!/bin/env python3
import json
from typing import TextIO
from datetime import datetime


def flatten_json(json_object: dict) -> dict:
    out = {}

    def flatten(json_entry, name=""):
        if type(json_entry) is dict:
            for entry in json_entry:
                flatten(json_entry[entry], name + entry + "_")

        elif type(json_entry) is list:
            i = 0
            for entry in json_entry:
                flatten(entry, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = json_entry

    flatten(json_object)
    return out


def flat_list_lookup(flat_json: dict) -> list:
    # Bulid list of keys relavent to our new dict
    tmp_list = []
    for k, v in flat_json.items():
        # We are using uri as the key since bookmarks are inherently link oriented
        # Only the actual bookmark will have a url
        if "uri" in k:
            tmp_list.append(k)

    return tmp_list


def json_dict_builder(flat_list: list, flat_json_object: dict) -> dict:
    new_dict = {}
    for item in flat_list:
        try:
            # Creating a dict with the information we want including tags
            new_dict[flat_json_object[f"{item[:-3]}title"]] = {
                "uri": flat_json_object[f"{item[:-3]}uri"],
                "dateAdded": flat_json_object[f"{item[:-3]}dateAdded"],
                "lastModified": flat_json_object[f"{item[:-3]}lastModified"],
                "tags": flat_json_object[f"{item[:-3]}tags"].split(","),
            }
        except:
            # Creating a dict with the information we want including making tags empty
            new_dict[flat_json_object[f"{item[:-3]}title"]] = {
                "uri": flat_json_object[f"{item[:-3]}uri"],
                "dateAdded": flat_json_object[f"{item[:-3]}dateAdded"],
                "lastModified": flat_json_object[f"{item[:-3]}lastModified"],
                "tags": [],
            }

    return new_dict


def json_convert(old_json_object: dict) -> dict:
    flattened_json = flatten_json(old_json_object)
    list_lookup = flat_list_lookup(flattened_json)
    new_dict = json_dict_builder(list_lookup, flattened_json)
    return new_dict


def raw_json_convert(old_json_file: TextIO) -> dict:
    return json_convert(json.load(old_json_file))


if __name__ == "__main__":
    f = open("/home/kali/Desktop/bookmarks-2024-10-03.json", "r")
    flat_bookjson = flatten_json(json.load(f))
    f.close()

    list_lookup = flat_list_lookup(flat_bookjson)
    new_dict = json_dict_builder(list_lookup, flat_bookjson)
    print(json.dumps(new_dict))
