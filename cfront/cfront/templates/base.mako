<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="/css/bootstrap/bootstrap.min.css" rel="stylesheet">
    <link href="/css/style.css" rel="stylesheet"/>
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

    <script src="/js/deps/bootstrap/bootstrap.min.js"></script>
    <script type="text/javascript" src="/js/deps/jquery-svg/jquery.svg.min.js"></script>

    <%include file="models.html"/>
    <script type="text/javascript" src="/js/pages/base.js"></script>
    <script type="text/javascript" src="/js/pages/identify.js"></script>
    <script type="text/javascript" src="/js/pages/submit.js"></script>
    <script type="text/javascript" src="/js/pages/find.js"></script>
    <script type="text/javascript" src="/js/pages/find_bb.js"></script>
    
  </head>
  <body class="${request.matched_route.name}" data-target="#navparent" data-spy="scroll" >
    <div class="header">
      <%include file="navbar.mako"/>
    </div>
    
    <%block name="content_html"/>
    <div class="footer">Zhang Lab, MIT 2013</div> 
  </body> 
</html>
