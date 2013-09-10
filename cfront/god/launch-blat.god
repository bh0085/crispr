God.watch do |w|
	  w.name = "gfserve-hg19"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8001 hg19.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-hg19.log"
	  w.keepalive(:interval => 15.seconds)
end

#God.watch do |w|
#	  w.name = "gfserve-mm9"
#	  w.group = "gfserve"
#	  w.dir = "/tmp/ramdisk/genomes"	
#	  w.start = "gfServer start localhost 8002 mm9.2bit -tileSize=8"
#	  w.log = "/home/ben/crispr/cfront/log/gfserve-mm9.log"
#	  w.keepalive(:interval => 15.seconds)
#end