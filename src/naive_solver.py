#!/usr/bin/env python3
## -*- coding:utf-8 -*-
##
## naive_solver.py
##
##  Creado por Mikel Molina.
#=========================================================================================0
import sys
from pysat.solvers import Solver
from itertools import product
import file_parser
import copy

class NaiveSolver:
    def __init__(self, qbf):
        """
        Constructor para la clase NaiveSolver.
        Inicializa el solucionador con un objeto QBF.
        """
        self.qbf = qbf

    def solve(self):

        """
        Método para resolver la QBF utilizando un el enfoque naíf.
        :return: true si la QBF es satisfacible, false si es insatisfacible.
        Para saber si su funcionamiento completo leer la memoria.
        """
        self.qbf.clauses = [set(clause) for clause in self.qbf.clauses if all(lit in clause and -lit not in clause for lit in clause)]
        while self.qbf.quantifiers and self.qbf.clauses:
            block = self.qbf.quantifiers.pop(0)
            quantifier = block[0]
            variables = block[1]
            if quantifier == 'a':
                if len(self.qbf.quantifiers) == 0:
                    for index in range(len(self.qbf.clauses)):
                        if not set([lit for lit in self.qbf.clauses[index] if abs(lit) not in variables]):
                           return False
                    return True
                old_qbf = copy.deepcopy(self.qbf)
                sign_combinations = product([-1, 1], repeat=len(variables))
                combinations =  [[l * sign for l, sign in zip(variables, signs)] for signs in sign_combinations]
                for combination in combinations:
                    new_clauses = []
                    for index in range(len(self.qbf.clauses)):
                        if any(lit in self.qbf.clauses[index] for lit in combination):
                            continue
                        new_clause = set([lit for lit in self.qbf.clauses[index] if -lit not in combination])
                        if not new_clause:
                            return False
                        new_clauses.append(new_clause)
                    self.qbf.clauses = new_clauses
                    result = self.solve()
                    if not result:
                        return False
                    self.qbf = copy.deepcopy(old_qbf)
            if quantifier == 'e':
                old_qbf = copy.deepcopy(self.qbf)
                models_iterator = Solver(bootstrap_with=self.qbf.clauses)
                if not models_iterator.solve():
                    return False
                for model in models_iterator.enum_models():
                    model_exists = set([model_var for model_var in model if abs(model_var) in variables])
                    models_iterator.add_clause([-lit for lit in model_exists])
                    self.qbf.clauses = [set([lit for lit in clause if -lit not in model_exists]) for clause in self.qbf.clauses if clause.isdisjoint(model_exists)]
                    if self.solve() == True:
                        return True
                    self.qbf = copy.deepcopy(old_qbf)
                return False
        return True