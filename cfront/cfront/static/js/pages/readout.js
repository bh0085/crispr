$(function(){
    init();
})

current_job = null;
function init(){
    host = location.host;
    pathname = location.pathname;
    jobid_string = location.pathname.split("/")[2];
   
    //if we have a subdomain prefix in the pathname, this will cause problems.
    jobid = parseInt(jobid_string);
    if (isNaN(jobid)){throw "bad jobid : "+jobid_string;}
    current_job = new JobM(init_state.job)
    current_job.poll()
    var rview = new ReadoutV({job:current_job})
    rview.render().$el.attr("id","readout").appendTo($("#readout-container"))
    rview.draw_job()

    current_job.get("spacers").models[0].set('active',true);

}




/* readout view initialized with a single job rendering pieces parts complete */
ReadoutV = Backbone.View.extend({
    className:"readout-view",
    template:$("#readout-section-template").html(),
    initialize:function(options){
	rv = this
	this.job = options.job;
	this.binder = new Backbone.EventBinder()
	this.binder.bindTo(this.job, "change:active_spacer", this.show_spacer,this)
    },
    render:function(){
	this.$el.html(_.template(this.template,{jobid:this.job.id}))
	return this
    },
    /** fired when spacers are market complete */
    draw_job:function(){
	this.jobview = new JobV({model:this.job})
	this.jobview.render().$el.appendTo(this.$(".job-header-area").empty())
	this.job_spacers_view = new JobSV({model:this.job})
	this.job_spacers_view.render().$el.appendTo(this.$(".spacers-container"))
    },
    show_spacer:function(job,spacer_m){
	if(this.spacer_h_view){
	    this.spacer_h_view.destroy()
	    this.spacer_view.destroy()
	}	
	this.spacer_h_view = new SpacerHV({model:spacer_m})
	this.spacer_h_view.render().$el.appendTo(this.$(".spacer-h-v-container"))

	this.spacer_view = new SpacerV({model:spacer_m})
	this.spacer_view.render().$el.appendTo(this.$(".spacer-v-container"))	
    },
})
