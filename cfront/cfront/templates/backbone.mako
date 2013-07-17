<script type="unknown" id="job-v-template">

</script>

<script type="unknown" id="job-h-template">
  <div class="row">
    <div class="span8 offset1">
      <h1>CRISPR guide candidates</h1>
      <h4>for job {{name}} ({{email}})</h4>
    </div>
  </div>
</script>

<script type="unknown" id="job-v-svg-container-template">
    <div class="selection-svg">
    </div>
</script>

<script id="readout-section-template" type="unknown">
  <div class="row page-header">
    <div class="span8 offset1 job-svg-view"></div>
  </div>
  <div class="row status page-header">
    <div class="span6 offset2">
      <div class="text">
	<p>locating spacers... should take a couple of seconds</p>
      </div>
      <div class="progress progress-striped active">
	<div class="bar" style="width: 0%;"></div>
      </div>
    </div>
  </div>
  <div class="spacers-area row">
    <div class="span3 col left spacers-container">
    </div>
    <div class="span4 col right hits-container">
    </div>
  </div>
</script>

<script id="submit-section-template" type="unknown">
  <div class="header page-header">
    <h1 class="header-oneword">{{name}}</h1>
    <span class="header-description">{{description}}</span>
  </div>
  <div class="scrolly-content">

    <form class="form-horizontal" >
      <div class="control-group">
	<span class="control-label">search name *</span>
	<div class="controls">
	  <input name="name" id="search-name" type="text" required="true" placeholder="name" value="ben_jobX">
	</div>
      </div>
      <div class="control-group">
	<span class="control-label">email address *</span>
	<div class="controls">
	  <input name="email" id="email-address" type="email" required="true" placeholder="email" value="crispr.scan@gmail.com">
	</div>
      </div>
      <div class="control-group">
	<span class="control-label">sequence type</span>
	<div  class="controls">
	  <label  class="radio">
	    <input type="radio" name="optionsRadios" id="optionsRadios1" value="option1" checked>
	    unique human genomic region (23-1000 nt)
	  </label>
	  <label class="disabled radio">
	    <input disabled type="radio" name="optionsRadios" id="optionsRadios2" value="option2">
	    other region (23-1000 nt)
	  </label>
	  <label class="disabled radio">
	    <input disabled type="radio" name="optionsRadios" id="optionsRadios3" value="option3">
	    single spacer sequence (23 nt)
	  </label>
	</div> 
      </div>
      <div class="control-group">
	<span class="control-label">sequence</span>
	<div class="controls">
	  <textarea name="sequence" id="sequence_submission_area" required="true" pattern=".{23,}" rows=10>GGAGCTGCAGGGACCTCCATGTCCTGGGACTGTTTGTGCAGGGCTCCGAGGGGACCCATGTGGCTCAGGGTGGCTAAGGGGGCAATGCTGCCCCCACCCGCTGGATGACCCAAGTGCTGTGTTTCAAATGCTGATAGCAGCCCTTTGTTTATTCTACACATTCCACTACCATGGGAGGCT</textarea>
	</div>
      </div>
      <div class="control-group">
	<div class="controls"><input type="submit"></input></div>
    </form>
    </div>
</script>
