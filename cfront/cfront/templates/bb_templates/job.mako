<script type="unknown" id="job-v-template">
  <div class="header showing-less">
    <!--header-->
    <h2 style="display:inline-block;">"{{name}}"</h2>
    <a class="show-more less med-left-margin annotation">... show info</a>
    <a class="med-left-margin more annotation show-less">... hide info?</a>
    <div class="job-description med-left-margin med-top-margin more">
      <dl>
	<dt>Submitted by:</dt><dd>{{email}}</dd><br/>
	<dt>Date submitted:</dt><dd>{{submitted}}</dd><br/>
	<dt>Date completed:</dt><dd>{{completed}}</dd><br/>
	<dt>Aligns to:</dt><dd>{{genome_name}} on the <b>{{strand=="1"?"sense":"antisense"}}</b> strand of <b>{{chr}}</b> at <b>{{start}}</b> ({{locus}})</dd><br/>
	<dt>Sequence:</dt><dd class="seq"><span class="break-all dna">{{seq_html}}</dna></dd><br/>
	<dt>Statistics:</dt><dd>{{sequence.length}}nt, contains {{spacers.length}} possible guide sequences</dd><br/>
      </dl>
    </div>   
    <ul class="nav nav-tabs">
      <li><a href="#spacers-tab" data-toggle="tab">Spacers</a></li>
      <li ><a href="#downloads-tab" data-toggle="tab">Downloads</a></li>
      <li class="active"><a href="#double-nickase-tab" data-toggle="tab">Double Nickase</a></li>
    </ul>
    <div class="tab-content content-area">
      <div id="spacers-tab" name="spacers" class="tab-pane">
	<!-- svg drawing area -->
	<div class="header"><span class="section-name">Interactive results: </span><span class="annotation med-left-margin">mouse over a guide or explore below for details</div>
	<div class="svg-container">
	</div>
	<div class="spacers-area">
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
      <div id="double-nickase-tab" name="double nickase" class="tab-pane active">
	<div class="nickase-v-container"></div>
      </div>
    </div>
  </div>
</script>

<script type="unknown" id="job-v-svg-container-template">
</script>


<!-- A view containing all spacers in the left column -->
<script type="unknown" id="job-s-v-template">
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
