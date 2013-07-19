

var HitCollection = Backbone.Collection.extend({
    model:HitM,
    comparator:function(m){
	return -1 * m.get("score");
    }
})

var HitV = Backbone.View.extend({
    tagName:"tr",
    className:"hit-v",
    template:$("#hit-v-template").html(),
    destroy:function(){
	this.$el.removeData().remove();
    }, 
    render:function(){
	data = this.model.toJSON()
	data.gene = data.gene?data.gene:"";
	this.$el.html(_.template(this.template, data))
	return this
    }
});
