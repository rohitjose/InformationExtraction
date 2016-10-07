import sys
import json
import os
import nltk

def load_data(filename):
    """
    This function read a json file and check if this data is a valid
    data file for 6714 16s2 project input file.
    :param filename:
    :return: A list of sentence records.
    """
    if not os.path.exists(filename):
        return None
    try:
        json_data = open(filename).read()
        data = json.loads(json_data)
        return data
    except IOError:
        print('Oops! {0} cannot open.'.format(filename))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def build_sentence_tree(tagged_sentence):
    """Builds the sentence tree based on the IOB tags for person and date"""
    phrase=[]
    label = ""
    token_list = []
    for token in tagged_sentence:
        iob = token[2]
        word = token[:-1]
        if(iob=='O'):
            if(phrase!=[]):
                token_list.append(nltk.Tree(label,phrase))
                label=""
                phrase=[]
                token_list.append(word)
            else:
                token_list.append(word)
        else:
            label = iob[2:]
            phrase.append(word)

    #print(token_list)
    return token_list

filename = sys.argv[1]

data = load_data(filename)

single = data

grammar = r"""
  BORN:
    {<VB.><VB.><IN>*}          # Chunk everything
    {<VBN><IN>}
  PARENTS:
    {<IN><PERSON><.|..|...|CARDINAL|ORDINAL>*<CC><.><.|..|...|CARDINAL|ORDINAL>*<PERSON>}
  """
birthdate = r"""
  BIRTHDATE:
    {<PERSON><.|..|...|CARDINAL|ORDINAL>*<BORN><.|..|...>*<DATE>}          # Chunk everything
    {<BORN><GPE|DATE><.|..|...|CARDINAL|ORDINAL>*<PERSON>}
  """

for sentence in single:
    annotation = sentence["sentence"]["annotation"]
    text = sentence["sentence"]["text"]
    tagged_sentence = [(x[1],x[3],x[4]) for x in annotation]
    #print(tagged_sentence)
    entity_tagging = nltk.ne_chunk(tagged_sentence, binary=False)
    #print(entity_tagging)
    # cp = nltk.RegexpParser(grammar)
    # print(cp.parse(entity_tagging))
    token_list = build_sentence_tree(tagged_sentence)
    cp = nltk.RegexpParser(grammar)
    print(text)
    #print(cp.parse(token_list))
    TREE = cp.parse(token_list)
    #TREE.draw()
    birth = nltk.RegexpParser(birthdate)
    print(birth.parse(TREE))

