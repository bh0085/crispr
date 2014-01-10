<script type="unknown" id="nickase-v-template">
  <div class="content-area">

    <div class="page-header">
      <h3>Double Nickase Design</h3>
      <div>Find double nicking pairs within your query input.<span class="right" style="float:right;"><a class="export export-all-pairs" target="_blank" href="{{export_gb_nicks_url}}">Export all pairs to Genbank</a></span></div>
    </div>

    <div class="pane pane2 nick-list-container">
      <div class="page-header">
	<h4>All Pairs</h4>
	<div>Sorted by score.</div>
	<div><a class="explain-scores">See how scores are computed </a></div>
	
	<div style="display:none;" class="scores-explanation">
	  Scores for each pair gX<-->gY are a product of three factors.<br/>
				    S(gX,gY) = s(gX) * s(gY) * OT(gX,gY)<br/>
				    Where s(gX/Y) are standard offtarget scores, computed per guide see <a href="/about">/about</a><br/>
				    And OT(g1,g2) is a weighting factor which penalizes guide pairs having potential double-nicking offtargets.
				    </div>

				    </div>
				    <div class="click-grabber"> </div>				
				    <div class="nicks-list">
				    </div>
				    </div>
				    

				    <div class="hover-helper">
				    </div>
				    <div class="right panes">
      <div class="pane1 pane">

	<div class="page-header">
	  <h4>Top Pairs</h4>
	  <div>Filtered by region</div>
	</div>


	<div class="nickase-tl-options-container">
	</div>
	<div class="main graphics">
	</div>
	<div class="click-grabber"> </div>				
      </div>

      <div class="main details details pane pane3">
      </div>
    </div>
  </div>
</script>

<!-- A view for a single spacer selement in Left Column-list view -->
<script type="unknown" id="nickase-list-v-template">
  <td>{{"N<span class=rank>"+rank+"</span>"}}</td>
  <td>{{name}}</td>
  <td class="center"><span class="">{{sprintf("%d",score)}}</span></td>
</script>

<script type="unknown" id="job-svg-view-template">
  <div class="main-svg-canvas"></div>
</script>

<script type="unknown" id="nickase-svg-view-template">
  <div class="main-svg-canvas"></div>
  <div class=""> </div>
</script>


<script type="unknown" id="nickase-tl-options-template">
  Filter by subregion.<br/>
  <form class="form-horizontal">
    <div class="control-group">
      <div class="controls">
	<label class="radio input-type-select">
	  <input checked=true class="entire-region" type="radio" name="group1">No filter <span class='med-margin-left annotation'>(finds all guide pairs in the query sequence).</span></input>
	</label>
	<label class="radio input-type-select">
	  <input type="radio" class="spanning-region" name="group1"></input>Only guide pairs spanning a subregion from base(s) <span class="active-region-start-display">??</span> to <span class="active-region-end-display">??</span>  <span class='med-margin-left annotation'>(drag below specify a region)</span>
	</label>
	
      </div>
    </div> 
  </form>
  <div class="full-width-bottom">
    Choose from one of the top-ten guide pairs or view all below.<span class="right"><a class="explain-this-view">Explain this View</a></span>
  </div>
  <span style="display:none;" class="explanation">
    Horizontal bars indicate possible guide pairs for CAS-9 double nickase over the input query. <span style="color:green;">Green</span> pairs are recommended.<br/>Arrows indicate cut sites of guides on each strand. <span style="color:green;">Green</span> arrows correspond to guides having low offtarget activity.<br/>Please select from all recommended guide pairs or drag a selection below to indicate that guides pairs should span a query subregion.
  </span>

</script>


<script type="unknown" id="nickase-detail-v-template">
  <div class="page-header">
    <h4 class="nickase-detail-title">Guide pair NICKING details</h4>
    <div>For guides {{name}}</div>
    <div><a class="export export-active-nick" href="{{export_gb_url}}" target="_blank">Export this info</a></div>
  </div>

  <div class="details-svg-container">
  </div>

  <div class="sequence-details-container"></div>
  <div>SCORE: <b>{{Math.round(score*10)/10}} ({{quality}})</b></div>
  <div>ranked #{{rank}} by quality for this query</div>
  <div>{{n_offtargets}} off target nicks are likely</div>
  <div>{{n_genic_offtargets}} off target nicks are in genes</div>

  <div class=spacers>
    <span class="spacer forward">
      <h5 class="guide-title">FORWARD guide g{{forward_guide.rank}}</h5>
      <dl>
	<dt>score</dt><dd>{{Math.round(forward_guide.score*100)}} of 100</dd><br/>
	<dt>cut site</dt><dd>{{forward_guide.cut_site}}</dd><br/>
	<dt>sequence</dt><dd class="sequence">{{forward_guide.sequence}}</dd><br/>
      </dl>
    </span>
    <span class="spacer reverse">
      <h5 class="guide-title">REVERSE guide g{{reverse_guide.rank}}</h5>
      <dl>
	<dt>score</dt><dd>{{Math.round(reverse_guide.score * 100)}} of 100</dd><br/>
	<dt>cut site</dt><dd>{{reverse_guide.cut_site}}</dd><br/>
	<dt>sequence</dt><dd class="sequence">{{reverse_guide.sequence}}</dd><br/>
      </dl>
    </span>
  </div>
</script>

 <!-- variables to trigger interface updates 
included-nicks-count-display
active-region-width-display
active-region-end-display
active-region-start-display

-->



<!-- A view containing all spacers in the left column -->
<script type="unknown" id="job-nicks-list-v-template">
  <table>
    <thead>
      <tr> 
	<th></th>
	<th class="center">guides</th>
	<th class="center">score</th>
      </tr>
    </thead>
    <tbody class="views"></tbody>
  </table>
</script>
