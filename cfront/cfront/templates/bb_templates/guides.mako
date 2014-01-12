<script type="unknown" id="job-v-template">
  <div class="header">
    <!--header-->
    <div class="job-title showing-less"><h3 style="display:inline-block;">"{{name}}"</h3>
    </div>

    <ul class="nav nav-tabs">
      <li class="active"><a href="#spacers-tab" data-toggle="tab">Spacers</a></li>
      <!--
      <li><a href="#downloads-tab" data-toggle="tab">Downloads</a></li>
      <li><a href="#double-nickase-tab" data-toggle="tab">Double Nickase</a></li>
      -->
    </ul>
    <div class="tab-content content-area">
      <div id="spacers-tab" name="spacers" class="tab-pane active">
	<!-- svg drawing area -->
	<div class="header"><span class="section-name">Interactive results: </span><span class="annotation med-left-margin">mouse over a guide or explore below for details</div>
	<div class="jobsvg-v-container">
	</div>
	<div class="col-tables-area">
	  <div class="spacer-v-container"></div>
	  <div class="col left">
	    <div class="spacers-container"></div>
	  </div><div class="col right spacer-h-v-container">
	  </div>
	</div>
      </div>
      <div id="downloads-tab" name="downloads" class="tab-pane"> 
	<!-- files download area -->
	<div id="downloadable" class="files-area"></div>
      </div>
      <div id="double-nickase-tab" name="double nickase" class="tab-pane">
	<div class="nickase-v-container"></div>
      </div>
    </div>
  </div>
</script>

<script type="unknown" id="job-v-svg-container-template">
</script>


<!-- A view containing all spacers in the left column -->
<script type="unknown" id="job-spacer-list-v-template">
  <div class="header showing-less">
    <div><h4>all guides</h4></div>
    <div>scored by inverse likelihood of offtarget binding</div>
    <span class="annotation">mouse over for details</span> 
    <a class="med-left-margin less show-more annotation">... show legend</a>
    <a class="med-left-margin more show-less annotation">... hide legend</a>

    <div class="guide-quality more">
      <div class="high-quality color-text"> high quality guide</div>
      <div class="medium-quality color-text"> mid quality guide</div>
      <div class="low-quality color-text"> low quality guide</div>
    </div>
  </div>
  <table class="med-top-margin">
    <thead>
      <tr> 
	<th></th>
	<th class="center">score</th>
	<th class="center">sequence</th>
      </tr>
    </thead>
    <tbody class="views"></tbody>
  </table>
</script>
