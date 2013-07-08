/* readout view initialized with a single job rendering pieces parts complete */
ReadoutV = Backbone.View.extend({
    template:$("#readout-section-template").html(),
    initialize:function(options){
	this.job = options.job;
	this.job.on("change:computed_spacers",this.draw_job, this);
	//job.on("change:computed_hits",this.draw_hits, this)
    },
    render:function(){
	this.$el.html(_.template(this.template,{}))
	return this
    },
    computed_hits:function(val){
	if (val == false){throw "hits should never be changed to false"}
	throw "not yet implemented"
    },
    /** fired when spacers are market complete */
    draw_job:function(val){
	if (val == false){throw "spacers should never be changed to false"}
	this.jobview = new JobV({model:this.job})
	this.jobview.render().$el.appendTo(this.$el)
    }
    
})

/* job view that listens to joined relations of job to render spacers, hits as they come in */
JobV = Backbone.View.extend({
    template:$("#job_v_template").html(),
    className:"job_v",
    tagName:"div",
    initialize:function(){
	//right now, just assumes that the spacers are initialized on launch
	
	if(!this.model.get('computed_spacers')){
	    throw "for now we assume that spacers are already computed (hits need not be)"
	    //this.model.on("add:spacers", this.draw_spacer, this)
	}
	_.each(this.get("spacers"), function(e){
	    e.on("change:computed_hits", function(){
		console.log("computed hits for spacer, " + e.id)
	    },e);
	}, this)
	
    },
    render:function(){
        //removes current svg content
        this.$(".job-v-svg-container").remove();
        this.$el.append(
	    $("<div>",{"class":"job-v-svg-container"})
                .html($("#job-v-svg-container-template").html()));
        var ss = this.$(".selection-svg");  

	//svg(parent, x, y, width, height, vx, vy, vwidth, vheight;
        this.svg = ss.svg(null, 0, 0, 600,600,600,600).svg('get');
	$(this.svg._svg).attr("height", "100%");
	$(this.svg._svg).attr("width", "100%");
        return this;
    },
    
    compute_collisions:function(){
	var ranges, spacers
	spacers = this.model.get("spacers");
	this.collisions_info = {}
	
	ranges = []
	_.each(spacers,function(e){
	    identify_data.collisions[e.id] = _.filter(ranges,
						      function(r){
							  return !(r[0] > (e.get("start")+23) || r[1] < e.get("start"))
						      }).length;
	    ranges.push([e.get("start"),e.get("start")+23])
	});
    },

    draw_spacers:function(){
    var el, canvas_w, canvas_h, svg;
    
	//config and create for SVG

	/*
	  el = $("#identify .spacers-svg-container")
	  canvas_w = 400, canvas_h = 200
	  svg = el.svg(null, 0, 0, canvas_w,canvas_h,0,0,canvas_w,canvas_h).svg('get');
	  $(svg._svg).attr("height",""+ canvas_h + "px");
	  $(svg._svg).attr("width", ""+ canvas_w + "px");

	*/

	
	//draw functions and config
	strand_ofs = 5;
	collision_ofs = 3;
	spacer_color = "blue"
	strand_color = "black"
	function draw_query_spacer(spacer){
	    var left_f,right_f, opts, left, right,top;
	    if(spacer.strand==1){
		left_f = spacer.start / submit_data.input_sequence.length;
		right_f = (spacer.start +23) / submit_data.input_sequence.length;
		top = canvas_h / 2 - strand_ofs - collision_ofs*identify_data.collisions[spacer.id]
	    } else {
		left_f = (submit_data.input_sequence.length - spacer.start - 23) / submit_data.input_sequence.length;
		right_f = ( submit_data.input_sequence.length - spacer.start) / submit_data.input_sequence.length;
		top = canvas_h/2 + strand_ofs + collision_ofs * identify_data.collisions[spacer.id]
	    }
	    left = left_f * canvas_w;
	    right = right_f * canvas_w;
	    console.log(left, right, top)
	    p = this.svg.createPath();
	    p.moveTo(left,top);
	    p.lineTo(right,top);
	    opts = {stroke:spacer_color,strokeWidth:1};
	    this.svg.path(p,opts);
	}
	
	function draw_query_strands(){
	    var left_f,right_f,left,right,opts,p;
	    left_f = 0;
	    right_f = 1;
	    left = left_f * canvas_w;
	    right = right_f * canvas_w;
	    top_plus = canvas_h/2 - strand_ofs * .5
	    top_minus = canvas_h/2 + strand_ofs *.5
	    
	    opts = {stroke:strand_color, strokeWidth:1}
	    p = this.svg.createPath();
	    p.moveTo(left, top_plus)
	    p.lineTo(right,top_plus)
	    this.svg.path(p,opts)

	    p = this.svg.createPath();
	    p.moveTo(left,top_minus)
	    p.lineTo(right,top_minus)
	    this.svg.path(p,opts)
	}

	//draw loop
	draw_query_strands()
	_.each(identify_data.spacers,
	       function(e,i){
		   draw_query_spacer(e);
	       });
	
    }

})
