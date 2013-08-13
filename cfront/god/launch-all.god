God.watch do |w|
	  w.name = "cfront-prod-job"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/prod-job.log"
	  w.keepalive(:interval => 15.seconds)
end
	  
God.watch do |w|
	  w.name = "cfront-prod-file"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/genome_io.py /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/prod-file.log"
	  w.keepalive(:interval => 15.seconds)
end

God.watch do |w|
	  w.name = "cfront-dev-job"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/job_handler.py /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-job.log"
	  w.keepalive(:interval => 15.seconds)
end
	  
God.watch do |w|
	  w.name = "cfront-dev-file"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/genome_io.py /home/ben/crispr/cfront/development.ini"
	  w.log = "/home/ben/crispr/cfront/log/dev-file.log"
	  w.keepalive(:interval => 15.seconds)
end
	  
God.watch do |w|
	  w.name = "cfront-dev-serve"
	  w.group = "cfront-dev"
	  w.start = "/home/ben/crispr/cfront/venv/bin/pserve --reload /home/ben/crispr/cfront/development.ini >> /home/ben/crispr/cfront/log/dev-serve.log"
	  w.log = "/home/ben/crispr/cfront/log/dev-serve.log"
	  w.keepalive(:interval => 15.seconds)
end
