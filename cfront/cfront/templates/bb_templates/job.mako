<script type="unknown" id="job-page-view-template">
  <div class="status-view-container"></div>
  <div class="pages-view-container"></div>
</script>
<script type="unknown" id="job-page-status-view-template">
  <div class="">
    <h2>Status</h2>
    <div class="status-text full-width">about ?? minutes left<span class="right"><control class="email"><input id="email-complete" class="inline v-middle" {{email_complete?"checked":""}} type="checkbox"></input><label class="unselectable inline v-middle med-left-margin" for="email-complete">Email when done</label></control></span></div>
  </div>


  
  <!-- status display area -->
  <div class="status">
    <div class="progress progress-striped active">
      <div class="progress-bar bar" style="width: 0%;"></div>
    </div>
  </div>

</script>
<script type="unknown" id="job-page-pages-view-template">
  <div class="page-header">
    <h2>Results</h2>
    <div class="full-width">view results online<span class="right">or see <a href="{{downloads_page_url}}">available downloads</a></span></div>
  </div>
  <div class="cards">
    <div class="card guides">
      <div class="background"></div>
      <a class="covering-link" href="{{readout_page_url}}"></a>
      <div class="header"><h4>Guides and offtargets</h4></div>
      <div class="footer"><a href="{{export_gb_guides_url}}" target="_blank">download as genbank</a></div>
    </div>
    <div class="card nickase">
      <div class="background"></div>
      <a class="covering-link" href="{{nickase_page_url}}"></a>
      <div class="header"><h4>Nickase analysis</h4></div>
      <div class="footer"><a href="{{export_gb_nicks_url}}" target="_blank">download as genbank</a></div>
    </div>
  </div>
</script>
