JobSVGV = Backbone.View.extend({
    tagName:"div",
    className:"selection-svg svg-container",
    template:$("#job-svg-view-template").html(),
    initialize:function(){
	this.compute_collisions()
	this.rendered_spacers = {}
	this.binder = new Backbone.EventBinder()
	
	//drawing geometry
	var self = this
	this.canvas_h = 100 + (16 * 2 * _.max(_.map(self.collisions,function(e){return e})))
	this.left_f = .2;
	this.right_f = .8;
	this.canvas_w= 800;
	

    },
    //OVERIDE THIS METHOD
    register_listeners:function(){
	throw "unimplemented"
    },
    //OVERIDE THIS METHOD
    initial_draw:function(){
	throw "unimplemented"
    },
    render:function(){
	this.$el.html(_.template(this.template, {}))
	this.svg = this.$(".main-svg-canvas").svg({}).svg("get");
	$(this.svg._svg).attr("height",""+ this.canvas_h + "px");
	$(this.svg._svg).attr("width", "100%");
	this.initial_draw();
	this.register_listeners();
	return this
    },

})


SimpleSpacerSVGV = JobSVGV.extend({
    register_listeners:function(){
	var self = this
	_.each(this.model.get("spacers").models,function(s){
	    self.update_spacer(s)
	    self.binder.bindTo(s, "change:score",self.update_spacer, self);
	    self.binder.bindTo(s, "change:active",self.update_spacer,self);
	});
    },
    initial_draw:function(){
	this.draw_spacers();
    },
    compute_collisions:function(){
	var ranges, spacers
	spacers = this.model.get("spacers").models.sort(function(x,y){return x.get("start")<y.get("start")})
	this.collisions = {}
	
	ranges_fwd = []
	ranges_rev = []

	_.each(spacers,$.proxy(function(e){
	    if(e.get("strand") == 1){ranges = ranges_fwd}
	    else{ranges = ranges_rev}
	    this.collisions[e.id] = _.filter(ranges,
					     function(r){
						 return !(   r[0] > (e.get("start")+23) || r[1] <( e.get("start"))  )
					     }).length;
	    ranges.push([e.get("start"),e.get("start")+23])
	},this));
	this.ranges_fwd = ranges_fwd
	this.ranges_rev = ranges_rev
    },

    draw_spacers:function(){
	
	//draw functions and config
	this.strand_ofs = 15;
	this.collision_ofs = 12;
	this.spacer_color = "lightgray"
	this.spacer_width =10
	this.strand_color = "black"
	
	//draw loop
	this.draw_query_strands()
	var spacers = this.model.get("spacers")
	for (var i = 0 ; i < spacers.length ; i++){
	       this.draw_query_spacer(spacers.models[i]);
	}
    },
    draw_query_strands:function(){
	var left,right,opts,p;
	left = halfint(this.left_f * this.canvas_w);
	right = halfint(this.right_f * this.canvas_w);
	top_plus = halfint(this.canvas_h/2 - this.strand_ofs * .5)
	top_minus = halfint(this.canvas_h/2 + this.strand_ofs *.5)
	
	opts = {stroke:this.strand_color, strokeWidth:1}

	p = this.svg.createPath();
	p.moveTo(0,halfint(top_plus+top_minus) /2)
	p.lineTo(this.canvas_w,halfint((top_plus+top_minus)/2))
	this.svg.path(p,{stroke:"lightgray", strokeWidth:1})
	top_avg =halfint((top_plus+top_minus)/2)
	this.svg.text(null,0,-5+(top_plus+top_minus)/2,current_job.get("genome_name")+" " + (current_job.get("mapped") ? current_job.get("chr") : "") )

	t = this.svg.text(null,left-3,top_avg-5,"+"+
			  (current_job.get("mapped") ? this.model.get("start") : "??"),{"textAnchor":"end"})
	t = this.svg.text(null,right+3,top_avg+10,"-"+
			   (current_job.get("mapped") ? this.model.get("start")+this.model.get("sequence").length : "??"))

	p = this.svg.createPath();
	p.moveTo(left, top_plus)
	p.lineTo(right,top_plus)

	this.svg.path(p,opts)

	p = this.svg.createPath();
	p.moveTo(left,top_minus)
	p.lineTo(right,top_minus)
	this.svg.path(p,opts)
    },
    draw_query_spacer:function(spacer){
	var opts, left, right,top, input_sequence, left_f, right_f;
	input_sequence = spacer.get("job").get("sequence")
	left_f_rel = spacer.get("start") /input_sequence.length;
	right_f_rel = (spacer.get("start") +23) / input_sequence.length;
	if(spacer.get("strand")==1){
	    top =halfint( this.canvas_h / 2 - this.strand_ofs - this.collision_ofs*(this.collisions[spacer.id] + 1))
	} else {
	    top =halfint(this.canvas_h/2 + this.strand_ofs + this.collision_ofs * (this.collisions[spacer.id] + 1))
	}


	//coord transforms
	left_f = (this.right_f - this.left_f) * left_f_rel + this.left_f
	right_f = (this.right_f - this.left_f) * right_f_rel + this.left_f
	left = halfint(left_f * this.canvas_w) +2;
	right = halfint(right_f * this.canvas_w) -2;

	if (spacer.get("rank") <= 5){
	    if(spacer.get("strand") == 1){
		text = this.svg.text(null, left,halfint(top -8), sprintf("#%s",spacer.get("rank"))
				    ,{fontSize:11})
	    }else{
		text = this.svg.text(null, right,halfint(top +15), sprintf("#%s",spacer.get("rank"))
				    ,{fontSize:11,textAnchor:"end"})
	    }
	}

	var hi = halfint; //function(e){return Math.round(e)};
	var sw = this.spacer_width;
	p = this.svg.createPath();
	if(spacer.get("strand") == 1){
	    p.moveTo(hi(left),hi(top -sw/2));
	    p.lineTo(hi(left),hi(top +sw/2));
	    p.lineTo(hi(right - sw/2),hi(top +sw/2));
	    p.lineTo(hi(right),hi(top));
	    p.lineTo(hi(right - sw/2),hi(top -sw/2));
	    p.close();
	} else {
	    p.moveTo(hi(right),hi(top -sw/2));
	    p.lineTo(hi(right),hi(top +sw/2));
	    p.lineTo(hi(left + sw/2),hi(top +sw/2));
	    p.lineTo(hi(left),hi(top));
	    p.lineTo(hi(left + sw/2),hi(top -sw/2));
	    p.close();
	}
	opts = {fill:this.spacer_color,stroke:"rgba(0, 0, 0, 1);",strokeWidth:1};
	el = this.svg.path(p,opts);
	$(el).attr("cid", spacer.cid);
	$(el).on("mouseover", spacer_select)
	this.rendered_spacers[spacer.id] = el;
    },
    update_spacer:function(spacer){	
	color = spacer.get("active")?  "rgba(122, 122, 255, .7)" : this.spacer_color;
	p = this.svg.configure(this.rendered_spacers[spacer.id],{fill:color,stroke:"black",strokeWidth:1})
    }
})
