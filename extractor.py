# -*- coding: utf-8 -*-

# Relation Extraction Skeleton
# ==========================================
#
# Author: Jianbin Qin <jqin@cse.unsw.edu.au>

from relation import Relation

def extract_date_of_birth(sentence):
    predicate = "DateOfBirth"
    results = []
    #print("called")
    ############################################################
    # Replace this part to your own code of extract DataOfBirth.
    #
    # If you identify one relation. Use the following code to add
    # into relations.

    # Naive Solution:
    from sample_solution import sample_extract_date_of_birth
    from relation_test import extract_date_relations
    # results.extend(sample_extract_date_of_birth(sentence))
    results.extend(extract_date_relations(sentence))
    #
    #   rel = Relation("Subject", predicate, "Object")
    #   results.append(rel)
    #
    ############################################################

    return results


def extract_has_parent(sentence):
    predicate = "HasParent"
    results = []

    ############################################################
    # Replace this part to your own code of extract HasParent.
    #
    # If you identify one relation. Use the following code to add
    # into relations.

    # Naive Solution:
    # from sample_solution import sample_extract_has_parent
    # results.extend(sample_extract_has_parent(sentence))
    from relation_test import extract_parent_relations
    results.extend(extract_parent_relations(sentence))

    #
    #   rel = Relation("Subject", predicate, "Object")
    #   results.append(rel)
    #
    ############################################################

    return results
