/** Spacer and hit list views */
var SpacerHV = Backbone.View.extend({
    template:$("#spacer-h-v-template").html(),
    className:"spacer-h-view spacer",
    tagName:"div",
    initialize:function(){
	this.binder = new Backbone.EventBinder()
	this.top_hits = new HitCollection()
	this.gene_hits = new HitCollection()
    },
    destroy:function(){
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
	this.$el.attr("cid", this.model.cid)

	var self = this
	this.top_hits.on("add",function(m){
	    var hv = new HitV({model:m});
	    hv.render().$el.appendTo(this.$("table.top-hits"))
	    this.$(".n-top").text(this.top_hits.length)
	},this)

	_.each(this.model.top.models,function(e,i){
	    self.top_hits.add(e);
	});
	this.binder.bindTo(this.model.top,"add",		   
			   function(e){
			       this.top_hits.add(e);
			   },this)

	this.gene_hits.on("add",function(m){
	    var hv = new HitV({model:m});
	    hv.render().$el.appendTo(this.$("table.gene-hits"))
	    this.$(".n-genic").text(this.gene_hits.length)
	},this)

	_.each(this.model.genic.models,function(e,i){
	    self.gene_hits.add(e);
	});
	this.binder.bindTo(this.model.genic,"add",		   
			   function(e){
			       this.gene_hits.add(e);
			   },this)

	this.$("#exonic-only").on("click",function(){
	    if($(this).is(":checked")){
		self.$(".hits").addClass("gene").removeClass("top")
	    } else{
		self.$(".hits").addClass("top").removeClass("gene")
	    }
	})
	return this;
    },
});

var SpacerV = Backbone.View.extend({
    template:$("#spacer-v-template").html(),
    className:"spacer-v spacer",
    tagName:"div",
    initialize:function(){
	this.binder = new Backbone.EventBinder()
	this.top_hits = new HitCollection()
	this.gene_hits = new HitCollection()
    },
    destroy:function(){
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
	this.$el.attr("cid", this.model.cid)
	return this;
    }
})


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
	this.$el.toggleClass("low-quality",this.model.get("score") > 0 && this.model.get("score") < low_quality_threshold?true: false);
	this.$el.toggleClass("no-quality",this.model.get("score") == 0?true: false);

	return this
    }
    
})

