<script type="unknown" id="batch-v-template">
  <h1 class="header">
    {{original_filename}}
  </h1>
  <div>
    <h3>Info</h3>
    <div>{{jobs.length}} jobs querying the genome {{genome_name}}.</div>
    <div>Submitted by {{email}} at {{submitted_ms}}, completed at 
      <span class="completed_ms">{{completed_ms != null ? completed_ms : "(not yet completed)"}}
      </span>
    </div>
  </div>
  <h3 class="header">Jobs</h3>
  <div class="job-links">
  </div>
</script>

<script type="unknown" id="job-link-template">
  <a href={{link}}>#<span class="id">{{id}}</span> <span class="name">{{name}}</span> (<span class="n_completed_spacers {{n_completed_spacers==0?'unstarted':'started'}}">{{n_completed_spacers}}</span>/<span class="n_spacers">{{n_spacers}}</span> spacers)</a>
</script>
