#!/usr/bin/env python

from Bio import SeqIO, Seq
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--program", "-p",  dest="program",
                        required=True, type=str,
                        help="""program to run -- default, format_fa, 
allowed values are: 
[write_fa]""")
    parser.add_argument("--sequence", "-s", dest = "sequence",
                        default = None, type =str,
                        help="""sequence input, assumes stdin if none provided""")
    parser.add_argument("--id", "-i",dest="id",
                        default=None, type=str,
                        help="sequence id(s) if applicable")

    parser.add_argument("--description", "-d",dest="description",
                        default=None, type=str,
                        help="sequence id(s) if applicable")
    args = parser.parse_args()

    if args.program == "format_fa":
        s = SeqIO.SeqRecord(Seq.Seq(args.sequence if args.sequence else sys.stdin.read().strip()),
                            id=args.id if args.id  else "sequence1",
                            description=args.description if args.description else "")
        print s
        print s.format("fasta")
        #sys.stdout.write(s.format("fasta"))
    else :
        parser.print_help()
        exit()
    
if __name__ == "__main__":
    main()

    
