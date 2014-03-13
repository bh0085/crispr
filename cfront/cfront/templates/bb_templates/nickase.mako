<script type="unknown" id="nickase-v-template">
  <div class="content-area">

    <div class="">
      <h3>Double Nickase Design</h3>
    </div>
    <div class="top panes">
      <div class="click-grabber"></div>				
      <div class="pane left pane2 nick-list-container">
	<div class="">
	  <h4>All Pairs</h4>
	  <div>Sorted by score.</div>
	  <div><a class="export export-all-pairs" target="_blank" href="{{export_gb_nicks_url}}">Export all pairs to GENBANK</a></div>
	  
	  <div style="display:none;" class="scores-explanation">"explanation temporarily removed"</div>

	</div>
	<div class="nicks-list">
	</div>
      </div>
      <div class="pane1 right pane">
	<div class=" nickase-tl-header">
	  <h4>Top Pairs</h4>
	  <div>View top pairs by overhang subregion.</div>
	  <div class="nickase-tl-options-container">
	  </div>
	  <div class="full-width"><span class="right" style="float:right;"><a class="explain-this-view">Explain this View</a></span></div>
	</div>
	<div class="main graphics">
	</div>
      </div>
    </div><!-- top panes end -->
    <div class="bottom panes">
      <div class="main details details pane pane3">
      </div>
    </div>
    </div>
  </div>
</script>

<!-- A view for a single spacer selement in Left Column-list view -->
<script type="unknown" id="nickase-list-v-template">
  <td>{{"#<span class=rank>"+rank+"</span>"}}</td>
  <td>{{start}} .. {{end}}</td>
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
  <form class="form-horizontal">
    <div class="control-group">
      <div class="controls">
	<label class="radio input-type-select">
	  <input checked=true class="entire-region" type="radio" name="group1">No filter <span class='med-margin-left annotation'>(finds all guide pairs in the query sequence).</span></input>
	</label>
	<label class="radio input-type-select">
	  <input type="radio" class="spanning-region" name="group1"></input>Guide pairs overlapping a subregion from base(s) <span class="active-region-start-display">??</span> to <span class="active-region-end-display">??</span>  <span class='med-margin-left annotation'>(drag below specify a region)</span>
	</label>
	
      </div>
    </div> 
  </form>
  <span style="display:none;" class="explanation">
    Horizontal bars indicate possible guide pairs for CAS-9 double nickase over the input query. <span style="color:green;">Green</span> pairs are recommended.<br/>Arrows indicate cut sites of guides on each strand. <span style="color:green;">Green</span> arrows correspond to guides having low offtarget activity.<br/>Please select from all recommended guide pairs or drag a selection below to indicate that guides pairs should span a query subregion.
  </span>

</script>


<script type="unknown" id="nickase-detail-v-template">

  <div class="full-width header page-header">
    <h4 class="nickase-detail-title">{{start}} .. {{end}}</h4>
    <span class="hover-helper"></span>
    <span class="right" style="float:right;"><a class="export export-active-nick" href="{{export_gb_url}}" target="_blank">Export to GENBANK</a></span>
  </div>


  <div class="details-svg-container">
  </div>

  <div class="cards">
    <div class="sequence-section card">
      <h5 class="header">Overhang region</h5>
      <div class="sequence-details-container">
      </div>
    </div>
    

    <div class="spacer reverse card {{reverse_guide.quality}}">
      <h5 class="header">Guide A</h5>
      <div class='qbox'><span>{{Math.round(reverse_guide.score*100)}}</span></div>

	<dl>
	  <dt>quality</dt><dd>{{reverse_guide.quality}}</dd>
	  <dt>cuts after position</dt><dd>{{reverse_guide.cut_site}} in query</dd>
	  <dt>sequence</dt><dd class="sequence">{{reverse_guide.sequence}}</dd>
	  <dt># offtargets</dt><dd>{{reverse_guide.n_offtargets}}</dd>
	  <dt># genic offtargets</dt><dd>{{reverse_guide.n_genic_offtargets}}</dd>
	  <div><a class="export export-one-guide" target="_blank" href="{{export_csv_reverse_guide_url}}">Export off-targets to .csv</a></div>

	</dl>
    </div>
    <div class="spacer forward card {{forward_guide.quality}}">
      <div class='qbox'><span>{{Math.round(forward_guide.score*100)}}</span></div>

      <h5 class="header">Guide B</h5>
	<dl>
	  <dt>quality</dt><dd>{{forward_guide.quality}}</dd>
	  <dt>cuts after position</dt><dd>{{forward_guide.cut_site}} in query</dd>
	  <dt>sequence</dt><dd class="sequence">{{forward_guide.sequence}}</dd>
	  <dt># offtargets</dt><dd>{{forward_guide.n_offtargets}}</dd>
	  <dt># genic offtargets</dt><dd>{{forward_guide.n_genic_offtargets}}</dd>
	  <div><a class="export export-one-guide" target="_blank" href="{{export_csv_forward_guide_url}}">Export off-targets to .csv</a></div>
	</dl>
    </div>
    <div class="score card {{quality}}">
      <h5 class="header">Pair score, A & B</h5>
      <div class='qbox'><span>{{Math.round(score)}}</span></div>
	<dl>
	  <dt>quality</dt><dd>{{quality}}</dd>
	  <dt># offtarget pairs of A & B</dt><dd class="sequence">{{n_offtargets}}</dd>
	  <dt># genic OT pairs of A & B</dt><dd class="sequence">{{n_genic_offtargets}}</dd>
	</dl>
    </div>

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
	<th class="center"></th>
	<th class="center">range</th>
	<th class="center">score</th>
      </tr>
    </thead>
    <tbody class="views"></tbody>
  </table>
</script>




<svg style="display:none;" version="1.1" id="pacman-inline" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 width="612px" height="792px" viewBox="0 0 612 792" enable-background="new 0 0 612 792" xml:space="preserve">
<path fill="#FAF7BF" opacity=".25" d="M22.41-13.932h-0.023c-5.496,0-11.557,1.644-15.438,3.144C-0.108-8.072-7.146-3.576-12.402,1.985
	c-5.259,5.562-8.723,12.176-8.722,19.139c0.001,4.149,1.225,8.438,4.059,12.746c1.95,2.965,5.664,5.891,10.138,8.049
	c4.471,2.162,9.699,3.566,14.669,3.566h0.006c0.277,0,0.555-0.004,0.83-0.014l0.014,0.396l0.017-0.396
	c0.976,0.045,2.036,0.072,3.152,0.072h0.021c3.874,0,8.428-0.332,12.475-1.449c4.058-1.115,7.58-3.016,9.469-6.094
	c0.932-1.517,1.301-2.898,1.303-4.211c0.004-2.543-1.422-4.904-3.145-7.291c-1.715-2.39-3.703-4.783-4.684-7.47
	c-0.49-1.349-0.705-2.61-0.705-3.796c0-1.924,0.566-3.643,1.398-5.232c1.249-2.386,3.087-4.506,4.591-6.709
	c1.507-2.205,2.671-4.465,2.671-7.131c0-0.498-0.041-1.014-0.128-1.548c-0.547-3.286-2.144-5.378-4.382-6.702
	C28.408-13.408,25.501-13.932,22.41-13.932"/>
<path fill="#E1B8A0" d="M22.398-13.932h0.012c3.092,0,5.998,0.524,8.234,1.843c2.238,1.325,3.836,3.416,4.381,6.702
	c0.088,0.534,0.129,1.05,0.129,1.548c0,2.666-1.164,4.926-2.671,7.131C30.979,5.495,29.141,7.615,27.892,10
	c-0.831,1.59-1.398,3.309-1.398,5.232c0,1.186,0.215,2.447,0.705,3.796c0.98,2.687,2.969,5.08,4.684,7.47
	c1.722,2.387,3.15,4.748,3.144,7.289c-0.001,1.314-0.37,2.696-1.301,4.213c-1.89,3.078-5.412,4.979-9.47,6.094
	c-4.047,1.117-8.601,1.449-12.476,1.449h-0.02c-1.117,0-2.177-0.027-3.151-0.072l-0.018,0.396l-0.014-0.396
	c-0.275,0.01-0.553,0.014-0.83,0.014H7.742c-4.969,0-10.197-1.404-14.669-3.566c-4.474-2.158-8.188-5.082-10.137-8.049
	c-2.836-4.309-4.059-8.597-4.06-12.746c-0.001-6.963,3.463-13.576,8.722-19.139C-7.146-3.576-0.108-8.072,6.948-10.791
	c3.882-1.498,9.943-3.142,15.438-3.142H22.398 M22.482-14.723h-0.168c-5.629,0.019-11.71,1.677-15.65,3.194
	C-0.5-8.767-7.624-4.219-12.977,1.442c-5.35,5.658-8.937,12.447-8.938,19.682c-0.001,4.308,1.278,8.76,4.189,13.18
	c2.074,3.146,5.886,6.117,10.454,8.328c4.57,2.207,9.9,3.645,15.02,3.645c0.278,0,0.56-0.004,0.84-0.014
	c0.983,0.045,2.055,0.072,3.183,0.072c3.921,0,8.537-0.33,12.694-1.476c4.154-1.146,7.88-3.11,9.934-6.444
	c0.998-1.617,1.421-3.158,1.419-4.627c-0.004-2.849-1.56-5.34-3.293-7.752c-1.739-2.414-3.675-4.773-4.581-7.277
	c-0.461-1.271-0.656-2.434-0.656-3.525c-0.002-2.646,1.162-4.895,2.67-7.096c1.504-2.197,3.342-4.322,4.59-6.717
	c0.832-1.596,1.399-3.324,1.399-5.26c0-0.543-0.045-1.101-0.139-1.676c-0.567-3.486-2.338-5.836-4.761-7.255
	C28.646-14.182,25.635-14.712,22.482-14.723"/>
<path fill="none" stroke="#AE1F24" stroke-width="0.791" d="M-0.078,0c-10.695,3.765-22.897-5.539-33.827-5.107"/>
<path fill="none" stroke="#B53033" stroke-width="0.791" d="M5.233-10.08c-2.551-0.75-1.752-3.688-1.64-5.998
	c0.044-0.975,0.865-2.676,0.949-3.635c0.156-1.85-3.4-1.9-4.176-0.377c-0.591,1.157,0.066,3.078,0.32,4.256
	c0.57,2.653,0.204,5.793-0.757,8.381c-0.273,0.721-1.554,2.014-1.471,2.004C-2.727-4.96-3.388-4.805-4.634-4.644
	c-1.24,0.16-2.493,0.162-3.734,0.037c-2.53-0.254-5.05-0.902-7.504-1.621c-2.528-0.736-5.002-1.67-7.52-2.436
	c-2.441-0.738-4.94-1.371-7.464-1.676c-1.15-0.139-2.277-0.152-3.392-0.055"/>
<path fill="none" stroke="#AE1F24" stroke-width="0.791" d="M-33.745-5.123c-1.207,0-2.591-0.562-3.116-1.705
	c-0.812-1.752,0.936-3.629,2.684-3.576"/>
</svg>

