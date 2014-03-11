#!/usr/bin/python
import sys
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastxCommandline
from Bio.Blast import NCBIXML

contigs_file = str(sys.argv[1])
sample = str(sys.argv[2])

for seq_record in SeqIO.parse(contigs_file, 'fasta'):
    name = seq_record.id
    sequence = seq_record.seq
    out = name + '.xml'
    fasta = name + '.fasta'

    SeqIO.write(seq_record, fasta, 'fasta')

    with open('plasmid_results_%s.txt' % sample, 'a') as results:
            results.write('Checking %s:' % name + '\n' + '=======================' + '\n')

    for n in range(3):

        plasmid = '~/Sekventering/references/NC_00779%s.fna' % n
        comp = out + '-p%s' % n

        blastx_cline = NcbiblastxCommandline(cmd='blastn', out=comp,\
            outfmt=5, query=fasta,\
            subject=plasmid)

        stdout, stderr = blastx_cline()

        result_handle = open(comp)

        blast_record = NCBIXML.read(result_handle)


        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                if hsp.score > 1000:
                    with open('plasmid_results_%s.txt' % sample, 'a') as results:
                        results.write('Contig ' + name\
                         + ' aligns to:\n' + alignment.title + '\n')

    with open('plasmid_results_%s.txt' % sample, 'a') as results:
            results.write('Done checking %s:' % name + '\n' + '=======================' + '\n')