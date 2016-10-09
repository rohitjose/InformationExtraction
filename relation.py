# -*- coding: utf-8 -*-

# Relation Extraction Skeleton
# ==========================================
#
# Author: Jianbin Qin <jqin@cse.unsw.edu.au>

# THIS IS PART OF SKELETON
# DO NOT CHANGE THIS FILE

# Relation
class Relation:
    """
    The data class that holds one relation.
    """
    def __init__(self, subject, predicate, object):
        self._subject = subject
        self._predicate = predicate
        self._object = object

    @property
    def subject(self):
        return self._subject

    @property
    def predicate(self):
        return self._predicate

    @property
    def object(self):
        return self._object

    def __repr__(self):
        return '<' +self._subject + ' --' + self._predicate + '--> ' + self._object + '>'
