<%inherit file="base.mako"/>
<%block name="content_html">
<span class="row content-row">
  <span id="scrolling-content" class="span8 offset1 scrolly-column">
   
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

