<script type="unknown" id="spacer-h-v-template">
  
  <div class="header">
    <h4>guide #{{rank}} details</h4>
  </div>
  <div class="info">

    <dl>
      <dt>sequence</dt>
      <dd><span class="dna">{{sequence}}</span></dd>
      <dt>quality</dt>
      <dd><span class="score">{{sprintf("%d",score*100) }}%</span></dd>
      <dt>locus</dt>
      <dd><span class="description">{{locus}}</span></dd>
      <dt>number of offtarget sites in genome</dt>
      <dd class="n-top">{{n_offtargets}}</dd>
      <dt>number of genic offtargets</dt>
      <dd class="n-genic">{{gene_hits.length}}</dd>
    </dl>
  </div>
  <div class="hits">
    <div class="header"><span class="table-type-selection">show genome-wide offtarget hits: <a name="top" class="current">...top 50</a> <a hname="genic">...exonic</a></span></div>
    <table>
      <thead>
	<tr>
	  <th>sequence</th>
	  <th>score</th>
	  <th>mismatches</th>
	  <th>gene</th>
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
  <td class="score"> {{sprintf("%d",score)}}%</td>
  <td class="mismatches">{{n_mismatches}} ({{n_mismatches > 0 ? mismatches : "ontarget"}})</td>
  <td class="gene">{{gene}}</td>
  <td class="locus">{{locus}}</td>
</script>


<!-- A view for a single spacer element in Left Column-list view -->
<script type="unknown" id="spacer-list-v-template">

  <td>Guide #<span class="rank">{{rank}}</span></td>
  <td class="center"><span class="score">{{sprintf("%d",score*100)}}</span></td>
  <td><span class="guide dna">{{guide}}</span><span class="nrg dna">{{nrg}}</span></td>

  <span class="hover">
    <span class="position-container">position: 
      <span class="strand">{{strand == 1? "+" : "-"}}</span>
      <span class="position">{{position}}</span><br/>
    </span>
    <span class="guide dna">{{guide}}</span><span class="nrg dna">{{nrg}}</span>
    <span class="score-container">score: <span class="score">{{score}}</span></span>
  </span>
</script>
