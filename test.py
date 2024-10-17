from ast import literal_eval

content_text = """This is a test file.
I'm the dumbass writing his own markup language.
I know there is a markup language that is very similar to this but the internet sucks and everything is enshittified!"""
markup_text = """(1,10)#:(1,14)#:(2,16)+:(2,22)+:(3,30)-:(3,40)-:(1,8)+:(1,20)+"""


def token_parser(markup):
    tmp_dict = {}
    tmp_tuple = literal_eval(markup[:-1])
    tmp_dict[tmp_tuple] = markup[-1]
    return tmp_dict


def markup_parser(markup):
    markup = markup.split(":")
    for i, mark in enumerate(markup):
        markup[i] = token_parser(mark)
    return markup


def markup_engine(content, markup):
    content = content.splitlines()
    markup = markup_parser(markup)
    last_token = ""
    line_offset = {}
    for x in range(len(content)):
        line_offset[x] = 0
    for x in markup:
        key = list(x.keys())[0]
        value = list(x.values())[0]

        match value:
            case "#":
                if "#" == last_token:
                    msg_join = "".join(
                        [
                            content[key[0] - 1][: key[1] + line_offset[key[0] - 1]],
                            "</mark>",
                            content[key[0] - 1][key[1] + line_offset[key[0] - 1] :],
                        ]
                    )
                    line_offset[key[0] - 1] += 7
                else:
                    msg_join = "".join(
                        [
                            content[key[0] - 1][: key[1] - 1 + line_offset[key[0] - 1]],
                            "<mark>",
                            content[key[0] - 1][key[1] - 1 + line_offset[key[0] - 1] :],
                        ]
                    )
                    line_offset[key[0] - 1] += 6
                    last_token = "#"
            case "-":
                if "-" == last_token:
                    msg_join = "".join(
                        [
                            content[key[0] - 1][: key[1] + line_offset[key[0] - 1]],
                            "</u>",
                            content[key[0] - 1][key[1] + line_offset[key[0] - 1] :],
                        ]
                    )
                    line_offset[key[0] - 1] += 4
                else:
                    msg_join = "".join(
                        [
                            content[key[0] - 1][: key[1] - 1 + line_offset[key[0] - 1]],
                            "<u>",
                            content[key[0] - 1][key[1] - 1 + line_offset[key[0] - 1] :],
                        ]
                    )
                    line_offset[key[0] - 1] += 3
                    last_token = "-"
            case "+":
                if "+" == last_token:
                    msg_join = "".join(
                        [
                            content[key[0] - 1][: key[1] + line_offset[key[0] - 1]],
                            "</b>",
                            content[key[0] - 1][key[1] + line_offset[key[0] - 1] :],
                        ]
                    )
                    line_offset[key[0] - 1] += 4
                else:
                    msg_join = "".join(
                        [
                            content[key[0] - 1][: key[1] - 1 + line_offset[key[0] - 1]],
                            "<b>",
                            content[key[0] - 1][key[1] - 1 + line_offset[key[0] - 1] :],
                        ]
                    )
                    line_offset[key[0] - 1] += 3
                    last_token = "+"
        content[key[0] - 1] = msg_join
        # msg_join = "".join(
        #    [
        #        content[key[0] - 1][: key[1] - 1],
        #        value,
        #        content[key[0] - 1][key[1] - 1 :],
        #    ]
        # )
        # content[key[0] - 1] = msg_join

    return "".join(["<!DOCTYPE html><html><head></head><body>", "".join(content), "</body></html>"])


print(markup_engine(content_text, markup_text))
