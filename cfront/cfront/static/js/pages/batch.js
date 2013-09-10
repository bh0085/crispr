current_batch = null;

function init_page(){
    //if we have a subdomain prefix in the pathname, this will cause problems.
    current_batch = new BatchM(init_state.batch)
    var bview = new BatchV({model:current_batch})
    bview.render().$el.attr("id","batch").appendTo($("#batch-container"))
}

 
BatchM = Backbone.RelationalModel.extend({
    defaults:{
	active_job:null
    },
    relations:[{
	key:"jobs",
	type:Backbone.HasMany,
	relatedModel:"JobM",
	inclueInJSON:"id",
	reverseRelation:{
	    key:"batch",
	    keySource:"batchid",
	    includeInJSON:"id",
	    type:Backbone.HasOne
	}
    }],
    url:function(){
	return routes.route_path("batch_rest", {"batch_key":this.get("key")})
    },
    //waiting for hits, polls. true when done.
    poll:function(){
	var self =this
	self.fetch(
	    {success:function(){
		self.set("poll_timeout",self.get("poll_timeout") + 100);
		window.setTimeout($.proxy(self.poll,self),
				  self.get("poll_timeout"));
	    }})
	
    },

    activateOne:function(j,val){
	if( val){
	    _.each(this.get("jobs").models,function(j2, i2){
		if (j2.id != j.id)
		{j2.set("active",false)}
	    });
	    this.set("active_spacer",j);
	}
    },
    initialize:function(){
	var self = this
	this.binder = new Backbone.EventBinder()
	_.each(self.get("jobs").models, function(j,i){
	    j.on("change:active",self.activateOne,self);
	});
    },

})
BatchV = Backbone.View.extend({
    template:$("#batch-v-template").html(),
    className:"batch-v",
    tagName:"div",
    render:function(){
	this.$el.html(_.template(this.template, this.model.toJSON()))
	var self = this;
	
	_.each(self.model.get("jobs").models,
	       function(e,i){
		   jlv = new JobLinkView({model:e})
		   jlv.render().$el.appendTo(self.$(".job-links"))
	       });
	
	return this
    }
})

JobLinkView = Backbone.View.extend({
    template:$("#job-link-template").html(),
    className:"job-link-v",
    tagName:"div",
    render:function(){
	data = this.model.toJSON()
	data["link"] = routes.route_path("readout",{"job_key":this.model.get("key")})
	this.$el.html(_.template(this.template,data))		  
	return this
    }
})
