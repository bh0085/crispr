<script id="submit-section-template" type="unknown">
  <div class="header page-header">
    <h1 class="header-oneword">{{name}}</h1>
    <span class="header-description">{{description}}</span>
  </div>
  <% from cfront import cfront_settings %>
  <div class="scrolly-content">
    <form class="form-horizontal" >
      <div class="control-group">
	<span class="control-label">search name *</span>
	<div class="controls">
	  <input name="name" id="search-name" type="text" required="true" placeholder="name" value=${"ben_jobX" if cfront_settings.get("debug_mode", False) else ""}>
	</div>
      </div>
      <div class="control-group">
	<span class="control-label">email address *</span>
	<div class="controls">
	  <input name="email" id="email-address" type="email" required="true" placeholder="email" value=${"crispr.design@gmail.com" if cfront_settings.get("debug_mode", False) else ""}>
	</div>
      </div>
      <div class="control-group">
	<span class="control-label">sequence type</span>
	<div  class="controls">
	  <label  class="radio input-type-select">
	    <input type="radio" name="inputRadios" id="optionsRadios1" value="unique_genomic" checked>
	    unique genomic region (23-500 nt) <a class="annotation show-genome-example">[..demo]</a>
	  </label>
	  <label class="radio input-type-select">
	    <input  type="radio" name="inputRadios" id="optionsRadios2" value="other_region">
	    other region (23-500 nt) <a class="annotation show-other-example">[..demo]</a>
	  </label>
	  <label class="radio input-type-select">
	    <input  type="radio" name="inputRadios" id="optionsRadios3" value="guides_list">
	    <span class="showing-less">list of guide sequences (N x 23 nt) <a class="show-more less"> [...info]</a><a class="show-less more"> [...hide]</a><div class="more annotation">please enter one guide per line followed by optional names</div><a class="more show-example">[show example]</a>
	  </label>
	</div> 
      </div>
      <div class="control-group">
	<span class="control-label">target genome</span>
	<div  class="controls">
	  <label  class="radio genome">
	    <input type="radio" name="genome" id="genomeRadios1" value="HUMAN" checked>
	    human genome (hg19)
	  </label>
	  <label class="radio genome">
	    <input  type="radio" name="genome" id="genomeRadios2" value="MOUSE">
	    mouse genome (mm9) <span class="annotation">(experimental)</span>
	  </label>
	</div> 
      </div>
      <div class="control-group">
	<span class="control-label">sequence</span>
	<div class="controls">
	  <textarea name="query" id="sequence_submission_area" required="true" placeholder="" pattern=".{23,}" rows=10></textarea>
	</div>
      </div>
      <div class="control-group submit-group">
	<div class="controls"><input type="submit"></input></div>
    </form>
    </div>
    

</script>
