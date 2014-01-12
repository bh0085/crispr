
DownloadV = Backbone.View.extend({

});





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
	this.job_spacers_view = new SpacerListView({model:this.job})
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

StatusV = Backbone.View.extend({
    template:$("#status-v-template").html(),
    initialize:function(){
	this.binder = new Backbone.EventBinder()
    },
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	var self = this
	_.each(this.model.get("spacers").models,function(s){
	    self.binder.bindTo(s, "change:score",self.update_status, self);
	});

	_.each(this.model.get("files").models,function(f){
	    self.binder.bindTo(f, "change:ready",self.update_status, self);
	});

	self.update_status()
	return this
    },
    
    update_status:function(){

	message = this.model.status_message()
	frac = this.model.status_frac()

	this.$(".status .text").empty().append($("<span>").text(message))
	this.$(".status").toggleClass("done",frac == 1) 
	this.$(".status .progress .bar").css("width"," "+ (frac * 100)+"%");
    },

})
