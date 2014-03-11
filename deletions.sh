#!/bin/bash
for sample in $*;
do
    cd ~/Sekventering/reads/master_trim/$sample/

    samtools mpileup stampy_rg_$sample.bam > pileup_$sample.txt

    python ~/NGS/my_scripts/find_deletions.py pileup_$sample.txt
done