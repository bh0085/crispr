<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="/css/bootstrap/bootstrap.min.css" rel="stylesheet">
    <link href="/css/style.css" rel="stylesheet"/>
    <link href="/js/deps/jquery-tablesorter/themes/blue/style.css" rel="stylesheet"/>

    <meta HTTP-EQUIV="CONTENT-LANGUAGE" CONTENT="en-US">
    <meta charset="utf-8">   
    <meta name="description" content="CRISPR design portal">
    <title>CRISPR design app</title>
  
    <script type="text/javascript" src="/js/cdn/jquery.min.js" ></script>
    <script type="text/javascript" src="/js/cdn/underscore-min.js" ></script>
    <script type="text/javascript" src="/js/cdn/backbone-min.js" ></script>
    <script type="text/javascript" src="/js/cdn/mustache.min.js" ></script>
    <script type="text/javascript" src="/js/deps/backbone.eventbinder.js" ></script>
    <script type="text/javascript" src="/js/deps/backbone-relational/backbone-relational.js" ></script>
    <script type="text/javascript" src="/js/deps/jquery-tablesorter/jquery.tablesorter.min.js" ></script>

    <script src="/js/deps/bootstrap/bootstrap.min.js"></script>
    <script type="text/javascript" src="/js/deps/jquery-svg/jquery.svg.min.js"></script>

    <%include file="models.html"/>
    <%include file="backbone.mako"/>
    <%include file="bb_templates/spacers.mako"/>
    <script type="text/javascript" src="/js/pages/base.js"></script>

    %if request.matched_route.name == "submit":
    <script type="text/javascript" src="/js/pages/submit.js"></script>
    %elif request.matched_route.name == "readout":
    <script type="text/javascript" src="/js/pages/readout.js"></script>
    %endif

    <script type="text/javascript" src="/js/models/job_m.js"></script>
    <script type="text/javascript" src="/js/models/spacer_m.js"></script>
    <script type="text/javascript" src="/js/models/hit_m.js"></script>
    <script type="text/javascript" src="/js/views/job_v.js"></script>
    
  </head>
  <body class="${request.matched_route.name}" data-target="#navparent" data-spy="scroll" >
    <div class="header">
      <%include file="navbar.mako"/>
    </div>
    
    <%block name="content_html"/>
    <div class="footer">Zhang Lab, MIT 2013</div> 
  </body> 
</html>
