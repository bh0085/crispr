$(function(){
    init();
})

current_job = null;
function init(){

    params ={"name":"Readout",
	     "description":"Best possible guide sequences."}
    $("#readout").html(
	_.template($("#scrolly-section-template").html(),
		   params))
    
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
	rv = this
	this.job = options.job;
	this.job.on("all_spacers_ready",this.draw_job, this);
	this.job.on("change:computed_n_hits", this.draw_hits, this);
    },
    render:function(){
	
	this.$el.html(_.template(this.template,{jobid:this.job.id}))
	return this
    },
    /** fired when spacers are market complete */
    draw_job:function(model,val){
	this.$(".status").empty().append($("<p>").text("aligning spacers, ("+_.filter(this.job.get("spacers").models,function(e){return e.get("computed_hits")}).length + " of " + this.job.get("spacers").length+")"))
	if (val == false){throw "spacers should never be changed to false"}
	this.jobview = new JobV({model:this.job})
	this.jobview.$el.appendTo(this.$el)
	this.jobview.render()
	this.jobview.compute_collisions()
	this.jobview.draw_spacers()
	this.job_spacers_view = new JobSV({model:this.job})
	this.job_spacers_view.render().$el.appendTo(this.$el)
	this.draw_hits()
    },
    draw_hits:function(model){

	var done_count = _.filter(this.job.get("spacers").models,function(e){return e.get("computed_hits")}).length
	var total_count = this.job.get("spacers").length
	if(done_count != total_count){
	    this.$(".status").empty().append($("<p>").text("aligning spacers, ("+ done_count + " of " + total_count +")"))
	}  else {
	    this.$(".status").empty().append($("<p>").text("done aligning spacers"))
	}

	spacers = this.job.get("spacers").models
	for (var i = 0 ; i < spacers.length ; i++){
	    console.log("SPACE",i, spacers[i])
	    //spacers[i].on("change:score",this.jobview.update_query_spacer,this.jobview)
	    if(spacers[i].get("score") != null){
		this.jobview.update_query_spacer(spacers[i])
	    }
	}
    }
})
