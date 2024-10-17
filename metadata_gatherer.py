#!/bin/env python3
from convert import json_convert
from bs4 import BeautifulSoup
from io import BytesIO
from typing import TextIO
import requests, json, base64

# set the useragent to something related to the program
# TODO: allow the user to set this
headers = {"User-Agent": "link-brain-opengraph-spider"}


def crawl_img(url: str) -> str:
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        enc_img = base64.b64encode(r.content).decode("utf-8")
        return enc_img
    return Null


def crawl_metadata(url: str) -> dict:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    # I klepped this from somewhere. I'm not 100% clear on how it works.
    # From what I can tell, find_all() will cycle through every single meta tag.
    # The lambda then acts more like a wrapper to filter for "og:"
    # Then it dumps all the meta tags with "og:" to the tags var
    tags = soup.find_all(
        "meta", attrs={"property": lambda x: x and x.startswith("og:")}
    )
    json_tags = {}
    for tag in tags:
        json_tags[tag.get("property")] = tag.get("content")
        if tag.get("property") == "og:image":
            json_tags["og:image:base64"] = crawl_img(tag.get("content"))
    return json_tags


def get_metadata(json_object: dict) -> dict:
    bookjson = json_convert(json_object)
    for entry in bookjson:
        bookjson[entry]["metadata"] = crawl_metadata(bookjson[entry]["uri"])
    return bookjson


def get_metadata_raw(json_object: TextIO) -> dict:
    return get_metadata(json.load(json_object))


if __name__ == "__main__":
    f = open("/home/kali/Desktop/bookmarks-2024-10-03.json", "r")
    bookjson = get_metadata_raw(f)
    f.close()

    print(json.dumps(bookjson))
