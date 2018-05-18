God.watch do |w|
	  w.name = "gfserve-hg38"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8001 hg38.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-hg38.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "gfserve-mm10"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8002 mm10.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-mm10.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-ce10"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8004 ce10.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-ce10.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "gfserve-danRer11"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8005 danRer11.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-danRer11.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-dm6"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8006 dm6.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-dm6.log"
	  w.keepalive(:interval => 15.seconds)
end



God.watch do |w|
	  w.name = "gfserve-oryCun2"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8007 oryCun2.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-oryCun2.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-sucScr11"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8008 sucScr11.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-sucScr11.log"
	  w.keepalive(:interval => 15.seconds)
end


God.watch do |w|
	  w.name = "gfserve-monDom5"
	  w.group = "gfserve"
	  w.dir = "/fastdata/genomes"	
	  w.start = "gfServer start localhost 8009 monDom5.2bit -tileSize=8"
	  w.log = "/home/ben_coolship_io/crispr/cfront/log/gfserve-monDom5.log"
	  w.keepalive(:interval => 15.seconds)
end
