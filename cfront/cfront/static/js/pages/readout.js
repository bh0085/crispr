current_job = null;
function init_page(){
    //if we have a subdomain prefix in the pathname, this will cause problems.
    current_job = new JobM(init_state.job)
    current_job.poll()
    var rview = new ReadoutV({job:current_job})
    rview.render().$el.attr("id","readout").appendTo($("#readout-container"))
    rview.draw_job()
    if(current_job.status_frac() < 1){
	rview.draw_status();
    }
    current_job.get("spacers").models[0].set('active',true);

}

