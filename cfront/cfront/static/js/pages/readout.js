$(function(){
    init();
})

current_job = null;
function init(){


    $("#readout").html(
	_.template($("#scrolly-section-template").html(),{}))
    
    host = location.host;
    pathname = location.pathname;
    jobid_string = location.pathname.split("/")[2];
   
    //if we have a subdomain prefix in the pathname, this will cause problems.
    jobid = parseInt(jobid_string);
    if (isNaN(jobid)){throw "bad jobid : "+jobid_string;}
    current_job = new JobM({id:jobid})
    current_job.fetch({success:$.proxy(current_job.fetched,current_job)})
}




/* readout view initialized with a single job rendering pieces parts complete */
ReadoutV = Backbone.View.extend({
    template:$("#readout-section-template").html(),
    initialize:function(options){
	$("#readout .header.row").html(
	    _.template($("#job-h-template").html(),options.job.toJSON()))
	rv = this
	this.job = options.job;
	this.job.on("all_spacers_ready",this.draw_job, this);
	this.job.on("change:computed_n_hits", this.draw_hits, this);
    },
    render:function(){
	this.$el.html(_.template(this.template,{jobid:this.job.id}))
	return this
    },
    update_status:function(){
	
	var done_count = _.filter(this.job.get("spacers").models,function(e){return e.get("computed_hits")}).length
	var total_count = this.job.get("spacers").length
	
	if(done_count < total_count){
	    console.log(this.$(".status .text"))
	    this.$(".status .text").empty().append($("<p>").text("aligning spacers, ("+ done_count + " of " + total_count +")"))
	}  else {
	    this.$(".status").addClass("done");
	    this.$(".status .text").empty().append($("<p>").text("done aligning spacers"))
	}
	this.$(".status .progress .bar").css("width"," "+ (done_count/total_count * 100)+"%")

    },
    /** fired when spacers are market complete */
    draw_job:function(model,val){
	if (val == false){throw "spacers should never be changed to false"}
	this.update_status()
	this.jobview = new JobV({model:this.job})
	this.jobview.$el.appendTo(this.$(".job-svg-view"))
	this.jobview.render()
	this.jobview.compute_collisions()
	this.jobview.draw_spacers()
	this.job_spacers_view = new JobSV({model:this.job})
	this.job_spacers_view.render().$el.appendTo(this.$(".spacers-container"))
	this.draw_hits()
    },
    draw_hits:function(model){
	this.update_status()
	spacers = this.job.get("spacers").models
	for (var i = 0 ; i < spacers.length ; i++){
	    //spacers[i].on("change:score",this.jobview.update_query_spacer,this.jobview)
	    if(spacers[i].get("score") != null){
		this.jobview.update_query_spacer(spacers[i])
	    }
	}
	this.show_spacer(current_job.get("spacers").models[0])

    },
    show_spacer:function(spacer_m){
	if(this.spacer_h_view){
	    this.spacer_h_view.destroy()
	}
	
	this.spacer_h_view = new SpacerHV({model:spacer_m})
	this.spacer_h_view.render().$el.appendTo(this.$(".hits-container"))
	this.spacer_h_view.$el.tablesorter(); 
	
    }
})

