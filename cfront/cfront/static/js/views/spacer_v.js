/** Spacer and hit list views */
var SpacerHV = Backbone.View.extend({
    template:$("#spacer-h-v-template").html(),
    className:"spacer-h-view tablesorter",
    tagName:"table",
    initialize:function(){
	this.viewsByCID={}
	this.binder = new Backbone.EventBinder()
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
	data ={}
	content = _.template(this.template,data)
	this.$el.html(content)
	_.each( this.model.get("hits").models,  $.proxy(this.addOne, this) )
	this.binder.bindTo(this.model,"add:hits",this.addOne,this);
	this.rendered = true;
	return this
	
    },
    addOne:function(h){
	var hv = new HitV({model:h})
	this.viewsByCID[hv.cid] = hv
	hv.render().$el.appendTo(this.$("tbody"))
	if(this.rendered){this.$el.tablesorter()}
    }
});

var HitV = Backbone.View.extend({
    tagName:"tr",
    className:"hit-v",
    template:$("#hit-v-template").html(),
    destroy:function(){
	this.$el.removeData().remove();
    }, 
    render:function(){
	data = this.model.toJSON()
	this.$el.html(_.template(this.template, data))
	return this
    }
});
