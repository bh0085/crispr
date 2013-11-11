God.watch do |w|
	  w.name = "cfront-dev-job1"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=1 --jobstride=4  /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-job1.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  God.watch do |w|
	  w.name = "cfront-dev-job2"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=2 --jobstride=4  /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-job2.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  God.watch do |w|
	  w.name = "cfront-dev-job3"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=3 --jobstride=4  /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-job3.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  God.watch do |w|
	  w.name = "cfront-dev-job4"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py --jobofs=0 --jobstride=4  /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-job4.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  

God.watch do |w|
	  w.name = "cfront-dev-file"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/genome_io.py /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-file.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
	  
God.watch do |w|
	  w.name = "cfront-dev-serve"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/pserve --reload /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-serve.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end
