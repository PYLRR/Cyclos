# -*- coding: utf-8 -*-
class Term:
    """abstract class used to describe terms, which can be cryptographic primitives or types"""

    # creates a term knowing its parent
    def __init__(self, parent=None):
        # primitivte which contains this term, if root it doesn't exist and hence is None
        self.parent = parent

