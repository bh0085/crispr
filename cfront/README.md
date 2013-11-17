cfront README
==================

Getting Started
---------------

SETUP
{cd <directory containing this file>}

>> source venv/bin/activate
>> python setup.py develop
>> initialize_cfront_db development.ini
>> initialize_genomes development.ini

RUNNING THE WEBSERVER IN DEVELOPMENT MODE

>> source venv/bin/activate
[screen] 
>> pserve --reload development.ini
[screen] 
>> cfront/utils/job_handler.py development.ini
[screen] 
>> cfront/utils/genome_io.py development.ini

RUNNING THE WEBSERVER IN PRODUCTION MODE

{configure wsgi to run venv/pyramid.wsgi}
{ensure that god is running}
>> god load god/launch-prod.god



# Data directories
Most data is stored on the RAMDISK of the CRISPR server
RD_DATAROOT = "/tmp/ramdisk/crispr"

# Installation notes for
## Webserver
1. clone the repo
2. cd cfront
3. virtualenv venv
4. source venv/bin/activate
5. python setup.py develop
6. pip install numpy scipy biopython twobitreader

## Exon databases

## Genomes
For every genome, the following is required:
1. a bitpacked spacer library created by
utils/byte_scanner.py -p init -g {GENOME}

where {GENOME} should be on disk as a directory at:
RD_DATAROOT/{GENOME}/alllocs.txt

2. a postgres table listing all exons in the genome created by
utils/exons.py -p init


These actions will be performed on the default set of genomes by the genomes
install script, "install_genomes.py development.ini"
