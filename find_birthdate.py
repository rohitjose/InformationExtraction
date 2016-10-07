import sys
import json
import os
import nltk
from relation import Relation

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

def getLeaves(tree):
    entity=[]
    for leave in tree.leaves():
        entity.append(leave)
    return entity

filename = sys.argv[1]

data = load_data(filename)

single = data

parents = r"""
  PARENTS:
    {<IN><.|..|...|DATE>*<PERSON><.|..|...|DATE|-.RB->*<CC><.|..|...|DATE>*<PERSON>}
  """
birthdate = r"""
  BORN:
    {<VB.><VB.><IN|PERSON>*}          # Chunk everything
    {<VBN><IN>}
  BIRTHDATE:
    {<PERSON><.|..|...|CARDINAL|ORDINAL>*<BORN><.|..|...>*<DATE>}          # Chunk everything
    {<BORN><GPE|DATE>*<.|..|...|DATE|CARDINAL|ORDINAL>*<PERSON>}
  """
results = []
predicate = "DateOfBirth"
for sentence in single:
    annotation = sentence["sentence"]["annotation"]
    text = sentence["sentence"]["text"]
    tagged_sentence = [(x[1],x[3],x[4]) for x in annotation]

    token_list = build_sentence_tree(tagged_sentence)
    cp = nltk.RegexpParser(birthdate,loop=2)
    #print(text)
    BIRTH_DATE_RELATION  = cp.parse(token_list)
    #print(BIRTH_DATE_RELATION)
    # TREE = cp.parse(token_list)
    # #TREE.draw()
    # birth = nltk.RegexpParser(birthdate)
    # print(birth.parse(TREE))
    for subtree in BIRTH_DATE_RELATION.subtrees(filter=lambda t: t.label() =='BIRTHDATE'):
        relation_dict={}
        for nestedtree in subtree.subtrees(filter=lambda t: t.label() in ['PERSON','DATE']):
            if(nestedtree.label()=='PERSON' and "PERSON" not in relation_dict):
                relation_dict["PERSON"] = [x[0] for x in getLeaves(nestedtree)]
            if(nestedtree.label()=='DATE'):
                relation_dict["DATE"] = [x[0] for x in getLeaves(nestedtree)]
        if("PERSON" in relation_dict and "DATE" in relation_dict):
            person = " ".join(relation_dict["PERSON"])
            date = " ".join(relation_dict["DATE"])
            rel = Relation(person, predicate, date)
        else:
            print(text)
            #print(BIRTH_DATE_RELATION)
        results.append(rel)

print(results)




