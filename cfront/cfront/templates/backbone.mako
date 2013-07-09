<script type="unknown" id="job-v-template">
</script>
<script type="unknown" id="job-s-v-template">
  <div class="uncategorized section">
    <p class="header">guides not yet aligned to the genome</p>
    <ul class="views">
    </ul>
  </div>
  <div class="good section">
    <p class="header">guides having very few off-target hits in the genome</p>
    <ul class="views">
    </ul>
  </div>
  <div class="bad section">
    <p class="header">guides with substantial off-target cutting in the genome</p>
    <ul class="views">
    </ul>
  </div>
</script>


<script type="unknown" id="spacer-list-v-template">
  <span class="header">Spacer <span class="rank-container">{{id}}</span></span><br/>
  <span class="position-container">position: 
    <span class="strand">{{strand == 1? "+" : "-"}}</span>
    <span class="position">{{position}}</span><br/>
  </span>
  <span class="guide" style="font-family:courier">{{guide}}</span> <span style="font-family:courier; color:blue" class="nrg">{{nrg}}</span></br/>
  <span class="score-container">score: <span class="score">{{score}}</span></span>
</script>

<script type="unknown" id="job-v-svg-container-template">
    <div class="selection-svg">
    </div>
</script>

<script id="readout-section-template" type="unknown">
  <div class="status">
    <p>locating spacers... should take a couple of seconds</p>
  </div>
  <div class="job-container"></div>
</script>
