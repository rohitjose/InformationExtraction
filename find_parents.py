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
            if(iob[2:] in ["PERSON","DATE"]):
                if(label==iob[2:] or label==""):
                    label = iob[2:]
                    phrase.append(word)
                else:
                    token_list.append(nltk.Tree(label, phrase))
                    label = ""
                    phrase = []
                    phrase.append(word)

    if (phrase != []):
        token_list.append(nltk.Tree(label, phrase))

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
                            {<VB.><VB.><IN>?<PERSON>*}          # Chunk everything
                            {<VBN><IN>}
                			}<VBN><IN><PERSON>{
                          ADDNINFO:
                    		{<-LRB-><.|..|PERSON|DATE|BORN|PARENTS>*<-RRB->}
                          PARENTS:
                            {<IN><.|..|...|DATE|HYPH>*<PERSON><.|..|...|DATE|ADDNINFO|HYPH>*<CC>?<.|..|...|DATE|BORN|PRP.|HYPH>*<PERSON>?}
                    		{<BORN><IN><PERSON>}
                    		{<BORN|IN>*<PERSON><CC><PERSON>}
                    		{<DT|NN|IN|DATE>+<PERSON><CC>*<PERSON>*}
                          RELATION:
                            {<BORN>*<.|..|...|DATE|>*<PERSON><BORN>*<.|..|...|DATE|ADDNINFO|BORN|PRP.>*<PARENTS>}
                          """
    results = []
    predicate = "HasParent"

    annotation = sentence["annotation"]
    text = sentence["text"]
    tagged_sentence = [(x[1], x[3], x[4]) for x in annotation]

    token_list = build_sentence_tree(tagged_sentence)
    cp = nltk.RegexpParser(parents,loop=3)
    print(text)
    PARENT_RELATION = cp.parse(token_list)
    print(PARENT_RELATION)
    PARENT_RELATION.draw()
    print("Person List")
    relation_list = []
    # for subtree in PARENT_RELATION.subtrees(filter=lambda t: t.label() == 'RELATION'):
    #     subject = []
    #     parent_names = []
    #     ts = ()
    #     for info in subtree:
    #         if (type(info) != type(ts) and info.label() == 'PERSON'):
    #             subject.extend([x[0] for x in info.leaves()])
    #     for parents_rel in subtree.subtrees(filter=lambda t: t.label() == 'PARENTS'):
    #         for node in parents_rel:
    #             if(type(node)!= type(ts) and node.label()=='PERSON'):
    #                 parent_names.append(" ".join([x[0] for x in node.leaves()]))
    #     #print(subject)
    #     #print(parent_names)
    #     for name in parent_names:
    #         rel = Relation(" ".join(subject), predicate, name)
    #         relation_list.append(rel)
    return relation_list



filename = sys.argv[1]

data = load_data(filename)

for sentence in data:
    results = extract_parent_relations(sentence['sentence'])
    print(results)
