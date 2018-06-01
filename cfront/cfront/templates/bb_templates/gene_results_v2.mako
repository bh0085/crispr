<script type="unknown"  id="gene-results-v2-section-template">

  <div class="fixed-width-header">
	  <div class="header">
    <h1 class="header-oneword title">{{name}}</h1>
	  </div>
	  </div>
  
  <% from cfront import cfront_settings %>

  <ul class="nav nav-tabs">
    <li class="active"><a href="#knockout" data-toggle="tab">Knock out with CAS9 or CPCF1</a></li>
  </ul>
  
  <div class="tab-content">
    <div id="knockout" name="knock out" class="tab-pane  active">
      <div class="hero">
	<div class="selection-container">
	  <div id="drawing" class="gene">	  
	  </div>
	  
          <div class="content-width-600 selection-slider-container">
	    <div id="slider"></div>
	  </div>
	  <div class="content-width-600">Selecting guides which target <span class="exon-count"></span> exons between bases <span class="range-start"></span> and <span class="range-end"></span> of gene {{gene_name}} of {{genome_name}} ({{assembly}}). Read on for guide recommendations or adjust targeting range by clicking an exon or sliding the window above. </div>
	  
	  
	</div>
	<div id="hero-spacers">	  
	</div>
	
      </div>
      <div class="row">
	<div class="col-xs-12">
	  <div class="fixed-width-header">
	    <div class="background-stripe"></div>
	    <div class="header-container"><h2>GUIDE DETAILS</h2><div class="hiline"><a class="download-guide-gb underline disabled" id="download-guide-gb" target="_blank">...download to genbank file</a></div></div>
	    <div class="biline">select a guide above to view details</div>

	    <div class="spacer-details" id="spacer-details-container">
	      
	    </div>
	  </div>
	</div>
      </div>
      
      
      
      <div class="row">
	<div class="col-xs-12">
	  <div class="fixed-width-header">
	    <div class="background-stripe"></div>
	    <div class="header-container"><h2>SEQUENCE VIEW</h2><div class="hiline"><a class="download-letters underline" href="/v2/{{assembly}}/{{geneid}}/top_spacers.gb" target="_blank">...download as genbank</a></div></div>
	    <div class="biline">view guide sequences in exonic context</div>
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
	<div><a id="download-selected" class="disabled" target="_blank">...download selected guides</a>
	</div>
      </div>
    </div>
    <div class="biline">top guide choices from bases <span class="start-base"></span>..<span class="end-base"></span></div>
  </div>
  <form>
  <table>
    <tr>
      <th>show</br>details</th>
      <th><label for="export-all"> export all</label></br><input id="export-all" class="export-all" type="checkbox"/></th>
      <th>guide</th>
      <th>tool</th>
      <th>score</th>
      <!--
	  <th>ov</th>
      <th>es</th>
      <th>av</th>
    <th>as</th>
    <th>vs</th>
    -->
  </tr>
  </table>
  </form>
</script>

<script type="unknown" id="spacer-oneline-header-template">
  <div class="line one"><span class="pam before">{{pam_before}}</span><span class="spacer">{{guide_sequence}}</span><span class="sequence"></span><span class="pam after">{{pam_after}}</span>[<span class="score">{{Math.floor(score)}}</span>]</div>
</script>

<script type="unknown" id="spacer-oneline-result-template">
  <div class="line one"><span class="pam before">{{pam_before}}</span><span class="spacer">{{guide_sequence}}</span><span class="sequence"></span><span class="pam after">{{pam_after}}</span></div><div>hsu 2013 score: {{Math.floor(score)}}</div>
</script>

<script type="unknown" id="hero-spacer-template">
  <td><input guide_sequence="{{guide_sequence}}" class="show-details" name="details" type="radio"/></td>
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
</script>

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


<script type="unknown" id="spacer-detail-view-template">
  guide detail view for {{spacer.guide_id}}, ({{spacer.guide_sequence}})
  <dl>
    <dt>tool</dt><dd>{{spacer.tool}}</dd>
    <dt>5' pam</dt>{{spacer.pam_before}}<dd></dd>
    <dt>3' pam</dt><dd>{{spacer.pam_after}}</dd>
    <dt>on target locus</dt><dd>{{spacer.chrom}} {{spacer.guide_start + gene.start}}</dd>
    <dt>strand</dt><dd>{{spacer.guide_strand}}</dd>    
  </dl>

  <h3>offtarget alignments</h3>
  <div class="ot-table-container empty">
    <div class="if-empty">
      no off-targets with less than 3 mismatches found for {{spacer.guide_sequence}} with {{spacer.tool}} in {{assembly}}
    </div>
    <div class="if-full">
      <table class="ot-table">
      <tr><th>offtarget position</th><th>mismatches</th></tr>
      

      </table>
    </div>
  </div>
</script>


<script type="unknown" id="offtarget-spacer-row-template">

  <tr>
    <td>{{a.chrom}} {{a.start}} {{a.strand}}</td>
    <td>{{a.mismatches}}</td>
  </tr>
</script>
