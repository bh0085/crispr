var FileV= Backbone.View.extend({
    className:"file-v",
    tagName:"span",
    template:$("#file-v-template").html(),
    initialize:function(){
	this.binder = new Backbone.EventBinder();
	this.binder.bindTo(this.model,"change:ready",this.render,this);
    },
    render:function(){
	fv = this
	var params = this.model.toJSON()
	this.$el.html(_.template(this.template, params));
	this.$el.toggleClass("ready",this.model.get("ready") ? true: false)
	this.binder.bindTo(this.model,"change:ready",function(){
	    this.$el.toggleClass("ready",this.model.get("ready") ? true: false)
	},this)
	return this
    },
    destroy:function(){
	this.binder.unbindAll()
	this.$el.remove()
    }
})

var FileListV = Backbone.View.extend({
    className:"file-list-v showing-less",
    tagName:"div",
    template:$("#file-list-v-template").html(),
    initialize:function(options){
	flv = this
	this.job = options.job
	if (!this.job){throw "no job"}
    },
    render:function(){
	var params = {job:this.job}
	var self = this
	this.$el.html(_.template(this.template, params))
	_.each(this.job.get("files").models,function(e){
	    self.$('.files').append(new FileV({model:e}).render().$el);
	});

	if(this.job.get("query_type") != "unique_genomic"){
	    this.$el.append($("<a>",{"class":"annotation med-left-margin less show-more"}).text("... show warning"))
	    this.$el.append($("<a>",{"class":"annotation med-left-margin more show-less"}).text("... hide warning"))
	}
	return this
    },
})

