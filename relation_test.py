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

def extract_date_relations(sentence):
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

    annotation = sentence["annotation"]
    text = sentence["text"]
    tagged_sentence = [(x[1], x[3], x[4]) for x in annotation]

    token_list = build_sentence_tree(tagged_sentence)
    cp = nltk.RegexpParser(birthdate, loop=2)
    # print(text)
    BIRTH_DATE_RELATION = cp.parse(token_list)
    # print(BIRTH_DATE_RELATION)
    # TREE = cp.parse(token_list)
    # #TREE.draw()
    # birth = nltk.RegexpParser(birthdate)
    # print(birth.parse(TREE))
    for subtree in BIRTH_DATE_RELATION.subtrees(filter=lambda t: t.label() == 'BIRTHDATE'):
        relation_dict = {}
        for nestedtree in subtree.subtrees(filter=lambda t: t.label() in ['PERSON', 'DATE']):
            if (nestedtree.label() == 'PERSON' and "PERSON" not in relation_dict):
                relation_dict["PERSON"] = [x[0] for x in getLeaves(nestedtree)]
            if (nestedtree.label() == 'DATE'):
                relation_dict["DATE"] = [x[0] for x in getLeaves(nestedtree)]
        if ("PERSON" in relation_dict and "DATE" in relation_dict):
            person = " ".join(relation_dict["PERSON"])
            date = " ".join(relation_dict["DATE"])
            rel = Relation(person, predicate, date)
            results.append(rel)
    return results

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
    # print(PARENT_RELATION)
    # print("Person List")
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