<script type="unknown"  id="gene-results-v2-section-template">

  <div class="fixed-width-header">
	  <div class="header">
    <h1 class="header-oneword title">{{name}}</h1>
	  </div>
	  </div>
  
  <% from cfront import cfront_settings %>

  <ul class="nav nav-tabs">
    <li class="active"><a href="#knockout" data-toggle="tab">Knock out with CAS9 or CPCF1</a></li>
    <li class=""><a href="#knockdown" data-toggle="tab">Knock down with CAS13 **BETA**</a></li>
  </ul>
  
  <div class="tab-content">
    <div id="knockdown" name="knock down" class="tab-pane ">
      <div class="header-description">in testing... knock down a transcript with cas 13</div>
    </div>
    <div id="knockout" name="knock out" class="tab-pane  active">

      

      <div class="fixed-width-header">
	<h2>CHOOSE A SUBREGION</h2>
	<div class="biline">
	  <div>Drag to select a subregion</div> 
	</div>
      </div>
      
      

      <div class="hero">
	<div class="selection-container">
	  <div id="drawing" class="gene">	  
	  </div>
	  
	</div>
	<div id="hero-spacers">
	  
	  
	</div>
	
      </div>
      <div class="row">
	<div class="col-xs-12">
	  <div class="fixed-width-header">
	    <div class="background-stripe"></div>
	    <div class="header-container"><h2>SEQUENCE VIEW</h2><div class="hiline"><a class="download-letters underline">...download as genbank</a></div></div>
	    <div class="biline">view guide sequences in exonic content</div>
	  </div>
	  <div class="gene-view-container">
	    <div class="gene-view">
	      <div class="letters">
	      </div>
	    </div>
	  </div>
	</div>
      </div>
    </div>
  </div>
</script>


<script type="unknown" id="hero-spacers-table-template">
  <div class="fixed-width-header">

    <div class="header-container">
      <div class="background-stripe"></div>
      <h2>SUGGESTED GUIDES</h2>
      <div class="hiline">
	<div><a href="/v2/{{genome_assembly}}/{{gene_info.id}}/top_spacers.gb">...download selected guides</a>
	</div>
      </div>
    </div>
    <div class="biline">top guide choices from bases <span class="start-base"></span>..<span class="end-base"></span></div>
  </div>

  <table>
  <tr>
    <th><input class="export-all" type="checkbox"/></th>
    <th>guide</th>
    <th>tool</th>
    <th>ot</th>
    <!--
    <th>ov</th>
    <th>es</th>
    <th>av</th>
    <th>as</th>
    <th>vs</th>
    -->
  </tr>
  </table>
</script>

<script type="unknown" id="spacer-oneline-header-template">
  <div class="line one"><span class="pam before">{{pam_before}}</span><span class="spacer">{{guide_sequence}}</span><span class="sequence"></span><span class="pam after">{{pam_after}}</span>[<span class="score">{{Math.floor(score)}}</span>]</div>
</script>

<script type="unknown" id="spacer-oneline-result-template">
  <div class="line one"><span class="pam before">{{pam_before}}</span><span class="spacer">{{guide_sequence}}</span><span class="sequence"></span><span class="pam after">{{pam_after}}</span></div><div>hsu 2013 score: {{Math.floor(score)}}</div>
</script>

<script type="unknown" id="hero-spacer-template">
  <td><input name="{{guide_sequence}}" class="export" type="checkbox"/></td>
  <td class="seq"><span class="pam-before ">{{pam_before != null?pam_before:""}}</span>
  <span class="guide-sequence ">{{guide_sequence}}</span>
  <span class="pam-after ">{{pam_after != null?pam_after:""}}</span>
  </td>
  <td class="tool {{tool}}">{{tool}}</td>
  <td class="flag hsu">{{Math.floor(score)}}</td>
  <!--
  <td class="flag overall"></td>
  <td class="flag exonic-offtargets"><input disabled="true" type="checkbox"/></td>
  <td class="flag human-only avana-guide"><input disabled="true" type="checkbox"/></td>
  <td class="flag mouse-only asiago-guide"><input disabled="true" type="checkbox"/></td>    
  <td class="flag human-only variant-safe"><input disabled="true" type="checkbox"/></td>
  -->
</space>

<script type="unknown" id="results-waiting-template">
  <div class="row">
    <div class="col-sm-6 col-sm-offset-3">
      <h1>
	... awaiting results ...
      </h1>
      <div>please sit tight while your results are being computed</div>
      <div>if you need to return to this job later, you can use this link:</div>
      <a href="{{location}}">{{location}}</div>
</script>
