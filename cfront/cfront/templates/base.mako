<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="/css/bootstrap/bootstrap.min.css" rel="stylesheet">
    <link href="/css/style.css" rel="stylesheet"/>

    <meta HTTP-EQUIV="CONTENT-LANGUAGE" CONTENT="en-US">
    <meta charset="utf-8">   
    <meta name="description" content="CRISPR design portal">
    <title>Optimized CRISPR Design</title>
    
    <link href='http://fonts.googleapis.com/css?family=Alegreya+SC' rel='stylesheet' type='text/css'>

    <% import json %>
    <script type="text/javascript">
      console.log("INITING")
      %if init_state is not UNDEFINED:
      init_state=${json.dumps(init_state) | n}
      %endif
      %if sessionInfo is not UNDEFINED:
      sessionInfo = ${json.dumps(sessionInfo) | n}
      %endif
    </script>

    <script type="text/javascript" src="/js/cdn/jquery.min.js" ></script>
    <script type="text/javascript" src="/js/cdn/underscore-min.js" ></script>
    <script type="text/javascript" src="/js/cdn/backbone-min.js" ></script>
    <script type="text/javascript" src="/js/cdn/mustache.min.js" ></script>
    <script type="text/javascript" src="/js/deps/backbone.eventbinder.js" ></script>
    <script type="text/javascript" src="/js/deps/backbone-relational/backbone-relational.js" ></script>
    <script type="text/javascript" src="/js/deps/jquery-tablesorter/jquery.tablesorter.min.js" ></script>

    <script src="/js/deps/bootstrap/bootstrap.min.js"></script>
    <script type="text/javascript" src="/js/deps/jquery-svg/jquery.svg.min.js"></script>
    <script type="text/javascript" src="/js/deps/sprintf.js/src/sprintf.min.js"></script>

    <%include file="models.html"/>
    <%include file="backbone.mako"/>
    <%include file="bb_templates/spacers.mako"/>
    <%include file="bb_templates/job.mako"/>
    <%include file="bb_templates/guides.mako"/>
    <%include file="bb_templates/batch.mako"/>
    <%include file="bb_templates/readout.mako"/>
    <%include file="bb_templates/downloads.mako"/>
    <%include file="bb_templates/submit.mako"/>
    <%include file="bb_templates/file.mako"/>
    <%include file="bb_templates/about.mako"/>
    <%include file="bb_templates/nickase.mako"/>
    <script type="text/javascript" src="/js/pages/base.js"></script>
    <script type="text/javascript" src="/js/pages/${request.matched_route.name}.js"></script>
    <script type="text/javascript" src="/js/app/constants.js"></script>
    <script type="text/javascript" src="/js/app/delegates.js"></script>
    <script type="text/javascript" src="/js/app/url.js"></script>
    <script type="text/javascript" src="/js/app/init.js"></script>
    <script type="text/javascript" src="/js/models/job_m.js"></script>
    <script type="text/javascript" src="/js/models/spacer_m.js"></script>
    <script type="text/javascript" src="/js/models/nickase_m.js"></script>
    <script type="text/javascript" src="/js/models/hit_m.js"></script>
    <script type="text/javascript" src="/js/models/file_m.js"></script>
    <script type="text/javascript" src="/js/views/job_v.js"></script>
    <script type="text/javascript" src="/js/views/svg_v.js"></script>
    <script type="text/javascript" src="/js/views/nickase_v.js"></script>
    <script type="text/javascript" src="/js/views/n_details_view.js"></script>
    <script type="text/javascript" src="/js/views/readout_v.js"></script>
    <script type="text/javascript" src="/js/views/spacer_v.js"></script>
    <script type="text/javascript" src="/js/views/hit_v.js"></script>
    <script type="text/javascript" src="/js/views/file_v.js"></script>
    
  </head>
  <body class="${request.matched_route.name}" data-target="#navparent" data-spy="scroll" >
    <div class="header">
      <%include file="navbar.mako"/>
    </div>
    
    <div id=${request.matched_route.name}-container>
    </div>

    <div class="footer">Zhang Lab, MIT 2013</div> 
  </body> 
</html>
