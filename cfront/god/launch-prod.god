God.watch do |w|
	  w.name = "cfront-prod-job1"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=1 --jobstride=3  /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/prod-job1.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  God.watch do |w|
	  w.name = "cfront-prod-job2"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=2 --jobstride=3  /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/prod-job2.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  God.watch do |w|
	  w.name = "cfront-prod-job3"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=0 --jobstride=3  /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/prod-job3.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end

God.watch do |w|
	  w.name = "cfront-prod-file"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/genome_io.py /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-file.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/usr/bin:/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  