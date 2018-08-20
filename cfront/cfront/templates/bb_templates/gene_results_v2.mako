<script type="unknown"  id="gene-results-v2-section-template">

  <div class="fixed-width-header title">
	  <div class="header">
    <h1 class="header-oneword title">{{name}} knockout guide</h1>
	  </div>
	  </div>
  
  <% from cfront import cfront_settings %>

  <ul class="nav nav-tabs">
    <li class="active"><a href="#knockout" data-toggle="tab">Knock out with CAS9 or CPCF1</a></li>
  </ul>
  
  <div class="tab-content">
    <div id="knockout" name="knock out" class="tab-pane  active">
      <div class="hero">


	<div class="fixed-width-header">
	  <div class="biline">1. ADJUST RANGE to select target exons in {{genome_name}} ({{assembly}}) gene, {{gene_name}}. [Click to target one exon]</div>
	  
	  <div class="selection-container">
	    <div id="drawing" class="gene">	  
	    </div>
	    
            <div class="content-width-600 selection-slider-container">
	      <div id="slider"></div>
	    </div>
	    
	    <div class="content-width-600"><p>Selected range: <span class="range-in-genome"></span></p><p>Evaluating <span class="guide-in-range-count"></span> guides which target <span class="bold"><span class="exon-count"></span> EXON(s)</span> between positions <span class="bold range-start"></span> and <span class="bold range-end"></span> of gene {{gene_name}} of {{genome_name}} ({{assembly}}). Read on for guide recommendations or adjust targeting range by sliding the window above.</p></div>
	    
	    
	  </div>
	  <div id="hero-spacers">	  
	  </div>
	</div>
      </div>
      <div class="row">
	<div class="col-xs-12">
	  <div class="fixed-width-header">
	    <div class="background-stripe"></div>
	    <div class="header-container"><h2>Selected guide</h2><div class="hiline"><a class="download-guide-gb underline disabled" id="download-guide-gb" target="_blank">...download to genbank file</a></div></div>
	    <div class="spacer-details" id="spacer-details-container">
	      
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
      <h2>Top guides</h2>
      <div class="hiline">
	<div><a id="download-selected" class="disabled" target="_blank">...export selected guides</a>
	</div>
      </div>
    </div>
    <div class="biline">2. CHOOSE A GUIDE targeting {{exons_string}} in {{genome_name}} gene, {{gene_name}} with Cpf1 and Cas9 (or  <span><a id="download-all" target="_blank" href="/v2/{{assembly}}/{{geneid}}/top_spacers.gb">download all guides</a>.</span>)</div>

  </div>
  <form>
  <table>
    <tr>
      <th class="select-radio"></th>
      <th><label for="export-all">export</br>all</label></br><input id="export-all" class="export-all" type="checkbox"/></th>
      <th>guide</th>
      <th>exon</th>
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
  <td class="select-radio"><input guide_sequence="{{guide_sequence}}" class="show-details" name="details" type="radio"/></td>
  <td><input name="{{guide_sequence}}" class="export" type="checkbox"/></td>
  <td class="seq"><span class="pam-before ">{{pam_before != null?pam_before:""}}</span>
  <span class="guide-sequence ">{{guide_sequence}}</span>
  <span class="pam-after ">{{pam_after != null?pam_after:""}}</span>
  </td>
  <td>{{exon_name}}</td>
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
  <h4>Guide info</h4>
  <dl>
    <dt>CRISPR tool type</dt><dd><span class="{{spacer.tool}}">{{spacer.tool}}</span></dd><br/>
    <dt>guide sequence</dt><dd>{{spacer.guide_sequence}}</dd><br/>
    <dt>5' pam sequence</dt><dd>{{spacer.pam_before?'<span class="pam-before">'+spacer.pam_before+'</span>':"(N/A)"}}</dd><br/>
    <dt>3' pam sequence</dt><dd>{{spacer.pam_after?'<span class="pam-before">'+spacer.pam_after+'</span>':"(N/A)"}}</dd><br/>
    <dt>target exon name</dt><dd>{{exon_name}}</dd><br/>
    <dt>target exon start {{gene.Name[0]}}</dt><dd>{{exon_start}}</dd><br/>
    <dt>on-target strand</dt><dd>{{spacer.guide_strand}}</dd><br/>
    <dt># predicted off-targets</dt><dd>{{spacer.offtarget_count}}</dd><br/>
    <dt>Hsu, 2013 score</dt><dd>{{spacer.score}}</dd><br/>
  </dl>

  <h4>On-target cut site</h4>

  <div id="cutsite" class="svg">
  </div>
  
  <h4>On-target exon sequence</h4>
  <div>>{{exon_name}} ({{assembly}} {{gene.Name[0]}}) guide {{'<span class="pam-before">'+(spacer.pam_before!=null?spacer.pam_before:'')+'</span>'}}{{spacer.guide_sequence}}{{'<span class="pam-before">'+(spacer.pam_after!=null?spacer.pam_after:'')+'</span>'}}</div>
  <div class="exon-sequence-container letters"></div>
  
  <h4>Off-target predictions</h4>
  <div class="ot-table-container empty">
    <div class="if-empty">
      No predicted off-target hits with less than 3 mismatches found for {{spacer.tool}} guide sequence: <span class="bold">{{spacer.guide_sequence}}</span> in {{assembly}}. This guide is recommended.
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
