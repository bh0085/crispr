<script id="splash-v2-section-template" type="unknown">
  <% from cfront import cfront_settings %>

  <div class="splash-greeting-container">
    <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3"><div class="biline"><h3>WELCOME TO CRISPR.MIT.EDU</h3><p>Gene knockout and knockdown design platform<p>This website is undergoing active development.<br/><b>Returning users</b>: to access the previous version of this site or learn what's new, please see "<a href="#whatchanged">WHAT CHANGED</a>", below.</div></div>
    </div>
  </div>
  
  <div class="tab-content content-area">
    <div class="splash-greeting-container">
      <h1 class="headline">CHOOSE A GENOME</h1>
      <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3">
	  <div class="biline"><p>Please choose a target organism to target with CRISPR Cas9 or Cpf1.</div>
      </div></div>
    </div>

    <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3">
	<ul id="genome-v2-links"></ul>
    </div></div>

    <div class="splash-greeting-container">

      <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3"><div class="biline"><p>Working with an organism not yet included in this list? Please feel free to suggest it for inclusion on the stickied "ADDITIONAL GENOMES THREAD" on the crispr.mit.edu <a href="https://groups.google.com/forum/#!forum/crispr">forum</a></div></div></div>
    </div>
    
    <div class="splash-greeting-container">
      <h1 class="headline" id="whatchanged">WHAT CHANGED</h1>
      <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3"><div class="biline"><p>2018--this tool is under active development to better support CRISPR users everywhere. <p>The current version is in beta. In addition to implementing server upgrades and performance improvements for all versions of this site, the new version of this site will focus upon providing simple and user-friendly guides allowing researchers to quickly employ good practice guide design strategies to knock down and knock out genes in a wide variety of organisms.
	    <p>Looking for the old version of this site?<br/>Access our original 2013 Cas9 guide optimization and off-target scanning search tool, <a href="/v1/submit">here.</a></div></div></div>
    </div>
    <div class="row">
      <div class="col-xs-12 col-sm-6 col-sm-offset-3">
	<h3>Previous Versions</h3>
	<ul>
	  <li><dt>JUNE 2018 -- CRISPR DESIGN PLATFORM (*BETA)</dt>
	    <dd><a href="http://crispr.mit.edu">crispr.mit.edu</a><br/>Our second generation tool is designed to simplify the process of choosing guides in located anywhere the coding sequence of a target gene. Choose a gene and scan it for all possible guides for either Cas9 or Cpf1. <i><p>COMING SOON: RNA knock down design with Cas13.</i></dd>
	  <li><dt>JULY 2013 -- OFF TARGET OPTIMIZATION</dt></li>
	  <dd><a href="http://crispr.mit.edu/v1/submit">crispr.mit.edu/v1</a><br/>Select optimal CRISPR Cas9 target sites in a genomic locus or synthetic sequence, evaluating guide optimality in a 5--250 bp region, using off-target predictions based on <a href="http://www.nature.com/nbt/journal/v31/n9/full/nbt.2647.html">Hsu et al, Nature Biotechnology 2013</a>.</dd></li>
	</ul>
      </div>
    </div>
  </div>
</script>

<script type="unknown" id="splash-genome-link">
  <a href="/v2/{{assembly}}/submit">{{name}}</a> ({{assembly}})
</script>

<div></div>
