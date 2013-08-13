current_job = null;
function init_page(){
    //if we have a subdomain prefix in the pathname, this will cause problems.
    current_job = new JobM(init_state.job)
    if(!current_job.get("start")){
	$("#nickase-container").text("job is not mapped to the genome")
    }
    current_job.poll()
    var rview = new NickaseV({job:current_job})
    rview.render().$el.attr("id","nickase").appendTo($("#nickase-container"))
}


/* html view for the nickase model */
NickaseV = Backbone.View.extend({
    className:"nickase-view",
    template:$("#nickase-v-template").html(),
    initialize:function(){
	this.job = current_job;
	//initializes a new graphics (SVG) view with this job
	this.ngraphics = new NickaseGraphicalV({
	    model: new NickaseGraphicalM({job:this.job})
	})
    },
    render:function(){
	params = current_job.toJSON()
	this.$el.html(_.template(this.template,params))
	this.$(".graphics").append(this.ngraphics_view.render())	      
	return this
    }	
})

/* graphical model for the nickase SVG, constructs and stores spans */
NickaseGraphicalM = Backbone.RelationalModel.extend({
    relations:[
	{
	    key:"spans",
	    type:Backbone.HasMany,
	    relatedModel:"SpanVM",
	    reverseRelations:{
		key:"parent",
		type:Backbone.HasOne
	    }
	}
    ],
    initialize:function(){
	this.set("cwidth", 600)
	this.set("cheight", 400)
	
	//initialize and create span models
	tops = _.filter(this.get("job").get("spacers").models,
			function(e){
			    return e.get("strand") == 1
			})
	bottoms = _.filter(this.get("job").get("spacers").models,
			  function(e){
			      return e.get("strand") == -1
			  })
	for(var i = 0 ; i < tops.length ; i++){
	    for (var j = 0 ; j < bottoms.length ; j++){
		var s = new SpanVM({top:tops[i],
				    bottom:bottoms[j],
				    parent:this,
				    offset:i + j
				   })
	    }
	}
    },
    convert_rel_base_to_x:function(base){
	var parent = this.get("parent")
	var j = parent.job
	frac = (base  - j.get("start") ) / j.get("sequence").length
	return frac = this.cwidth;
    },
    convert_offset_to_y:function(ofs){
	return 20 * ofs
    }
})

/* SVG renderer for the nickase model */
NickaseGraphicalV = Backbone.View.extend({
    initialize:function(){
	this.views_list = _.map(this.model.get("spans").models,function(e){
	    return new SpanV({model:e}) 
	})
    },
    render:function(){
	this.svg = this.$el.svg({}).svg("get");
	
	//assigns an SVG renderer to this model so that it can be accessed by
	//child spans
	this.model.set("svg", this.svg)
	this.svg._svg.attr("height",this.model.get("cheight") + "px")
	this.svg._svg.attr("width",this.model.get("cwidth") + "px")

	//renders subview only after this model has been assigned an SVG object
	for (var i = 0 ; i < this.views_list.length; i++){
	    this.views_list[i].render()
	}
	return this
    },
})

/* model storing varying properties of a span view */
SpanVM = Backbone.RelationalModel.extend({
    defaults:{
	top:null,
	bottom:null,
	job:null,
    },
    initialize:function(){
	if(!this.get("top") || !this.get("bottom") || !this.get("offset")){
	    throw "inadequately initialized span."
	}
	this.get("top").on("change:score", this.computeScore, this)
	this.get("bottom").on("change:score", this.computeScore, this)
	this.computeScore()
    },
    computeScore:function(){
	if(this.get("bottom").get("score") == null || this.get("top").get("score") == null){
	    this.set("score",0)
	} else{
	    this.set("score", this.get("bottom").get("score") *
		     this.get("top").get("score"))
	} 
    }
})

/* span view rendered into a nickase graphical view */
SpanV = Backbone.View.extend({
    initialize:function(opts){
	if(this.model == null){ throw "null model for a span view" }
	this.model.on("change:score",this.render())
	this.model.on("change:offset",this.render())
    },
    render:function(svg){
	var s = this.model
	var svg = s.get("parent").get("svg")
	if (svg == null){ throw "no svg yet exists..."}
	var y = s.get("parent").convert_offset_to_y(s.get("offset"))
	var x0 = s.get("parent").convert_rel_base_to_x(s.get("bottom").get("start"))
	var x1 = s.get("parent").convert_rel_base_to_x(s.get("top").get("start"))

	if(this.group == null){
	    //first time rendered, create an element
	    this.group = svg.group()
	    
	    var p = svg.createPath()
	    p.moveTo(x0,y)
	    p.lineTo(x1,y)
	    var path = svg.path(this.group, p)
	    svg.configure(path,{"strokeWidth":10,
				"stroke":"black"})
	    
	}

    }
})
