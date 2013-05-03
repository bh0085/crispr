<script id="submit-section-template" type="unknown">
  <div class="header">
    <h1 class="header-oneword">{{name}}</h1>
  </div>
  <% from cfront import cfront_settings %>

  <ul class="nav nav-tabs">
    <li class="active"><a href="#submit-one" data-toggle="tab">Single Sequence</a></li>
    <li ><a href="#submit-many" data-toggle="tab">Batch Mode</a></li>
  </ul>
  <div class="tab-content content-area">
    <div id="submit-one" name="submit-sequence" class="tab-pane scrolly-content active">
      <div class="header-description">{{description}}</div>
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
	    <label class="radio input-type-select">
	      <input  type="radio" name="inputRadios" id="optionsRadios2" value="other_region" checked>
	      other region (23-500 nt) <a class="annotation show-other-example">[..demo]</a>
	    </label>
	    <label  class="radio input-type-select">
	      <input type="radio" name="inputRadios" id="optionsRadios1" value="unique_genomic" >
	      unique genomic region (23-500 nt) <a class="annotation show-genome-example">[..demo]</a>
	    </label>
	  </div> 
	</div>
	<div class="control-group">
	  <span class="control-label">target genome</span>
	  <div  class="controls genome-controls">
	  </div> 
	</div>
	<div class="control-group">
	  <span class="control-label">sequence</span>
	  <div class="controls">
	    <textarea name="query" id="sequence_submission_area" required="true" placeholder="" pattern=".{23,}" rows=10></textarea>
	  </div>
	</div>
	<div class="control-group submit-group">
	  <div class="controls"><input type="submit"></input>
	  </div>
	</div>
      </form>
    </div>
    <div id="submit-many" name="submit-fasta" class="tab-pane scrolly-content">
      <div class="header-description">Submit multiple sequences in Fasta format for CRISPR design and analysis.</div>
      <form class="form-horizontal" name="submit-fasta" >

	<div class="control-group">
	  <span class="control-label">FASTA file *</span>
	  <div  class="controls">
	    <label>
	      <input type="file" name="fasta_file" id="file-input-2" required=true title="fasta file" value="choose a file"/>
	    </label>
	  </div> 
	</div>
	<div class="control-group">
	  <span class="control-label">email address *</span>
	  <div class="controls">
	    <input name="email" id="email-address-2" type="email" required="true" placeholder="email" value=${"crispr.design@gmail.com" if cfront_settings.get("debug_mode", False) else ""}>
	  </div>
	</div>
	<div class="control-group">
	  <span class="control-label">target genome</span>

	  <div  class="controls genome-controls">
	    <!-- this is filled in the rendering script with genome-contro -->
	  </div> 
	</div>
	<div class="control-group submit-group">
	  <div class="controls"><input type="submit"></input>
	  </div>
	</div>
      </form>
    </div>
  </div>
</script>

<script type="unknown" id="genome-control-template">
    <input type="radio" name="genome" value="{{name}}" {{checked_string}}>{{descriptive_name}} ({{name}})
</script>

