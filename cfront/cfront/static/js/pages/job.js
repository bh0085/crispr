var current_job
function init_page(){
    current_job = new JobM(init_state.job)
    jpv = new JPView({model:current_job})
    jpv.render().$el.appendTo($("#job-container"))
}

JPView = Backbone.View.extend({
    className:"job-page-view",
    template:$("#job-page-view-template").html(),
    initialize:function(){
	this.jpsv = new JPStatusView({model:this.model})
	this.jppv = new JPPagesView({model:this.model})
    },
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	this.$(".status-view-container").html(this.jpsv.render().$el)
	this.$(".pages-view-container").html(this.jppv.render().$el)
	return this
    }
})

JPStatusView = Backbone.View.extend({
    className:"job-page-status-view",
    template:$("#job-page-status-view-template").html(),
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	return this
    }
    
    
})

JPPagesView = Backbone.View.extend({
    className:"job-page-pages-view",
    template:$("#job-page-pages-view-template").html(),
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	return this
    }

})
