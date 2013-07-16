<script type="unknown" id="job-v-template">
</script>
<script type="unknown" id="job-s-v-template">
  <div class="uncategorized section">
    <p class="header">guides not yet aligned to the genome</p>
    <ul class="views">
    </ul>
  </div>
  <div class="good section">
    <p class="header">guides having very few off-target hits in the genome</p>
    <ul class="views">
    </ul>
  </div>
  <div class="bad section">
    <p class="header">guides with substantial off-target cutting in the genome</p>
    <ul class="views">
    </ul>
  </div>
</script>

<script type="unknown" id="spacer-list-v-template">
  <span class="header">Spacer <span class="rank-container">{{id}}</span></span><br/>
  <span class="position-container">position: 
    <span class="strand">{{strand == 1? "+" : "-"}}</span>
    <span class="position">{{position}}</span><br/>
  </span>
  <span class="guide" style="font-family:courier">{{guide}}</span> <span style="font-family:courier; color:blue" class="nrg">{{nrg}}</span></br/>
  <span class="score-container">score: <span class="score">{{score}}</span></span>
</script>

<script type="unknown" id="job-v-svg-container-template">
    <div class="selection-svg">
    </div>
</script>

<script id="readout-section-template" type="unknown">
  <div class="status">
    <p>locating spacers... should take a couple of seconds</p>
  </div>
  <div class="job-container"></div>
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
	  <input name="email" id="email-address" type="email" required="true" placeholder="email" value="bh0085@gmail.com">
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
