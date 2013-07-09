/* readout view initialized with a single job rendering pieces parts complete */
ReadoutV = Backbone.View.extend({
    template:$("#readout-section-template").html(),
    initialize:function(options){
	rv = this
	this.job = options.job;
	this.job.on("all_spacers_ready",this.draw_job, this);
	this.job.on("some_hits_ready", this.draw_hits, this);
	//job.on("change:computed_hits",this.draw_hits, this)
    },
    render:function(){
	
	this.$el.html(_.template(this.template,{jobid:this.job.id}))
	return this
    },
    /** fired when spacers are market complete */
    draw_job:function(model,val){
	if (val == false){throw "spacers should never be changed to false"}
	this.jobview = new JobV({model:this.job})
	this.jobview.$el.appendTo(this.$el)
	this.jobview.render()
	this.jobview.compute_collisions()
	this.jobview.draw_spacers()
	this.job_spacers_view = new JobSV({model:this.job})
	this.job_spacers_view.render().$el.appendTo(this.$el)
    },
    draw_hits:function(model){
	spacers = this.job.get("spacers").models
	for (var i = 0 ; i < spacers.length ; i++){
	    if(spacers[i].get("computed_hits")) this.jobview.update_query_spacer(spacers[i])
	}
    }
})
