<script id="submit-v2-section-template" type="unknown">
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
	  <span class="control-label">gene name</span>
	  <div class="controls">
	    <div id="prefetch">
	      <input class="typeahead" type="text" placeholder="gene name">
	    </div>
	  </div>
	</div>
      </form>


      <div class="row gene-info-container">
	<div class="col-xs-12 col-sm-8 col-sm-offset-2">
	  <div class="gene-info">
	    
	  </div>
	</div>
      </div>

      
      <form class="form-horizontal" >
	<div class="control-group" readonly>
	  <span class="control-label">gene ID</span>
	  <div class="controls">
	    <input name="gene_id" id="gene_id_value" type="text" placeholder="please select a gene" readonly />
	  </div>
	</div>
	<div class="control-group">
	  <span class="control-label">email address *</span>
	  <div class="controls">
	    <input name="email" id="email-address" type="email" required="true" placeholder="email">
	  </div>
	</div>

	
	<div class="control-group submit-group">
	  <div class="controls"><input  type="submit"></input>
	  </div>
	</div>
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
