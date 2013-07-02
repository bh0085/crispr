
/**backbone models for relations used in "find"*/
var OffTargetM = Backbone.Model.extend({
    loci_id:null,
    start:null,
    chr:null,
    strand:null,
    sequence:null,
    exon:null
});
var OffTargetV = Backbone.View.extend({
    template:$("#offtarget_v_template").html(),
    tagName:"li",
    className:"offtarget_v",
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	return this
    }
});


var SpacerM = Backbone.Model.extend({
    status:null,
    job_id:null,
    find_id:null,
    offtargets :null,
    sequence:null,
    initialize:function(){
	this.set("offtargets",new OffTargetsG());
    },
    retrieveHitsJSON:function(hits_array){
	_.each(hits_array,function(e,i){
	    /** needs to add in the loci, starts etc once returned */
	    var m = new OffTargetM({
		loci_id:e.id,
		start:1,
		chr:1,
		strand:1,
		sequence:e.sequence,
		similarity:e.similarity,
	    });
	    this.get("offtargets").add(m)
	},this)
    }
});
var SpacerOffTargetsV = Backbone.View.extend({
    template:$("#spacer_offtargets_v_template").html(),
    className:"spacer_offtargets_v",
    tagName:"li",
    initialize:function(){
	this.views = [];
    },
    render:function(){
	last_v = this;
	this.$el.html(_.template(this.template,this.model.toJSON()))
	this.binder = new Backbone.EventBinder()
	this.binder.bindTo(this.model.get("offtargets"), "add", this.addOne, this);
	return this
    },
    cleanupRelations:function(){
	_.each(this.views,function(e,i){
	    e.destroy();
	});
	delete this.views;
	this.binder.unbindAll()
	delete this.binder;
    },
    addOne:function(m,collection){
	var v = new OffTargetV({model:m})
	v.render().$el.appendTo(this.$el)
	this.views.push(v);
    }
});

var OffTargetsG = Backbone.Collection.extend(
    {model:OffTargetM});

