import os, sys
from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

genomes_settings = {}


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    prefix = "genomes."

    for k,v in settings.iteritems():
        #find all relevant settings, cast them and set "genomes_settings"
        if prefix == k[:len(prefix)]:
            setting_name =k[len(prefix):]
         
            if v.lower() in ['true', 'false']: val =  (v.lower()=='true')
            else: val = v
            genomes_settings[setting_name] = val


    genomes = [ g.strip() for g in genomes_settings.get("genome_names").split(",")]
    for i,g in enumerate(genomes):
        #set up a gfServer
        print "configuring genome: {0}".format(g)
    
        gfport_address = genomes_settings.get("{0}_gfport".format(g))
        print "NOTE please ensure that gfServer for {0} is running at {1}".format(g,gfport_address)
        
        exons_file = genomes_settings["ucsc_tsv_template"].format(g)
        if not os.path.isfile(exons_file):
            print "ERROR no exons file exists at: {0}".format(exons_file)
        else: print "found exons file for {0}".format(g)
        
        #import cfront.utils.exons as exons
        #import cfront.utils.byte_scanner as byte_scanner

        print "please run exons -g {0}".format(g)     


if __name__=="__main__":
    main()
