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
	//this renders the main job view on the "readout" page 
	// -- equivalent tot he nickaseV in nickase_v.js
	var self = this;
	params = this.model.toJSON()
	params.seq_html=this.get_seq_html();
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


SpacersDisplayC = Backbone.Collection.extend({
    model:SpacerM,
    comparator:function(m){
	return -1 * m.get("score")
    }
})

NicksDisplayC = Backbone.Collection.extend({
    model:NickM,
    comparator:function(m){
	return -1 * m.get("score")
    }
})


GenericListView = Backbone.View.extend({
    initialize:function(options){
	jsv = this;
	this.views_by_id = {}
	this.binder = new Backbone.EventBinder()

	this.binder.bindTo(this.model, "change:rank", 
			   function(m,v){this.items.remove(m);
					 this.items.add(m);}
			   , this);

	this.items = new this.collection()
	this.items.on("add", this.add_one, this)
	this.items.on("remove", this.remove_one, this)
	//throw "WE SWAPPED OUT COLLECTIONS, SPACERS, ITEMS HERE, THIS IS FUCKED"
    },
    render:function(){
	params = this.model.toJSON()
	this.$el.html(_.template(this.template,params))
	_.each(this.model.get(this.collection_name).models,
	       $.proxy(function(e){
		   this.items.add(e)
		   e.on("change:score",function(e){
		       this.items.remove(e);
		       this.items.add(e);
		   },this)
	       },this))
	return this
    },
    add_one:function(item){
	var view, $parent
	view = new this.view_class({model:item})
	this.views_by_id[item.id] = view;
	idx = this.items.indexOf(item)
	prev = idx != 0 ? this.items.models[idx-1] : null
	if (prev){
	    this.views_by_id[prev.id].$el.after(view.render().$el)}
	else {this.$(".views").prepend(view.render().$el)}
    },
    remove_one:function(item){
	var v = this.views_by_id[item.id]
	delete this.views_by_id[item.id]
	v.remove()
    }
})


GenericItemView = Backbone.View.extend({
    tagName: "tr",

    initialize:function(){
	this.model.on("change:active",
		      function(m,v){
			  this.$el.toggleClass("active",v)
		      },this);
	this.$el.toggleClass("active",this.model.get("active") == true)
	this.model.on("change:rank",this.render,this);
	this.model.on("change:score",this.render, this);
    },
    render:function(){
	mjson = this.model.toJSON()
	this.$el.html(_.template(this.template,mjson))
	this.$el.attr("cid", this.model.cid)
	this.$el.removeClass("medium-quality high-quality low-quality no-quality")
	this.$el.addClass(this.model.get("quality")+"-quality")
	return this
    },
})


SpacerItemView = GenericItemView.extend({
    template: $("#spacer-list-v-template").html(),
    className: "spacer-list-v spacer list-row",

})

NickaseItemView = GenericItemView.extend({
    template:$("#nickase-list-v-template").html(),
    className: "nickase-list-v nickase list-row",   

    initialize:function(){
	this.model.on("change:active",
		      function(m,v){
			  this.$el.toggleClass("active",v)
		      },this);
	this.$el.toggleClass("active",this.model.get("active") == true)
	this.model.on("change:included",
		      function(m,v){
			  this.$el.toggleClass("included",v==null?false:true)
		      },this);
	this.$el.toggleClass("included",this.model.get("included")==null?false:true)

	this.model.on("change:rank",this.render,this);
	this.model.on("change:score",this.render, this);


	var nick = this.model
	this.$el.on("click",function(){
	    current_job.set("hover_locked", !current_job.get("hover_locked"))
	})

	this.$el.on("mouseenter",function(){
	    if(!current_job.get("hover_locked")){
		current_job.activateNick(nick, true)
	    }
	    $(".hover-helper").text("(click to select "+nick.get("range_name")+")")
	});

	this.$el.on("mouseleave",function(){
	    $(".hover-helper").text("")
	});


    },
})




/** view for spacers in a single list for the overall job view */
SpacerListView = GenericListView.extend({

    template:$("#job-spacer-list-v-template").html(),
    className:"job-list-v spacers-list",
    collection:SpacersDisplayC,
    collection_name:"spacers",
    view_class:SpacerItemView,
})

/** view for spacers in a list that will be selected from to get nickase views */
NickaseListView = GenericListView.extend({
    template:$("#job-nicks-list-v-template").html(),
    className:"job-list-v nicks-list",
    collection:NicksDisplayC,
    collection_name:"nicks",
    view_class:NickaseItemView
})





function halfint(number){return Math.floor(number) + .5}
