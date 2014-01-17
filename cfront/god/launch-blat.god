God.watch do |w|
	  w.name = "gfserve-hg19"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8001 hg19.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-hg19.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "gfserve-mm9"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8002 mm9.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-mm9.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "gfserve-rn5"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8003 rn5.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-rn5.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "gfserve-ce10"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8004 ce10.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-ce10.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "gfserve-danRer7"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8005 danRer7.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-danRer7.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-dm3"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8006 dm3.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-dm3.log"
	  w.keepalive(:interval => 15.seconds)
end



God.watch do |w|
	  w.name = "gfserve-oruCun2"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8007 oryCun2.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-oryCun2.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-susScr3"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8008 susScr3.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-susScr3.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-monDom5"
	  w.group = "gfserve"
	  w.dir = "/tmp/ramdisk/genomes"	
	  w.start = "gfServer start localhost 8009 monDom5.2bit -tileSize=8"
	  w.log = "/home/ben/crispr/cfront/log/gfserve-monDom5.log"
	  w.keepalive(:interval => 15.seconds)
end