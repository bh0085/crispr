#!/usr/bin/env python
'''
"SEQUENCE_ID=";
$id;
"\n";
"SEQUENCE_TEMPLATE=";
$seq;
"\n";
"SEQUENCE_TARGET=190,45";
"\n";
"PRIMER_OPT_SIZE=22";
"\n";
"PRIMER_MIN_SIZE=18";    
"\n";
"PRIMER_MAX_SIZE=26";    
"\n";
"PRIMER_MIN_TM=58";
"\n";
"PRIMER_MAX_TM=62";  
"\n";
"PRIMER_PAIR_WT_PRODUCT_SIZE_GT=1.0";
"\n";
"PRIMER_PRODUCT_OPT_SIZE=105";
"\n";
"PRIMER_THERMODYNAMIC_PARAMETERS_PATH=/home/ben/src/primer3-2.3.5/src/primer3_config/";
"\n";
"PRIMER_PRODUCT_SIZE_RANGE=60-140\n";
"=\n";
'''

def run_commands():
    cmd1 = ("perl {0}/scripts/make_primer3_offtarget_input.pl {1} "+\
           "{0}/reference/human_g1k_v37.fasta {2}").format(CDHOME, f6p, f7p)
    cmd2="primer3_core -p3_settings_file={0}/primer3/primer3-2.3.5/primer3web_v4_0_0_default_settings.txt -output={1} {2}".format(CDHOME,f8p,f7p)
    
    cmd3 = "perl {0}/parse_primer3_output.pl {1} {2} {3}".format(CDSCRIPTS, f8p, f6p,f9p)


