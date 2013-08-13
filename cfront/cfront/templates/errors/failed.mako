<html>
  <head>
    <title>Job failed</title>
  </head>
  <body>
    <link href="/css/bootstrap/bootstrap.min.css" rel="stylesheet"/>
    <link href="/css/style.css" rel="stylesheet"/>
    <div class="row med-margin-top">
      <div class="span6 offset2">
	<h1>Job failed!</h1>
	<h4>It looks like the job you're looking for (with key: ${request.matchdict["job_key"]}) has failed with error:</h4>
	<p>${message}</p>
	<p></p>
	<p>This is probably our bad ...</p>
	<p>While we run the server in alpha mode, we expect that errors will occasionally occur and will review the logs to figure out what went wrong. If you have selected to recieve email notifications for this job, then you'll be notified once we've fixed whatever issue caused your job to fail. </p>
	<p>Questions? <a href="mailto:crispr.scan@gmail.com">Contact Us</a>!</p>
      </div>
    </div>
  </body>
</html>
