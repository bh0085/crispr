<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <a class="navbar-brand" href="/" href="/">CRISPR Design</a>
    </div>
    
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
	<li><a href="/about">Help</a></li>        
        <li><a href="https://groups.google.com/forum/#!forum/crispr">Forum</a></li> 
      </ul>
    </div>
  </div>
</div>



    %if request.matched_route.name == "submit":
<div class="alert alert-info alpha-warning header">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  <div class="content showing-less">
    <span class="text-fixed-width-content">

<strong>2018/05/16 BACK ONLINE</strong> Greetings CRISPR ENGINEERS! We're happy to let you know that the server at crispr.mit.edu is back up and fully operational. Active development of new features will soon be underway. If you have any questions or feature requests for how we can make the tool work better for you, please drop us an email. benh@broadinstitute.org Enjoy! --BEN
</span>


    <a class=" less show-more">show more</a>
    <span class="more"> </span>
    <a class="med-left-margin more show-less">... show less</a> 
  </div>
</div>
%endif

<!--
%if request.matched_route.name == "batch":
<div class="alert alert-info alpha-warning header">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  <div class="content showing-less">
    <span class="text-fixed-width-content">"Batch-submit" and this page are in experimental development. We are currently working to improve the experience of this page and make it easier for you to quickly recover, view, and check the status of submitted jobs! For updates and announcement, please check visit our <a href="https://groups.google.com/forum/#!forum/crispr">discussion forum.</a>.</span>
    <a class=" less show-more">show more</a>
    <span class="more"> </span>
    <a class="med-left-margin more show-less">... show less</a> 
  </div>
</div>
%endif

%if request.matched_route.name == "readout":
<div class="alert alert-warning alpha-warning header">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  <div class="content showing-less">
    <span class="text-fixed-width-content">Heads up -- the CRISPR server is currently under heavy load as we churn through jobs which were submitted before system upgrades taking place over the past week. Single jobs may at the moment take an hour or more to complete, batch jobs are are at the back of the queue and could take longer. If any fail to finish by 9/11/2013, please let us know!</span>
    <a class=" less show-more">show more</a>
    <span class="more"> </span>
    <a class="med-left-margin more show-less">... show less</a> 
  </div>
</div>
%endif
-->
