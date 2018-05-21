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
	  <div class="biline"><p>Please choose a target organism to target with Crispr CAS-9, CPCF1, or CAS13.</div>
      </div></div>
    </div>

    <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3">
	<ul id="genome-v2-links"></ul>
    </div></div>

    <div class="splash-greeting-container">

      <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3"><div class="biline"><p>Working with a target organism not yet included in this list? Please feel free to suggest it for inclusion on the stickied "ADDITIONAL GENOMES THREAD" on the crispr.mit.edu <a href="https://groups.google.com/forum/#!forum/crispr">forum</a></div></div></div>
    </div>
    
    <div class="splash-greeting-container">
      <h1 class="headline" id="whatchanged">WHAT CHANGED</h1>
      <div class="row"><div class="col-xs-12 col-sm-6 col-sm-offset-3"><div class="biline"><p>SPR 2018--this tool is under active development to achieve the Zhang lab goal of making Crispr a more accessible technology for researchers everywhere. <p>The current version is in beta. In addition to implementing server upgrades and performance improvements for all versions of this site, the new version of this site will focus upon providing simple, and user-friendly guides allowing researchers to quickly employ good practice guide design strategies to knock down and knock out genes in a wide variety of organisms.
	    <p>Looking for the old version of this site?<br/>Access our original 2013 CAS-9 guide optimization and offtarget scanning search tool, <a href="/v1/submit">here.</a></div></div></div>
    </div>
    <div class="row">
      <div class="col-xs-12 col-sm-6 col-sm-offset-3">
	<h3>Previous Versions</h3>
	<ul>
	  <li><dt>JUNE 2018 -- CRISPR DESIGN PLATFORM (*BETA)</dt>
	    <dd><a href="crispr.mit.edu/v1/submit">crispr.mit.edu</a><br/>Our second generation tool is designed simplify the process of choosing guides in located anywhere in a target gene. Choose a gene and scan for all possible guides amongst multiple Crispr modules to Knock out a gene. Currently supported are CAS-9 and CPCF-1. <i><p>COMING SOON: RNA knock down design with CAS-13.</i></dd>
	  <li><dt>JULY 2013 -- OFF TARGET OPTIMIZATION</dt></li>
	  <dd><a href="crispr.mit.edu/v1/submit">crispr.mit.edu/v1</a><br/>Select optimal Crispr CAS-9 target sites in a genomic locus or synthetic sequence, evaluating guide optimality in a 5--250 bp region, using off-target predictions based on <a href="http://www.nature.com/nbt/journal/v31/n9/full/nbt.2647.html">Hsu et al, Nature Biotechnology 2013</a>.</dd></li>
	</ul>
      </div>
    </div>
  </div>
</script>

<script type="unknown" id="splash-genome-link">
  <a href="/v2/{{assembly}}/submit">{{name}}</a> ({{assembly}})
</script>

<div></div>
