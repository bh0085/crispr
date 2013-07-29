

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
	data.gene = white_pad(12,data.gene,true)
	
	data.mm_string = white_pad(22,sprintf("%sMMs [%s]", data.n_mismatches,data.mismatches ),true)
	this.$el.html(_.template(this.template, data))
	return this
    }
});



function white_pad(n,input,both_sides){
    d = Math.max(0,n - input.length)
    if (both_sides){
	d1 = Math.floor(d/2)
	d2 = Math.ceil(d/2)
	output = Array(d1).join("&nbsp;")+input+Array(d2).join("&nbsp;")
    } else {
        output = input + Array(d).join("&nbsp;")
    }
    return output
}
