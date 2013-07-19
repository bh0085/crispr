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
