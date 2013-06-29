<%inherit file="base.mako"/>
<%block name="content_html">
<span class="row content-row">
  <span class="float-left" id="navparent">
    <ul class="nav nav-list affix-top bs-docs-sidenav">
      <li class="submit-container"><a href="#submit">Submit<i class=" active icon-chevron-right"></i></a></li>
      <li class="identify-container inactive"><a href="#identify">Identify<i class="icon-chevron-right"></i></a></li>
      <li class="find-container inactive"><a href="#find">Find<i class="icon-chevron-right"></i></a></li>
    </ul>
  </span>
  <span id="scrolling-content" class="span8 offset2 scrolly-column">
    <%include file="submit.mako"/>
    <%include file="identify.mako"/>
    <%include file="find.mako"/>
    </div>
  </span>
</span>
<script id="scrolly-section-template" type="unknown">
  <div class="header page-header">
    <h4 class="header-back"><a class="previous">...back</a></h4>
    <h1 class="header-oneword">{{name}}</h1>
    <span class="header-description">{{description}}</span>
  </div>
  <div class="scrolly-content"></div>
</script>
</%block>

