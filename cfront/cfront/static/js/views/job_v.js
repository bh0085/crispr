/* job view that listens to joined relations of job to render spacers, hits as they come in */
JobV = Backbone.View.extend({
    template:$("#job-v-template").html(),
    className:"job-v",
    tagName:"div",
    initialize:function(){
	jv = this
	//right now, just assumes that the spacers are initialized on launch
	this.binder = new Backbone.EventBinder()
	this.svgv = new SimpleSpacerSVGV({model:this.model})
	this.nsvgv = new NickaseSVGV({model:this.model})
    },
    get_seq_html:function(){
	return $("<span>").text(this.model.get("sequence")).html();
    },

    render:function(){

	var self = this;
	params = this.model.toJSON()
	params.seq_html=this.get_seq_html();
	console.log( params.seq_html)
	var submitted_ms = this.model.get("submitted_ms")/1000;
	var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
	d.setUTCSeconds(submitted_ms);
	params.submitted = sprintf("%s",d)

	var completed_ms = this.model.get("completed_ms")/1000;
	if(completed_ms != 0){
	    var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
	    d.setUTCSeconds(completed_ms);
	    params.completed = sprintf("%s",d);
	} else { params.completed = "N/A" }

	this.$el.html(_.template(this.template,params))
	this.$(".files-area").empty().append(new FileListV({job:this.model}).render().$el);
	this.$(".jobsvg-v-container").append(this.svgv.render().$el)
	this.$(".nickase-v-container").append(this.nsvgv.render().$el)
	
        return this;
    },
})

GenericSV = Backbone.View.extend({
    template:$("#job-s-v-template").html(),
    className:"job-spacer-list-v",
    initialize:function(options){
	jsv = this;
	this.views_by_id = {}
	this.binder = new Backbone.EventBinder()

	this.binder.bindTo(this.model, "change:rank", 
			   function(m,v){this.spacers.remove(m);
					 this.spacers.add(m);}
			   , this);

	this.spacers = new SpacersDisplayC()
	this.spacers.on("add", this.add_one, this)
	this.spacers.on("remove", this.remove_one, this)
    },
    render:function(){
	params = this.model.toJSON()
	this.$el.html(_.template(this.template,params))
	_.each(this.model.get("spacers").models,
	       $.proxy(function(e){
		   this.spacers.add(e)
		   e.on("change:score",function(e){
		       this.spacers.remove(e);
		       this.spacers.add(e);
		   },this)
	       },this))
	return this
    },
    add_one:function(spacer){
	var view, $parent
	view = new SpacerListV({model:spacer})
	this.views_by_id[spacer.id] = view;
	idx = this.spacers.indexOf(spacer)
	prev = idx != 0 ? this.spacers.models[idx-1] : null
	if (prev){this.views_by_id[prev.id].$el.after(view.render().$el)}
	else {this.$(".views").prepend(view.render().$el)}
    },
    remove_one:function(spacer){
	var v = this.views_by_id[spacer.id]
	delete this.views_by_id[spacer.id]
	v.remove()
    }
})



JobSV = GenericSV.extend({
    add_one:function(spacer){
	var view, $parent
	view = new SpacerListV({model:spacer})
	this.views_by_id[spacer.id] = view;
	idx = this.spacers.indexOf(spacer)
	prev = idx != 0 ? this.spacers.models[idx-1] : null
	if (prev){this.views_by_id[prev.id].$el.after(view.render().$el)}
	else {this.$(".views").prepend(view.render().$el)}
    },

})

NickaseSV = GenericSV.extend({
    add_one:function(spacer){
	var view, $parent
	view = new SpacerNickaseListV({model:spacer})
	this.views_by_id[spacer.id] = view;
	idx = this.spacers.indexOf(spacer)
	prev = idx != 0 ? this.spacers.models[idx-1] : null
	if (prev){this.views_by_id[prev.id].$el.after(view.render().$el)}
	else {this.$(".views").prepend(view.render().$el)}
    },

})




function halfint(number){return Math.floor(number) + .5}
