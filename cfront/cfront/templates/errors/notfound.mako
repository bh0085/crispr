<html>
  <head>
    <title>Job not found</title>
  </head>
  <body>
    <link href="/css/bootstrap/bootstrap.min.css" rel="stylesheet"/>
    <link href="/css/style.css" rel="stylesheet"/>
    <div class="row med-margin-top">
      <div class="span6 offset2">
	<h1>Job not found!</h1>
	<h4>It looks like you're looking for a job with the key: ${request.matchdict["job_key"]}</h4>
	<p>But we dont' have a record of any such job in our system...</p>
	<p>If you think that you're receiving this message in error, please <a href="mailto:crispr.scan@gmail.com">Contact Us</a>!</p>
      </div>
    </div>
  </body>
</html>
