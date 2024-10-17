from ast import literal_eval

content_text = """This is a test file.
I'm the dumbass writing his own markup language.
I know there is a markup language that is very similar to this but the internet sucks and everything is enshittified!"""
# markup_text = """>>>>>>>>>#>>>#
# v>>>>>>>>>>>>>>>>>>>>>>>>>>>->>-
# v>>>>>>>>>>+>>>>>>>>>>>>+>>>>>>>>>>>>>>->>-"""
markup_text = """(1,10)#:(1,14)#:(2,16)+:(2,22)+:(3,30)-:(3,40)-"""


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
    for x in markup:
        key = list(x.keys())[0]
        value = list(x.values())[0]
        msg_join = ''.join([content[key[0]-1][:key[1]-1],value,content[key[0]-1][key[1]-1:]])
        content[key[0]-1] = msg_join

    return ''.join(content)
        

        #for key in x.keys():
        #    print(content[key[0]-1][key[1]-1])

print(markup_engine(content_text, markup_text))
