/** Spacer and hit list views */
var SpacerHV = Backbone.View.extend({
    template:$("#spacer-h-v-template").html(),
    className:"spacer-h-view spacer",
    tagName:"div",
    initialize:function(){
	this.viewsByCID={}
	this.binder = new Backbone.EventBinder()
	this.top_hits = new HitCollection()
	this.gene_hits = new HitCollection()
	
    },
    destroy:function(){
	_.each(this.viewsByCID,
	       function(e,i){
		   e.destroy();
	       });
	this.viewsByCID = {}
	this.$el.removeData().remove();
	this.binder.unbindAll();
	this.binder = null;
    },
    render:function(){
	params = this.model.toJSON() 
	params.top_hits = this.top_hits.models
	params.gene_hits = this.gene_hits.models

	params["rank"] =this.model.rank()

	this.$el.html(_.template(this.template,params))
	this.rendered = true;
	this.$el.attr("cid", this.model.cid)

	var self = this
	this.top_hits.on("add",function(m){
	    var hv = new HitV({model:m});
	    hv.render().$el.appendTo(this.$("table"))
	},this)

	
	_.each(this.model.top.models,function(e,i){
	    self.top_hits.add(e);
	});
	this.binder.bindTo(this.model.top,"add",
			   
			   function(e){
			       this.top_hits.add(e);
			   },this)
	return this
	
    },
});


/** view for spacers in a single list for the overall job view */
SpacerListV = Backbone.View.extend({
    template: $("#spacer-list-v-template").html(),
    className: "spacer-list-v spacer",
    tagName: "tr",
    initialize:function(){
	this.model.on("change:active",
		      function(m,v){
			  this.$el.toggleClass("active",v)
		      },this);
	this.$el.toggleClass("active",this.model.get("active"))
    },
    render:function(){
	mjson = this.model.toJSON()
	mjson["rank"] =this.model.rank()
	this.$el.html(_.template(this.template,mjson))
	this.$el.attr("cid", this.model.cid)
	this.$el.toggleClass("high-quality",this.model.get("score") >= high_quality_threshold?true: false);
	this.$el.toggleClass("medium-quality",(this.model.get("score") >= low_quality_threshold && this.model.get("score") < high_quality_threshold )?true: false);
	this.$el.toggleClass("low-quality",this.model.get("score") < low_quality_threshold?true: false);
	return this
    }
    
})

