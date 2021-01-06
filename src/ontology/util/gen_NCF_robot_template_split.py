#!/usr/bin/env python3
"""
Author : Kai
Date   : 2020-12-01
Purpose: Generate Robot template input from CDNO_nutritional_components_framework sheet as csv.

Run: ./gen_NCF_robot_template_split.py -i CDNO_nutritional_components_framework_v7.9_ROBOT_07122020.csv -o1 nutritional_components_framework.tsv -o2 sugar_derivatives.tsv
"""

import argparse
import sys
import csv
import re

#id_int = 1

range1_int = 1
range2_int = 100000

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # parser.add_argument(
    #     'positional', metavar='str', help='A positional argument')

    parser.add_argument(
        '-i',
        '--input',
        help='input csv',
        metavar='str',
        type=str,
        default='')

    parser.add_argument(
        '-o1',
        '--output1',
        help='nutritional components framework robot template',
        metavar='str',
        type=str,
        default='')

    parser.add_argument(
        '-o2',
        '--output2',
        help='sugar derivative robot template',
        metavar='str',
        type=str,
        default='')


    # parser.add_argument(
    #     '-f', '--flag', help='A boolean flag', action='store_true')

    return parser.parse_args()

# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)

# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)
# --------------------------------------------------

#for 'is a' relationships
def subclass_case(Parent,Parent_ID,Term,Id,Index):
    if Id == 'unspecified CHEBI term':
        ontology_ID = assign_CDNO_ID(Range='1')
    else:
        ontology_ID = Id
    label = Term

    if Parent_ID == '':
        parent_class = Parent
    #if parent_ID isn't chebi:
    elif str(Parent_ID)[0:6] == 'CHEBI:':
        parent_class = Parent_ID
    else:
        parent_class = Parent

    #parent_class = Parent
    #equivalence_axiom = ''
    definition = ''
    index = str(Index)
    outline= (ontology_ID,label,parent_class,definition,index)
    return(outline)
# --------------------------------------------------

# for 'derives from' relationships
def equivalence_case(Parent,Term,Id,Index):
    regex = r"\b\s"
    ontology_ID = assign_CDNO_ID(Range='2')
    label = '{} derived from {}'.format(Term,Parent)
    #parent_class = ''
    #if parent has more than one word
    if re.search(regex, Parent):
        # if term is multiple (and parent is multiple)
        if re.search(regex, Term):
            equivalence_axiom = "('{}' and 'derives from' some '{}')".format(Term,Parent)
        # if term is one and parent is multiple
        else:
            equivalence_axiom = "({} and 'derives from' some '{}')".format(Term,Parent)
    #if parent is only one word
    else:
        # if term is multiple and parent is one
        if re.search(regex, Term):
            equivalence_axiom = "('{}' and 'derives from' some {})".format(Term,Parent)
        # if term is one parent is one
        else:
            equivalence_axiom = "({} and 'derives from' some {})".format(Term,Parent)

    def_first = Term.capitalize()
    definition = '{} which is derived from {}.'.format(def_first,Parent)
    index = str(Index)
    outline= (ontology_ID,label,equivalence_axiom,definition,index)
    return(outline)
# --------------------------------------------------

def role_case(Parent,Term,Id,Index):
    ontology_ID = Id
    label = Term
    parent_class = ''
    equivalence_axiom = ''
    definition = ''
    index = str(Index)
    outline= (ontology_ID,label,parent_class,equivalence_axiom,definition,index)
    return(outline)
# --------------------------------------------------

# outputs a new unique CDNO curie
def assign_CDNO_ID(Range):
    #global id_int
    #global range1_int
    #global range2_int


    outstr = ''
    if id_int < 10:
        #print('CDNO:000000'+id_int)
        outstr = 'CDNO:000000{}'.format(id_int)
    elif id_int < 100:
        outstr = 'CDNO:00000{}'.format(id_int)
    elif id_int < 1000:
        outstr = 'CDNO:0000{}'.format(id_int)
    elif id_int < 10000:
        outstr = 'CDNO:000{}'.format(id_int)
    elif id_int < 100000:
        outstr = 'CDNO:00{}'.format(id_int)
    elif id_int < 1000000:
        outstr = 'CDNO:0{}'.format(id_int)
    elif id_int < 10000000:
        outstr = 'CDNO:{}'.format(id_int)
    id_int += 1
    return(outstr)
# --------------------------------------------------


#Global var
id_int = 1


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    input_arg = args.input
    #out_file = args.output
    out_file1 = args.output1
    out_file2 = args.output2

    input_list = []
    # open infile reading it in as list of OrderedDict
    with open(input_arg, mode ='r', encoding='utf-8-sig' ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_list.append(row)


    #open outfile1 and print
    o1_header_1 = ('Ontology ID', 'label', 'parent class', 'definition', 'index')
    o1_header_2 =('ID', 'AL rdfs:label@en', 'SC %', 'AL IAO:0000115@en', '')
    f1 = open(out_file1, 'a')
    print('\t'.join(o1_header_1), file=f1)
    print('\t'.join(o1_header_2), file=f1)

    #open outfile2 and print
    f2 = open(out_file2, 'a')
    o2_header_1 = ('Ontology ID', 'label', 'equivalence axiom', 'definition', 'index')
    o2_header_2 =('ID', 'AL rdfs:label@en', 'EC %', 'AL IAO:0000115@en', '')
    print('\t'.join(o2_header_1), file=f2)
    print('\t'.join(o2_header_2), file=f2)

    #print the input_list
    for num, dict in enumerate(input_list, start=2):
        parent = dict['parent']
        parent_id = dict['parent ID']
        term = dict['term']
        id = dict['term ID']
        reln = dict['relationship']
        if reln == 'is a':
            print('\t'.join(subclass_case(Parent=parent,Parent_ID=parent_id,Term=term,Id=id,Index=num)), file =f1)
        elif reln == 'derived from':
            #equivalence_case(Parent=parent,Term=term,Id=id)
            print('\t'.join(equivalence_case(Parent=parent,Term=term,Id=id,Index=num)), file =f2)
        elif reln == 'has role':
            print('\t'.join(role_case(Parent=parent,Term=term,Id=id,Index=num)), file =f1)
        else:
            print('no relationship in row {}'.format(num))


# --------------------------------------------------
if __name__ == '__main__':
    main()
