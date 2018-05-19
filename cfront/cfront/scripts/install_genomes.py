import os, sys
from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from cfront import genomes_settings


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)



def main(argv=sys.argv):
    #if len(argv) != 2:
    #    usage(argv)


    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--genome', '-g', dest = "genome", type = str,
                        help = "genome name [...]", required = True)
    parser.add_argument('inifile')
    args = parser.parse_args()

    settings = get_appsettings(args.inifile)

    
    prefix = "genomes."
    for k,v in settings.iteritems():
        #find all relevant settings, cast them and set "genomes_settings"
        if prefix == k[:len(prefix)]:
            setting_name =k[len(prefix):]
         
            if v.lower() in ['true', 'false']: val =  (v.lower()=='true')
            else: val = v
            genomes_settings[setting_name] = val

    
    import csv
    with open("/fastdata/crispr/config/genomes.csv") as f:
        r = csv.reader(f)
        cols = r.next()
        for l in r:
            g = dict(zip(cols,l))
            if g['assembly']!= args.genome:
                print "skipping {0}".format(g['name'])
                continue
            else:
                print "running {0}".format( g['name'])
                
            print "configuring genome: {0}".format(g)
            print "NOTE please ensure that gfServer for {0} is running at {1}".format(g["name"],g["blat"])
        
            exons_file = "/fastdata/zlab-genomes/{0}.ucsc.tsv".format(g["assembly"])
            if not os.path.isfile(exons_file):
                print "ERROR no exons file exists at: {0}".format(exons_file)
            else:
                import cfront.utils.exons as exons
                exons.populate_exons(g["assembly"])
                exons.create_indexes(g["assembly"])
                
                import cfront.utils.byte_scanner as byte_scanner
                byte_scanner.create_locs_file(g["assembly"])
                byte_scanner.init_library_bytes(g["assembly"])
                byte_scanner.create_packed_locs_file(g["assembly"])



if __name__=="__main__":
    main()
