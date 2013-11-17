<script type="unknown" id="about-section-template">
  <div class="row med-margin-top">
    <div id="purpose" class="span6 offset2">
      <h1>About CRISPR Design</h1>
      <h3>Purpose of the CRISPR Design Tool</h3>
      <p>The CRISPR design tool is a web tool crafted to simplify the process of CRISPR guide selection in an input DNA sequence by (i) discovering possible offtargets genome-wide, (ii) highlighting guides with high target specificity, and (iii) flagging guides with numerous or genic offtargets in target genomes.</p>
    </div>
  </div>

  <div class="row med-margin-top">
    <div id="using" class="span6 offset2">
      <h3>Using CRISPR Design</h3>
      <p>To use the CRISPR design web tool, simply: <ol><li>head over to submission page at <a href="crispr.mit.edu">crispr.mit.edu</a> </li><li>enter in a DNA sequence</li><li>choose a target genome, </li></ol> and click submit. </p><p>The sequence will be scanned for possible CRISPR guides (20 nucleotides followed by a PAM sequence: NGG) and scanned for possible offtarget matches throughout the selected genome. Job output will be presented on the job output page with each guide linked to a list of offtargets and presented in the order of their score from zero to 100% roughly indicating the faithful on-target activity of each guide.</p>
    </div>
  </div>

  <div class="row med-margin-top">
    <div id="score" class="span6 offset2">
      <h3>Interpreting Scores</h3>
      <p>The CRISPR design tools output page:</p>
      <img  style="margin:10px; max-width:auto;" src="/img/output_preview.gif"></img>
      <p>presents a ranked list of all possible guides in the query sequence ordered by faithfullness of on-target activity computed as 100% minus a weighted sum of offtarget hit-scores in the target genome.</p>
      <p>Offtarget hit scores are displayed for top matches of each guide and are computed by taking into account total number of mismatches, mismatch absolute position -- to accommodate for the relatively high disturbance of mismatches falling close to the PAM site, and mean pairwise distance between mismatches -- to account for the steric affect of closely neighboring mismatches in disrupting guide-DNA interaction.</p>
    </div>
  </div>
  <div class="row med-margin-top">
    <div id="single-hit" class="span6 offset2">
      <h3>Scores of Single Hits</h3>  
      <p>The actual algorithm used to score single offtargets is:</p>
<img  style="margin:10px; max-width:auto;" src="http://latex.codecogs.com/gif.latex?\prod_{e\in{\mathcal{M}}}\left(1-&space;W[e]\right)\times\frac{1}{\left(\frac{(19&space;-&space;\bar{d})}{19}\times4&space;&plus;&space;1\right)}\times\frac{1}{n^2_{mm}}" title="\prod_{e\in{\mathcal{M}}}\left(1- W[e]\right)\times\frac{1}{\left(\frac{(19 - \bar{d})}{19}\times4 + 1\right)}\times\frac{1}{n^2_{mm}}" />
      <p>Within the first term, <i>e</i> runs over the mismatch positions between guide and offtarget, with M:</p>
      <img style="margin:10px; max-width:auto;" src="http://latex.codecogs.com/gif.latex?M&space;=&space;[0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,\\&space;0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]" title="M = [0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,\\ 0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]" />
      <p>representing the experimentally-determined effect of mismatch position on targeting. (<a href="http://www.nature.com/nbt/journal/v31/n9/full/nbt.2647.html">Hsu et al, Nature Biotechnology 2013</a>)</p>
      <p>And terms two and three factoring in the effect of mean pairwise distance between mismatches (<i>d</i>) and a dampening penalty for highly mismatched targets. </p>
    </div>
  </div>

  <div class="row med-margin-top">
    <div id="aggregate-score" class="span6 offset2">
      <h3>Aggregate Scores by Guide</h3>  
      <p>Once individual hits have been scored, each guide is assigned a score:</p>
      <img  style="margin:10px; max-width:auto;"  src="http://latex.codecogs.com/gif.latex?S_{guide}&space;=&space;\frac{100}{100&space;&plus;&space;\sum_{i=1}^{n_{mm}}S_{hit}(h_i)}" title="S_{guide} = \frac{100}{100 + \sum_{i=1}^{n_{mm}}S_{hit}(h_i)}"/>
      <p>and colored according to a broad categorization of guide quality which, taken into account with the presence or absence of marked genes in high-scoring offtargets indicate the relative (un)favorability of using a particular guide for specific targeting in the query region.</p>
    </div>
  </div>
  <div class="row med-margin-top">
    <div id="selection" class="span6 offset2">
      <h3>Guide Selection</h3>  
      <p> Guides having an aggregate score of greater than 50% are colored green and should be considered candidate targeting sequences if no high-scoring offtargets fall in marked gene regions (indicated in the table to the right). Guides colored yellow should be considered backups for specific targeting in the case where no suitable green guides are clear of high-scoring, genic offtargets. Red guides have many likely offtarget interactions in the target genome and should be avoided.
    </div>
  </div>
</script>
