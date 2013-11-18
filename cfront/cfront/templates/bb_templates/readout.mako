<script id="readout-section-template" type="unknown">
  <div class="status-header-area"></div>
  <div class="job-header-area"></div>
</script>


<script type="unknow" id="status-v-template">
  <!-- status display area -->
  <div class="status">
    <div style="white-space:nowrap;">
      <control><input id="email-complete" class="inline v-middle" {{email_complete?"checked":""}} type="checkbox"></input><label class="med-left-margin unselectable inline v-middle" for="email-complete">email ({{email}}) on completion</label></control>
    </div>
    <div class="progress progress-striped active">
      <div class="bar" style="width: 0%;"></div>
    </div>
    <div style="white-space:nowrap;">
      <span class="text">locating guides... should take a couple of seconds</span>
    </div>
  </div>
</script>
