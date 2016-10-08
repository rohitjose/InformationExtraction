import sys
import json
import os
import nltk
from relation import Relation

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

def extract_parent_relations(sentence):
    parents = r"""
      BORN:
        {<VB.><VB.><PERSON>*}          # Chunk everything
        {<VBN><IN>}
      ADDNINFO:
		{<-LRB-><.|..>*<PERSON|DATE>*<-RRB->}
      PARENTS:
        {<IN><.|..|...|DATE|NORP|HYPH|CARDINAL|ORDINAL>*<PERSON><.|..|...|DATE|ADDNINFO>*<CC><.|..|...|DATE>*<PERSON>}
      RELATION:
        {<BORN>*<.|..|...|DATE|NORP|>*<PERSON><BORN>*<.|..|...|DATE|NORP|ADDNINFO|LOCATION|WORK_OF_ART|CARDINAL>*<PARENTS>}
      """
    results = []
    predicate = "HasParent"

    annotation = sentence["annotation"]
    text = sentence["text"]
    tagged_sentence = [(x[1], x[3], x[4]) for x in annotation]

    token_list = build_sentence_tree(tagged_sentence)
    cp = nltk.RegexpParser(parents,loop=3)
    #print(text)
    PARENT_RELATION = cp.parse(token_list)
    print(PARENT_RELATION)
    print("Person List")
    relation_list = []
    for subtree in PARENT_RELATION.subtrees(filter=lambda t: t.label() == 'RELATION'):
        #print(subtree.leaves())
        person_list = []
        for person in subtree.subtrees(filter=lambda t: t.label() == 'PERSON' and t.label()!='ADDNINFO'):
            person_list.append(" ".join([x[0] for x in getLeaves(person)]))
        #print(person_list)
        if(person_list!=[]):
            subject = person_list[0]
            for parent in person_list[1:]:
                rel = Relation(subject, predicate, parent)
                relation_list.append(rel)
    if(len(relation_list)==3):
        del relation_list[1]
    return relation_list


filename = sys.argv[1]

data = load_data(filename)

for sentence in data:
    results = extract_parent_relations(sentence['sentence'])
    print(results)
