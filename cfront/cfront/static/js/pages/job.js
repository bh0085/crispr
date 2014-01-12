var current_job
function init_page(){
    current_job = new JobM(init_state.job)
    jpv = new JPView({model:current_job})
    jpv.render().$el.appendTo($("#job-container"))
    current_job.poll()
    
    current_job.on("change:status_hash",function(){
	$("body").toggleClass("done",current_job.status_frac()==1)
    })
    $("body").toggleClass("done",current_job.status_frac()==1)
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

	$(".breadcrumb").append($("<li>",{"class":"active"})
				.text('Job "'+this.model.get("name")+'"'))		       
	return this
    }
})

JPStatusView = Backbone.View.extend({
    className:"job-page-status-view",
    template:$("#job-page-status-view-template").html(),
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	this.model.on("change:status_hash",this.update_status,this)
	this.update_status()
	return this
    },
   update_status:function(){
	message = this.model.status_message()
	frac = this.model.status_frac()
	this.$(".status-text").empty().append($("<span>").text(message))
       if(frac == 1){
	   this.$(".status").toggleClass("done",true)
	   this.$(".bar").toggleClass("bar-success",true)
	   this.$(".progress").toggleClass("active",false)
	   this.$(".email").hide()
       }
	this.$(".status .progress .bar").css("width"," "+ (frac * 100)+"%");
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
