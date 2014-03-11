#!/usr/bin/python

'''
This scipts is called with the samtools mpileup
coverage file as the first argument. It then finds the missing postitions
assumes that these represent regions with zero coverage, since no reads
aligned. It then outputs a file with a list of intervals with zero coverage.
'''

import sys

filename = sys.argv[1]

zero_coverage = []

with open(filename, 'r') as info:
    for line in info:
        contents = line.split()
        position = contents[1]

        zero_coverage.append(position)

deletions = []

for n in range(len(zero_coverage) - 1):
    if int(zero_coverage[n+1]) - int(zero_coverage[n]) > 1:
        deletions.append([zero_coverage[n], zero_coverage[n+1], int(zero_coverage[n+1]) - int(zero_coverage[n])])
    else:
        pass

with open('output.txt', 'a') as out_file:
    for lst in deletions:
        out_file.write('Start: %s ; Stop: %s ; Length: %s \n' % (lst[0], lst[1], lst[2]))