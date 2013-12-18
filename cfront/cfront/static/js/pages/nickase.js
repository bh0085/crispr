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
    $(document).on("mouseover", ".spacer", {}, spacer_select)

}


/* html view for the nickase model */
NickaseV = Backbone.View.extend({
    className:"nickase-view",
    template:$("#nickase-v-template").html(),
    initialize:function(){
	this.job = current_job;
	//initializes a new graphics (SVG) view with this job
	this.ngraphics_view = new NickaseGraphicalV(this.job)
	this.job_spacers_view = new NickaseSV({model:this.job})
	this.job.on("change:active_spacer",
		    this.ngraphics_view.tryrender_current_spacer,
		    this.ngraphics_view)


    },
    render:function(){
	params = current_job.toJSON()
	this.$el.html(_.template(this.template,params))
	this.$(".graphics").append(this.ngraphics_view.$el)
	this.job_spacers_view.render().$el.appendTo(this.$(".spacer-list"))
	return this
    }	
})

/* SVG renderer for the nickase model */
NickaseGraphicalV = Backbone.View.extend({
    convert_rel_base_to_x:function(base){
	var j = this.job
	frac = (base ) / j.get("sequence").length
	return frac * this.cwidth;
    },
    convert_offset_to_y:function(ofs){
	return ( this.cheight /2 ) +  10 * ofs
    },   
    initialize:function(job){
	this.job = job
	this.cwidth = 600
	this.cheight = 400
	gview = this;
    },

    tryrender_current_spacer:function(){
	spacer = this.job.get("active_spacer")
	if(spacer.get("fetched_regions")){
	    this.render()
	} else {
	    spacer.fetch_regions()
	}
    },

    render:function(){
	this.spans = []
	var cmodel = this.job.get('active_spacer')

	
	if(cmodel.get("strand") == 1){
	    consorts = _.filter(this.job.get("spacers").models,
			       function(e){
				   return e.get("strand") == -1
			       })
	} else{
	    consorts = _.filter(this.job.get("spacers").models,
				function(e){
				    return e.get("strand") == 1
				})
	}


	for(var i = 0 ; i < consorts.length ; i++){
	    this.spans.push( {spacer:cmodel,
			      consort:consorts[i],
			      parent:this,
			      offset:(i)  * ((cmodel.get("strand")==1)?1:-1),
			      score:N.spacer_score_consort(cmodel,consorts[i].get("sequence")) 
			     })
	    
	}
	
	this.views_list = _.map(this.spans,function(e){
	    return new SpanV({model:e}) 
	})
	
	this.svg = this.$el.svg({}).svg("get");
	this.svg.clear()
	svgel = this.svg

	//assigns an SVG renderer to this model so that it can be accessed by
	//child spans
	$(this.svg._svg).attr("height",this.cheight + "px")
	$(this.svg._svg).attr("width",this.cwidth + "px")

	//renders subview only after this model has been assigned an SVG object
	for (var i = 0 ; i < this.views_list.length; i++){
	    this.views_list[i].render()
	}
	return this
    },
})

/* span view rendered into a nickase graphical view */
SpanV = Backbone.View.extend({
    initialize:function(opts){
	this.model = opts.model
    },
    render:function(svg){
	var s = this.model
	var svg = s.parent.svg
	if (svg == null){ throw "no svg yet exists..."}
	var y = s.parent.convert_offset_to_y(s.offset)
	var x0 = s.parent.convert_rel_base_to_x(s.spacer.get("start"))
	var x1 = s.parent.convert_rel_base_to_x(s.consort.get("start"))

	if(this.group == null){
	    //first time rendered, create an element
	    this.group = svg.group()
	    var p = svg.createPath()
	    p.moveTo(x0,y)
	    p.lineTo(x1,y)
	    var path = svg.path(this.group, p)
	    svg.configure(path,{"strokeWidth":(20- s.score),
				"stroke":"black"})
	}

    }
})
