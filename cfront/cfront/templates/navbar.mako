<div class="navbar unselectable">
  <div class=""><!--removed navbar inner styling -->
    <div class="container"> 
      <a class="brand" href="/">CRISPR Design</a>
      <!-- Everything you want hidden at 940px or less, place within here -->
      <ul class="nav pull-right">
        <li><a href="/about">About</a></li>        
        <li><a href="mailto:crispr.design@gmail.com">Contact</a></li>        
      </ul>
    </div>
  </div>
</div>
%if request.matched_route.name == "submit":
<div class="alert alert-success alpha-warning header">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  <div class="content showing-less">
    <span class="text-fixed-width-content">The CRISPR design tool is all fixed up and will soon enter beta-phase. During this period we're going to continue working to improve performance and reliability -- especially of handy features like email alerts and the like. We'll fix errors as we become aware of them, so as always, please don't hesitate to contact us at: <a href="mailto:crispr.scan@gmail.com">crispr.design@gmail.com</a> or post on the <a href="https://groups.google.com/forum/#!forum/crispr">discussion forum.</a></span>
    <a class=" less show-more">show more</a>
    <span class="more"> </span>
    <a class="med-left-margin more show-less">... show less</a> 
  </div>
</div>
%endif
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
