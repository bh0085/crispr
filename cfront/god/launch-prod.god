God.watch do |w|
	  w.name = "cfront-prod-job1"
	  w.group = "cfront-prod"
	  w.start = "/home/ben/crispr/cfront/venv/bin/python -u /home/ben/crispr/cfront/cfront/utils/threaded_job_handler.py  /home/ben/crispr/cfront/production.ini"
	  w.log = "/home/ben/crispr/cfront/log/prod-job1.log"
	  w.keepalive(:interval => 15.seconds)
	  w.env = { 'VIRTUAL_ENV' => "/home/ben/crispr/cfront/venv/",
            	    'PATH' => "/home/ben/crispr/cfront/venv/bin:/home/ben/bin/:$PATH" }
end