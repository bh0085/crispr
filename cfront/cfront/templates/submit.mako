<div id="submit" class="scrolly-section submit-container">
</div>

<script id="submit-section-template" type="unknown">
  <form class="form-horizontal">
    <div class="control-group">
      <span class="control-label">search name</span>
      <div class="controls">
	<input id="search-name" type="text" placeholder="name">
      </div>
    </div>
    <div class="control-group">
      <span class="control-label">email address</span>
      <div class="controls">
	<input id="email-address" type="text" placeholder="email">
      </div>
    </div>
    <div class="control-group">
      <span class="control-label">sequence type</span>
      <div class="controls">
	<label class="radio">
	  <input type="radio" name="optionsRadios" id="optionsRadios1" value="option1" checked>
	  genomic region (23-1000 nt)
	</label>
	<label class="radio">
	  <input type="radio" name="optionsRadios" id="optionsRadios2" value="option2">
	  other region (23-1000 nt)
	</label>
	<label class="radio">
	  <input type="radio" name="optionsRadios" id="optionsRadios3" value="option3">
	  single spacer sequence (23 nt)
	</label>
      </div> 
    </div>
    <div class="control-group">
      <span class="control-label">sequence</span>
      <div class="controls">
	<textarea id="sequence_submission_area" rows=10>AGAGAGGGAGATGTGATCGCTAGCATGCATCGACTAGCAT</textarea>
      </div>
    </div>
    <div class="control-group">
      <div class="controls"><h4><a class="next">Submit</a></h4></div>
  </form>
</script>
