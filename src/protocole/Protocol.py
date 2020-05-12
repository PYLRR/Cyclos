# -*- coding: utf-8 -*-
from src.protocole.Action import Action
from src.protocole.Variable import Variable
from src.protocole.protocolError import ProtocolError


class Protocol:
    """class used to describe the protocol"""

    # Creates a protocol with a given name, a list of types, transactions and variables
    def __init__(self, name="", listTyp=[], listTrans=[], listVar=[]):
        self.listTypes = listTyp
        self.listTransactions = listTrans
        self.listVar = listVar
        self.name = name

    # erases the lists describing the protocol
    def reset(self):
        self.listTypes = []
        self.listTransactions = []
        self.listVar = []

    # returns the type if it is present in the list (typeName is a string or another type), none otherwise
    def getTypeInlist(self, typeName):
        # rightTypeDeclared represents the already defined type that this variable has
        rightTypeDeclared = None
        for typeDeclared in self.listTypes:
            if typeDeclared.sameName(typeName):
                rightTypeDeclared = typeDeclared
        return rightTypeDeclared

    # returns the variable if it is present in the list (typeName is a string or another type), none otherwise
    def getVarInlist(self, typeName):
        # rightVarDeclared represents the already defined var
        rightVarDeclared = None
        for varDeclared in self.listVar:
            if varDeclared.sameName(typeName):
                rightVarDeclared = varDeclared
        return rightVarDeclared

    def build_dependencies(self):

        all_actions = self.transactions_in_actions()
        nb_actions = len(all_actions)

        # data dependencies
        mat_data = [['-1' for n in range(nb_actions)] for m in range(nb_actions)]

        j = 0
        for i in range(nb_actions):
            if all_actions[i].type:
                for action_out in all_actions:
                    if not action_out.type:
                        rho_out = action_out.rho()
                        rho_in = all_actions[i].rho()
                        for a in rho_in:
                            for b in rho_out:
                                if a.equals(b[0][0]):
                                    if mat_data[i][j] == '-1':
                                        mat_data[i][j] = str(b[0][1])
                                    else:
                                        if str(b[0][1]) not in mat_data[i][j].split(";"):
                                            mat_data[i][j] += ';' + str(b[0][1])
                    j += 1
            j = 0

        """for i in range(nb_actions):
            print(mat_data[i])
            print('\n')"""

        # key dependencies
        mat_key = [['-1' for n in range(nb_actions)] for m in range(nb_actions)]

        j = 0
        for i in range(nb_actions):
            if not all_actions[i].type:
                for b in all_actions:
                    if not b.type and b != all_actions[i]:
                        rho_out_a = all_actions[i].rho()
                        rho_out_b = b.rho()
                        for ra in rho_out_a:
                            if ra[1][0] != 0 or ra[1][1] != 0:
                                for rb in rho_out_b:
                                    if rb[0][0] == ra[1][0] or rb[0][0] == ra[1][1]:
                                        if mat_data[i][j] == '-1':
                                            mat_key[i][j] = str(rb[0][1])
                                        else:
                                            mat_data[i][j] += ';' + str(rb[0][1])
                    j += 1
            j = 0

        """for i in range(nb_actions):
            print(mat_key[i])
            print('\n')"""

        # sequential dependencies
        mat_seq = [['0' for n in range(nb_actions)] for m in range(nb_actions)]

        for a in self.listTransactions:
            for i in range(nb_actions):
                for j in range(nb_actions - 1):
                    if (all_actions[i] in a.actions) & (all_actions[j] in a.actions) \
                            & (all_actions[i] == all_actions[j + 1]):
                        mat_seq[i][j] = '1'

        """for i in range(nb_actions):
            print(mat_seq[i])
            print('\n')"""

        return [mat_seq, mat_data, mat_key]

    def refining(self):
        matrices = self.build_dependencies()

        mat_seq = matrices[0]
        mat_data = matrices[1]
        mat_key = matrices[2]

        #self.print_matrices(mat_data)

        marking1 = []
        marking2 = []
        self.marking_first_criteria(marking1)
        self.marking_second_criteria(marking2)

        for [l2, p2] in marking1:
            self.erase_data(mat_data, l2, p2)

        for [l2, p2] in marking2:
            self.erase_seq(mat_seq, mat_data, l2, p2)
            self.erase_data(mat_data, l2, p2)
            self.erase_key(mat_key, mat_data, l2, p2)

        #self.print_matrices(mat_data)
        return [mat_seq, mat_data, mat_key]

    def erase_seq(self, mat, data, l2, pos):
        for l1 in range(len(mat)):
            dep = mat[l2][l1]
            if dep != '0':
                list_dep = data[l1][l2]
                new_dep = list_dep
                for elem in list_dep.split(";"):
                    if elem == str(pos):
                        new_dep = '-1'
                data[l1][l2] = new_dep

    def erase_data(self, mat, l2, pos):
        for l1 in range(len(mat)):
            dep = mat[l1][l2]
            if dep != '-1':
                list_dep = mat[l1][l2].split(";")
                for elem in list_dep:
                    if elem == str(pos):
                        if len(list_dep) == 1:
                            mat[l1][l2] = '-1'
                        else:
                            list_dep.remove(elem)
                            mat[l1][l2] = ';'.join(str(e) for e in list_dep)

    def erase_key(self, mat, data, l2, pos):
        for l1 in range(len(mat)):
            dep = mat[l1][l2]
            if dep != '-1':
                list_dep = data[l1][l2].split(";")
                for elem in list_dep:
                    if elem == str(pos):
                        if len(list_dep) == 1:
                            mat[l1][l2] = '-1'
                        else:
                            list_dep.remove(elem)
                            mat[l1][l2] = ';'.join(str(e) for e in list_dep)

    """
    calcul du rho_out pour toutes les actions out, et markage de charque element du rho_out public
    marking = [i, j[1] ] avec i numéro de l'action et j[1] position de l'élément marqué dans l'action 
    """
    def marking_first_criteria(self, marking):
        all_actions = self.transactions_in_actions()
        nb_actions = len(all_actions)
        for i in range(nb_actions):
            if not all_actions[i].type:
                rho_out_a = all_actions[i].getArguments()
                for j in rho_out_a:
                    if j[0].isPublic():
                        marking.append([i, j[1]])

        """for m in marking:
            print(m[0])
            print('----')
            print(m[1])
            print('\n')"""

        return marking

    def marking_second_criteria(self, marking):
        matrices = self.build_dependencies()
        mat_seq = matrices[0]
        all_actions = self.transactions_in_actions()
        nb_actions = len(all_actions)
        for i in range(nb_actions):
            for j in range(nb_actions):
                if mat_seq[i][j] == '1':  # i --> j dep sequential
                    rho_out_a = []
                    rho_out_b = []
                    all_actions[i].rootTerm.rho_out(rho_out_a, 0, 0, True, True)  # "out"
                    all_actions[j].rootTerm.rho_out(rho_out_b, 0, 0, True, True)  # "in"
                    for a in rho_out_a:
                        for b in rho_out_b:
                            if a[0][0].equals(b[0][0]):
                                if a[1][0] != 0:
                                    if a[1][0].check_inclusion(b[1][1]):
                                        marking.append([i, a[0][1]])
                                if a[1][1] != 0:
                                    if a[1][1].check_inclusion(b[1][1]):
                                        marking.append([i, a[0][1]])
                                else:
                                    marking.append([i, a[0][1]])

        """for m in marking:
            print(m[0])
            print('----')
            print(m[1])
            print('\n')"""

    # returns the list of all actions in the protocol
    def transactions_in_actions(self):
        all_actions = []
        for t in self.listTransactions:
            for a in t.actions:
                all_actions.append(a)

        return all_actions

    # returns a specific action
    def getAction(self, i):
        return self.transactions_in_actions()[i]

    # utility function used to print a matrice
    def print_matrices(self, mat):
        for i in range(len(mat)):
            print(mat[i])
            print('\n')
        print('--------')

    # Currently unused because dooesn't work well. Checks typlecompliance of the whole protocol by recursively
    # comparing its elements (transactions first)
    def testTypeCompliance(self):
        print("Type Compliance")
        for i in range(0, len(self.listTransactions)):
            for j in range(i+1, len(self.listTransactions)):
                print("i= " + str(i) + "; j= " + str(j))
                if self.listTransactions[i].isTypeCompliant(self.listTransactions[j]):
                    pass
                    #return True #If one is typeCompliant OK
