#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# University of Zurich
# Department of Computational Linguistics

# Authors: Cui Ding(olatname: cding)
# Matriculation Numbers: 21-718-945
# 			Mia Tatjana Egli (olatname: miaegl)
# Matriculation Numbers: 21-700-406

# Codes for checking which encoding is used for the two .txt files:

# with open('encoding_1.txt', 'rb') as infile1, open('encoding_2.txt', 'rb') as infile2:
#     b_string1 = infile1.read()
#     b_string2 = infile2.read()
#     b_string1.decode('ASCII')
#     b_string2.decode('ASCII')
#     print(b_string1)
#     print(b_string2)
#     b_string1.decode('ISO 8859-1')
#     b_string2.decode('ISO 8859-1')
#     print(b_string1)
#     print(b_string2)

# encoding_1.txt --> ASCII
# encoding_2.txt --> Iso 8859-1


with open('encoding_1.txt', 'rb') as infile1, open('encoding_2.txt', 'rb') as infile2,\
        open('encoding_utf-8.txt', 'w', encoding='utf-8') as outfile:
    for line in infile1:
        outfile.write(line.decode('ASCII'))
    outfile.write('\n')
    for line in infile2:
        outfile.write(line.decode('ISO 8859-1'))
