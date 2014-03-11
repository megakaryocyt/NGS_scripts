for sample in $*
do
    cd ~/Sekventering/reads/master_trim/$sample

    if [ -f both_unmapped.bam ];
    then
        echo ".bam file exists"
    else
        samtools view -bT ~/Sekventering/reads/NC_007793.fasta stampy_$sample.sam > stampy_$sample.bam

        samtools view -u -f 12 -F 256 stampy_$sample.bam > both_unmapped.bam

        rm stampy_$sample.bam
    fi

    if [ -f unmapped_1.fastq ];
    then
        echo ".fastq files already exist"
    else
        java -jar ~/NGS/picard-tools-1.104/SamToFastq.jar I=both_unmapped.bam FASTQ=unmapped_1.fastq SECOND_END_FASTQ=unmapped_2.fastq
    fi

    VelvetOptimiser.pl -s 33 -e 93 -x 10 -f "-shortPaired -fastq -separate unmapped_1.fastq unmapped_2.fastq" -o "-min_contig_lgth 1000" -p velvet_out_2n_round

    cd velvet_out*

    mv contigs.fa unmapped_contigs_$sample.fasta

    python ~/NGS/my_scripts/insertions.py unmapped_contigs_$sample.fasta $sample
done