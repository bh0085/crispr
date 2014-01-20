<script type="unknown" id="job-page-view-template">


  <div class="status-view-container"></div>
  
  <ul class="nav nav-tabs crispr-tabs"><h4 class="tabs-label">Results</h4>

    <li class="active"><a href="#results-tab" data-toggle="tab">Results</a></li>
    <li><a href="#info-tab" data-toggle="tab">Job Info</a></li>
  </ul>
  <div class="tab-content content-area">
    <div id="results-tab" name="Results" class="tab-pane active"> 
      <div class="pages-view-container"></div>
    </div>
    <div id="info-tab" name="Job Info" class="tab-pane">
      <div class="info-view">
	<dl>
	  <dt>Submitted by:</dt><dd>{{email}}</dd><br/>
	  <dt>Date submitted:</dt><dd>{{date_submitted}}</dd><br/>
	  <dt>Aligns to:</dt><dd>{{genome_name}} on the <b>{{strand=="1"?"sense":"antisense"}}</b> strand of <b>{{chr}}</b> at <b>{{start}}</b> ({{locus}})</dd><br/>
	  <dt>Sequence:</dt><dd class="seq"><span class="break-all dna">{{sequence}}</span></dd><br/>
	  <dt>Statistics:</dt><dd>{{sequence.length}}nt, contains {{spacers.length}} possible guide sequences</dd><br/>
	</dl>
      </div>
    </div>
  </div>
</script>
<script type="unknown" id="job-page-status-view-template">
  <h3>CRISPR Job Submission "{{name}}"</h3>
  <div class="">
    <h4>Status</h4>
    <div class="status-text full-width">about ?? minutes left<span class="right"><control class="email"><input id="email-complete" class="inline v-middle" {{email_complete?"checked":""}} type="checkbox"></input><label class="unselectable inline v-middle med-left-margin" for="email-complete">Email when done</label></control></span></div>
  </div>


  
  <!-- status display area -->
  <div class="status">
    <div class="progress progress-striped active">
      <div class="progress-bar bar" style="width: 0%;"></div>
    </div>
  </div> 
  <div class="wait-for-nickase">Note: Nickase Analysis and Downloads will be ready when all guides are completely analyzed. <a href={{readout_page_url}}>Guides and offtargets</a> info may be loaded dynamically!</div>

</script>
<script type="unknown" id="job-page-pages-view-template">
  

      <div class="">
	<div class="full-width">View results online<span class="right"><!--... or view <span class="download-container"><a href="{{downloads_page_url}}">downloadable results</a>.</span>--></div>
      </div>
      <div class="cards">
	<div class="card guides">
	  <div class="background"></div>
	  <a class="covering-link" href="{{readout_page_url}}"></a>
	  <div class="header"><h4>Guides & offtargets</h4></div>
	  <div class="footer"><span class="download-container"><a href="{{export_gb_guides_url}}" target="_blank">Download as genbank</a></span></div>
	</div>
	<div class="card nickase">
	  <div class="background"></div>
	  <a class="covering-link" href="{{nickase_page_url}}"></a>
	  <div class="header"><h4>Nickase analysis</h4></div>
	  <div class="footer"><span class="download-container"><a class="download" href="{{export_gb_nicks_url}}" target="_blank">Download as genbank</a></span></div>
	</div>
      </div>
  </div>
</script>
