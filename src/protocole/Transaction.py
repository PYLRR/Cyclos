# -*- coding: utf-8 -*-
class Transaction:
    """class used to describe transactions, which are sets of actions (linked to the roles smbdy plays in a protocol)"""

    # creates a transaction with a given label which describes it, often a letter (like alpha) and with a set of actions
    def __init__(self, label, actions):
        # string representing the transaction
        self.label = label
        # list of actions the transaction contains
        self.actions = actions

    # Currently unused. Checks transactions typlecompliance by recursively comparing actions in 2 transactions
    def isTypeCompliant(self, transaction2):
        for i in range(0, len(self.actions)):
            for j in range(0, len(transaction2.actions)):
                if not self.actions[i].isTypeCompliant(transaction2.actions[j]):
                    print("not unifiable")