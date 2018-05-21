<script id="submit-v2-section-template" type="unknown">
  <div class="header">
    <h1 class="header-oneword">{{name}}</h1>
  </div>
  <% from cfront import cfront_settings %>

  <ul class="nav nav-tabs">
    <li class="active"><a href="#submit-one" data-toggle="tab">Single gene ({{genome_assembly}})</a></li>
    <li ><a href="#submit-many" data-toggle="tab" class="disabled" >Genomic region ({{genome_assembly}})</a></li>
  </ul>
  <div class="tab-content content-area">
    <div id="submit-one" name="submit-sequence" class="tab-pane scrolly-content active">
      <div class="header-description"><p>{{description}}</p><p style="color:black;">Selected genome: <b>{{genome_name}}</b> ({{genome_assembly}}). <a href="/">Choose another genome?</a></p></div>
      <form class="form-horizontal" >

	<div class="control-group">
	  <span class="control-label">gene name</span>
	  <div class="controls">
	    <div id="prefetch">
	      <input class="typeahead" type="text" placeholder="gene name">
	    </div>
	  </div>
	</div>
      </form>


      <div class="gene-helpers hidden">
	<div class="gene-info-container">
	  <div  class="gene-info"></div>
	</div>
	<div class="gene-info-helpers"><ul><li><a class="toggle-gene-info">hide gene info</a></li><li><a class="download-fa" target="_blank">download as fasta</a></li><li><a class="download-gb" target="_blank">download as genbank</a></li></ul></div>
      </div>

      <form id="submit-form">
	<div class="form-group">
	  <label for="gene_id_value">crispr.mit.edu gene id</label>
	  <input disabled="true" type="text" class="form-control updates-target" id="gene_id_value" placeholder="crispr.mit.edu gene ID" required="true">
	  <small id="emailHelp" class="form-text text-muted">Please select a gene name, above.</small>
	</div>
	<div class="form-group">
	  <label for="email-address">Email address *</label>
	  <input type="email" class="form-control updates-target" id="email-address" placeholder="your email" required="true">
	</div>
	<button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</script>

<script type="unknown" id="genome-control-template">
  <input type="radio" name="genome" value="{{name}}" {{checked_string}}>{{descriptive_name}} ({{name}})
</script>


<script type="unknown" id="typeahead-gene-suggestion-template">
  <div class="suggestion"><span class="gene-name">{{name}}</span><span class="gene-id"></span></div>
</script>


<script type="unknown" id="gene-info-template">
  <dl>
   <dt>{{name}}, {{end - start}}nt</h4></dt><dd>{{chrom}}:{{strand}}{{start}}-{{end}}</dd>
  </dl>
								      
</script>
