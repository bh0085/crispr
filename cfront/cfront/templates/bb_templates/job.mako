<script type="unknown" id="job-v-template">
  <div class="header">
    <h1>CRISPR guide candidates</h1>
    <h4>for job "{{name}}" ({{email}})</h4>
    <div>Aligns to HUMAN genome (hg19) on the <b>{{strand=="1"?"sense":"antisense"}}</b> strand of <b>{{chr}}</b> at <b>{{start}}</b> ({{locus}})</div>
    <div>In {{sequence.length}}nt, contains {{spacers.length}} possible guide sequences</div>
    <div class="annotation" style="opacity:.25; text-align:center;">mouse over a guide for details</div>
  </div>
  <div class="row svg-container page-header">
    <div class="span8 offset1 selection-svg">
    </div>
  </div>

  <div class="row status page-header {{done ? 'done' : ''}}">
    <div class="span8 offset1">
      <div class="text">
	<p>locating guides... should take a couple of seconds</p>
      </div>
      <div class="progress progress-striped active">
	<div class="bar" style="width: 0%;"></div>
      </div>
    </div>
  </div>
</script>

<script type="unknown" id="job-v-svg-container-template">
</script>


<!-- A view containing all spacers in the left column -->
<script type="unknown" id="job-s-v-template">
  <div class="header">
    <div><h4>guides</h4></div>
    <div>scored by inverse likelihood of offtarget binding</div>
    <div class="annotation">mouse over for details</div>
  </div>
  <table>
    <thead>
      <tr> 
	<th></th>
	<th class="center">quality score</th>
	<th class="center">sequence</th>
      </tr>
    </thead>
    <tbody class="views"></tbody>
  </table>
  <div class="guide-quality">
    <div class="high-quality color-text"> high quality guide</div>
    <div class="medium-quality color-text"> mid quality guide</div>
    <div class="low-quality color-text"> low quality guide</div>
  </div>
</script>
