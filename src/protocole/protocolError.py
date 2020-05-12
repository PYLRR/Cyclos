# -*- coding: utf-8 -*-
class ProtocolError(Exception):
    """class used to describe errors in the protocol. Will be raised when there is a problem in its writing"""
    def __init__(self,msg=None):
        if msg is None:
            msg = "An error occurred in the protocol file."
        super(ProtocolError, self).__init__(msg)
