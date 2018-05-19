<script id="splash-v2-section-template" type="unknown">
  <div class="header">
    <h1 class="header-oneword">{{name}}</h1>
  </div>
  <% from cfront import cfront_settings %>

  <div class="tab-content content-area">


 	</div>
	<div class="control-group">
	  <span class="control-label">target genome</span>
	  <div  class="controls genome-controls">
	  </div> 
	</div>

  <dl>
  <dt>v2 crispr-gene (in beta, June 2018*</dt><dd>Knock down or knock out a gene with CAS-9 or CPCF1.</dd>
  </dt>
  <dt>v1 crispr-locus (released, July 2013)</dt><dd>Select optimal Crispr CAS-9 target sites in a genomic locus or synthetic sequence using off-target predictions based on <a href="http://www.nature.com/nbt/journal/v31/n9/full/nbt.2647.html">Hsu et al, Nature Biotechnology 2013</a>.</dd>
  </dt>
  </div>
</script>

<script type="unknown" id="genome-control-template">
    <input type="radio" name="genome" value="{{name}}" {{checked_string}}>{{descriptive_name}} ({{name}})
</script>


