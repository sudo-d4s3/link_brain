#!/bin/env python3
from ast import literal_eval


def token_parser(markup: str) -> dict:
    tmp_dict = {}
    tmp_tuple = literal_eval(markup[:-1])
    tmp_dict[tmp_tuple] = markup[-1]
    return tmp_dict


def markup_parser(markup: str) -> list:
    markup = markup.split(":")
    for i, mark in enumerate(markup):
        markup[i] = token_parser(mark)
    return markup


def markup_engine(content: str, markup: str) -> str:
    content = content.splitlines()
    for i, c in enumerate(content):
        content[i] = c.split()
    markup = markup_parser(markup)
    msg_join = ""
    for i, x in enumerate(markup):
        key = list(x.keys())[0]
        value = list(x.values())[0]

        match value:
            # '#' is highlight
            case "#":
                try:
                    if key[2]:
                        msg_join = f"<mark>{' '.join(content[key[0] - 1][key[1] - 1: key[2]])}</mark>"
                except:
                    msg_join = f"<mark>{content[key[0] - 1][key[1] - 1]}</mark>"
            # '-' is underline
            case "-":
                try:
                    if key[2]:
                        msg_join = f"<u>{' '.join(content[key[0] - 1][key[1] - 1: key[2]])}</u>"
                except:
                    msg_join = f"<u>{content[key[0] - 1][key[1] - 1]}</u>"
            # '+' is bold
            case "+":
                try:
                    if key[2]:
                        msg_join = f"<b>{' '.join(content[key[0] - 1][key[1] - 1: key[2]])}</b>"
                except:
                    msg_join = f"<b>{content[key[0] - 1][key[1] - 1]}</b>"
            # '*' is italics
            case "*":
                try:
                    if key[2]:
                        msg_join = f"<i>{' '.join(content[key[0] - 1][key[1] - 1: key[2]])}</i>"
                except:
                    msg_join = f"<i>{content[key[0] - 1][key[1] - 1]}</i>"
        try:
            if key[2]:
                line_msg_join = f"{' '.join(content[key[0]- 1][:key[1]-1])} {msg_join} {' '.join(content[key[0] - 1][key[2]:])}"
                line_msg_split = line_msg_join.split()
                content[key[0] - 1] = line_msg_split
        except:
            content[key[0] - 1][key[1] - 1] = msg_join
    # turn the sub lists into strings
    for i, c in enumerate(content):
        content[i] = " ".join(content[i])

    return "".join(
        [
            "<!DOCTYPE html><html><head></head><body>",
            "<br />".join(content),
            "</body></html>",
        ]
    )


if __name__ == "__main__":
    content_text = """This is a test file.
    I'm the dumbass writing his own markup language.
    I know there is a markup language that is very similar to this but the internet sucks and everything is enshittified!"""
    test_html = """<!DOCTYPE html><html><head></head><body>This is a <mark>test</mark> <b>file.</b><br />I'm the <mark>dumbass</mark> <b>writing</b> his <u>own</u> <i>markup</i> language.<br />I <mark>know</mark> there is a markup language <u>that is <i>very</i> similar</u> to this but the internet sucks and everything is enshittified!</body></html>"""
    markup_text = (
        """(1,4)#:(1,5)+:(2,3)#:(2,4)+:(2,6)-:(2,7)*:(3,2)#:(3,8,11)-:(3,10)*"""
    )
    assert markup_engine(content_text, markup_text) == test_html
    markup_text2 = (
        """(1,4)#:(1,5)+:(2,3)#:(2,4)+:(2,6)-:(2,7)*:(3,2)#:(3,10)*:(3,8,11)-"""
    )
    assert markup_engine(content_text, markup_text2) == test_html
    markup_text3 = (
        """(2,4)+:(1,4)#:(1,5)+:(2,3)#:(3,8,11)-:(2,6)-:(2,7)*:(3,2)#:(3,10)*"""
    )
    assert markup_engine(content_text, markup_text3) == test_html
