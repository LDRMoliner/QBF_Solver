#!/usr/bin/env python3
## -*- coding:utf-8 -*-
##
## bica_solver.py
##
##  Creado por Mikel Molina.
#=========================================================================================0


from __future__ import print_function
from forqes import Forqes
from primer import Primer
import socket
import sys
from file_parser import QBF
import atexit
import os
import signal

def create_negation(pfname, temp_files):
    """
        Encodes the negation of the input CNF formula.
    """

    nofv = 0
    cnf_pos = []
    # print(pfname)
    comment_pos = -1  # there is no line 'c n orig vars' in the file
    for i, line in enumerate(open(pfname, 'r')):
        if line[0] != 'p' and line[0] != 'c':
            cl = [int(l) for l in line.split()[:-1]]
            nofv = max([abs(l) for l in cl] + [nofv])

            cnf_pos.append(cl)
        elif line[:13] == 'c n orig vars':
            nofv_orig = int(line[13:].strip())
            comment_pos = i
    fname = '{0}.{1}@{2}'.format(os.path.basename(pfname[0])[:-4], os.getpid(),
                                 socket.gethostname())

    if comment_pos == -1 or nofv != nofv_orig:
        pos = '{0}-p.cnf'.format(fname)
        temp_files.append(pos)
        try:
            with open(pos, 'w') as fp:
                print('c n orig vars', nofv, file=fp)
                print('p cnf', nofv, len(cnf_pos), file=fp)
                for cl in cnf_pos:
                    print(' '.join([str(l) for l in cl]), '0', file=fp)
        except IOError as e:
            sys.stderr.write('\033[31;1mERROR:\033[m Unable to write file {0}.\n'.format(pos))
            sys.stderr.write('\033[33m' + str(e) + '\033[m\n')
            sys.exit(1)
    else:
        pos = pfname

    neg = '{0}-n.cnf'.format(fname)
    temp_files.append(neg)

    try:
        with open(neg, 'w') as fp:
            print('c n orig vars', nofv, file=fp)

            cl_fin = []
            cnf_neg = []
            for cl in cnf_pos:
                if len(cl) > 1:
                    nofv += 1
                    cnf_neg.append(cl + [-nofv])

                    for l in cl:
                        cnf_neg.append([-l, nofv])

                    cl_fin.append(-nofv)
                else:
                    cl_fin.append(-cl[0])
            cnf_neg.append(cl_fin)

            print('p cnf', nofv, len(cnf_neg), file=fp)
            for cl in cnf_neg:
                print(' '.join([str(l) for l in cl]), '0', file=fp)
    except IOError as e:
        sys.stderr.write('\033[31;1mERROR:\033[m Unable to write file {0}.\n'.format(neg))
        sys.stderr.write('\033[33m' + str(e) + '\033[m\n')
        sys.exit(1)
    return pos, neg

def bica(file_name):
    """
        Converts a CNF formula to DNF using Bica.
    """

    fns = [file_name]

    temp_files = []
    setup_execution(temp_files)

    fns = list(create_negation(fns[0], temp_files))

    primer = Primer('b', fns[0], fns[1], 0, True)
    primes = primer.run()

    fns[0], fns[1] = fns[1], fns[0]

    miner = Forqes('forqes', fns[0], fns[1], primes, False, False, 0)
    mincnf, nofv = miner.run()
    lines = 'p dnf {} {}'.format(nofv, len(mincnf))
    for clid in mincnf:
        lines += '\n' + ' '.join([str(-int(l)) for l in primes[clid].split()])
    return lines

def at_exit(temp_files):
    for file_name in temp_files:
        if os.path.exists(file_name):
            os.remove(file_name)

def setup_execution(temp_files):
    def handler(signum, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    atexit.register(at_exit, temp_files)

class BicaSolver(object):
    def __init__(self, qbf: QBF):
        self.qbf = qbf

    def solve(self):
        self.qbf.clauses = [set(clause) for clause in self.qbf.clauses if all(lit in clause and -lit not in clause for lit in clause)]
        temp_files = []
        setup_execution(temp_files)
        while self.qbf.quantifiers and self.qbf.clauses:
            block = self.qbf.quantifiers.pop()
            quantifier = block[0]
            variables = block[1]
            if quantifier == 'a':
                if not self.qbf.is_cnf:
                    dimacs_file_name = "{}_to_dimacs.cnf".format(self.qbf.file_name)
                    temp_files.append(dimacs_file_name)
                    self.qbf.write_file(dimacs_file_name, negate = True)
                    dnf = bica(dimacs_file_name)
                    self.qbf.clauses = []
                    dnf = dnf.split('\n')
                    for line in dnf:
                        self.qbf.read_line(line, negate = True)
                    self.qbf.is_cnf = True
                    os.remove(dimacs_file_name)
                    temp_files.remove(dimacs_file_name)
                new_clauses = []
                for index in range(len(self.qbf.clauses)):
                    new_clause = set([lit for lit in self.qbf.clauses[index] if abs(lit) not in variables])
                    if not new_clause:
                        return False
                    new_clauses.append(new_clause)
                self.qbf.clauses = new_clauses
                continue
            if quantifier == 'e':
                if self.qbf.is_cnf:
                    dimacs_file_name = "{}_to_dimacs.cnf".format(self.qbf.file_name)
                    temp_files.append(dimacs_file_name)
                    self.qbf.write_file(dimacs_file_name)
                    dnf = bica(dimacs_file_name)
                    self.qbf.clauses = []
                    dnf = dnf.split('\n')
                    for line in dnf:
                        self.qbf.read_line(line)
                    os.remove(dimacs_file_name)
                    temp_files.remove(dimacs_file_name)
                new_clauses = []
                for index in range(len(self.qbf.clauses)):
                    new_clause = set([lit for lit in self.qbf.clauses[index] if abs(lit) not in variables])
                    if not new_clause:
                        return True
                    new_clauses.append(new_clause)
                self.qbf.clauses = new_clauses
                continue
        if not self.qbf.clauses and not self.qbf.is_cnf:
            return False
        return True