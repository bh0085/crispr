<script type="unknown"  id="gene-results-v2-section-template">
  <div class="header">
    <h1 class="header-oneword">{{name}}</h1>
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
      <div class="header-description"><p>{{description}}</p><p style="color:black;">Selected genome: <b>{{genome_name}}</b> ({{genome_assembly}}).</div>
      <div class="row">
	<div class="gene-view-container col-sm-8 col-sm-offset-2">
	  <div class="gene-view">
	    <div class="letters">
	    </div>
	  </div>
	</div>
      </div>
    </div>

  </div>

</script>


<script type="unknown" id="spacer-oneline-result-template">
  <div class="line one"><span class="pam before">{{pam_before}}</span><span class="spacer">{{guide_sequence}}</span><span class="sequence"></span><span class="pam after">{{pam_after}}</span></div><div>hsu 2013 score: {{score}}</div>
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
