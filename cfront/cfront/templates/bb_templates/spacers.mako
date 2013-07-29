<script type="unknown" id="spacer-v-template">
</script>
<script type="unknown" id="spacer-h-v-template">
  <span class="info">
    <h4 class="inline">guide #{{rank}}</h4>
    <dl class="header">
      <span class="guide dna">{{guide}}</span><span class="small-left-margin nrg dna">{{nrg}}</span>
      <dt>quality score </dt>
      <dd><span class="qscore">{{sprintf("%d",score*100) }}</span></dd><br/>
    </dl><br/>
    <dl>
      <dt>locus</dt>
      <dd><span class="locus description">{{locus}}</span></dd>
      <dt>#offtargets (#genic)</dt>
      <dd class="offtargets"><span class="n-top">{{n_offtargets}}</span> (<span class="n-genic">{{n_genic_offtargets}}</span>)</dd>
    </dl>
  </span>
  <span class="table-type-selection v-middle"><span class="annotation v-middle">top 20 genome-wide off-target sites</span><span class="hspace-80 dotted"></span><input class="v-middle inline " id="exonic-only" type="checkbox"><label class="v-middle inline" for="exonic-only">exonic only</label>
  </span>
  <div class="hits top">
    <table class="top top-hits">
      <thead>
	<tr>
	  <th>sequence</th>
	  <th>score</th>
	  <th>mismatches</th>
	  <th>UCSC gene</th>
	  <th>locus</th>
	</tr>
      </thead>
      <tbody> 
      </tbody>
    </table>
    <table class="gene gene-hits">
      <thead>
	<tr>
	  <th>sequence</th>
	  <th>score</th>
	  <th>mismatches</th>
	  <th>UCSC gene</th>
	  <th>locus</th>
	</tr>
      </thead>
      <tbody> 
      </tbody>
    </table>
  </div>
</script>

<script type="unknown" id="hit-v-template">
  <td class="sequence">{{sequence}}</td>
  <td class="score"> {{sprintf("%.1f",score)}}</td>
  <td class="mismatches">{{mm_string}}</td>
  <td class="gene">{{gene}}</td>
  <td class="locus">{{locus}}</td>
</script>


<!-- A view for a single spacer element in Left Column-list view -->
<script type="unknown" id="spacer-list-v-template">

  <td>Guide #<span class="rank">{{rank}}</span></td>
  <td class="center"><span class="qscore">{{sprintf("%d",score*100)}}</span></td>
  <td><span class="guide dna">{{guide}}</span><span class="nrg dna small-left-margin">{{nrg}}</span></td>

  <span class="hover">
    <span class="position-container">position: 
      <span class="strand">{{strand == 1? "+" : "-"}}</span>
      <span class="position">{{position}}</span><br/>
    </span>
    <span class="guide dna">{{guide}}</span><span class="nrg dna small-left-margin">{{nrg}}</span>
    <span class="score-container">quality score: <span class="score"><b>{{score}}</b></span></span>
  </span>
</script>
