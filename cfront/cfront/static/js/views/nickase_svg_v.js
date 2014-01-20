
/* SVG renderer for the nickase model */
NickaseGraphicalV = Backbone.View.extend({
    className:"svg-container nickase-graphical-view",
    base_to_x:function(base){
	var j = this.job
	frac = (base ) / j.get("sequence").length
	if(this.cwidth == 0 || this.cwidth == null){
	    return frac * 600 ///HACK
	}
	return frac * this.cwidth;
    },
    x_to_base: function(x){
	var j = this.job
	frac = x / this.cwidth

	if(this.cwidth == 0 || this.cwidth == null){
	    frac = x / 600 ///HACK
	}

	var base =  Math.floor(  frac * j.get("sequence").length )
	return base
    },
    offset_to_y:function(ofs){
	return ( this.default_height  - 60 ) +  -1 * 20 * ofs
    },   
    initialize:function(){
	this.job = this.model
	var self = this
	
	gview = this
	this.cwidth = $(window).width() - 100 /// temporary HACK!!
	this.cheight = 300
	this.default_height = 300

	this.$el.on("mousedown",$.proxy(this.on_mousedown, this))
	this.$el.on("mousemove",$.proxy(this.on_mousemove, this))
	this.$el.on("mouseup",$.proxy(this.on_mouseup, this))
	APP.on("changed_region_or_nicks",this.render, this)
	$(window).on("resize",$.proxy(this.render,this))
	this.job.on("change:active_nick",this.draw_spacers, this)
    },
    on_mousedown:function(ev){
	var sequence_y = this.offset_to_y(0)
	this.dragging = true;
	this.start_x = this.x_to_base(ev.offsetX)
    },
    on_mouseup:function(ev){
	if (this.dragging){
	    this.dragging = false;

	    var current_x = this.x_to_base(ev.offsetX);
	    var start =Math.min(this.start_x, current_x)
	    var end = Math.max(this.start_x, current_x)
	    this.job.update_region(start, end)

	    this.start_x = null;
	}
    },
    on_mousemove:function(ev){
	if (this.dragging){
	    var current_x = this.x_to_base(ev.offsetX);
	    var start =Math.min(this.start_x, current_x)
	    var end = Math.max(this.start_x, current_x)
	    this.job.update_region(start, end)
	}
    },
    render:function(){	
	this.svg = this.$el.svg({}).svg("get");
	this.svg.clear()

	this.cwidth = this.$el.width()
	$(this.svg._svg).attr("width",this.cwidth + "px")
	$(this.svg._svg).attr("height", 300+ "px")

	this.draw_strands()
	this.draw_scales()
	this.draw_spacers()
	this.draw_selection()
	
	//RENDERS THE SPANS IN THIS VIEW
	var included_nicks = APP.get_included_nicks()
	this.spans = []
	for(var i = 0 ; i < Math.min(included_nicks.length,10) ; i++){
	    var n = included_nicks[i]
	    this.spans.push( {fwd_strand:n.get("spacerfwd"),
			      rev_strand:n.get("spacerrev"),
			      parent:this,
			      offset:i+2,
			      score:n.get("score"), 
			      nick:n
			     })
	}
	this.views_list = _.map(this.spans,function(e ){return new SpanSVGView({model:e}) })
	if(this.views_list.length == 0){
	    this.svg.text(null,20,this.offset_to_y(1),
			  "no guide pairs have an overhang spanning bases " 
			  + this.job.region_bounds()[0]+ " through " 
			  + this.job.region_bounds()[1])
	} else {
	    for (var i = 0 ; i < this.views_list.length; i++){
		this.views_list[i].render()
	    }
	}


	return this
    },
    draw_strands:function(){
	hi = halfint
	yA0 = this.offset_to_y(.25)
	yA1 = this.offset_to_y(-.25)
	xA0 = this.base_to_x(0)
	xA1 = this.base_to_x(this.job.get("sequence").length)

	var pA = this.svg.createPath()
	pA.moveTo(xA0,hi(yA0))
	pA.lineTo(xA1,hi(yA0))
	pA.moveTo(xA0,hi(yA1))
	pA.lineTo(xA1,hi(yA1))

	var pathA = this.svg.path(null, pA)
	this.svg.configure(pathA,{"strokeWidth":1,
			      "stroke":"black"})
		   
	csvg = this.svg;
    },
    draw_scales:function(){
	var s = this.job.get("sequence")
	var inc
	if(s.length < 100){
	    inc = 20
	} else if (s.length < 300) {
	    inc  = 50
	} else {
	    inc = 100
	}
	var b = 0
	while(b < s.length){
	    var x0 = this.base_to_x(b)
	    var y0 = this.offset_to_y(-.25)
	    var y1 = this.offset_to_y(-.75)
	    var cl= this.svg.line(x0,y0,x0,y1)
	    this.svg.configure(cl,{stroke:"black",
				  strokeWidth:"1"})
	    this.svg.text(null, x0+5, y1+ 5, ""+b)
	    b+= inc;
	}
    },
    draw_spacers:function(){
	
	if(this.spacer_els != null){
	    for (var i = 0; i < this.spacer_els.length ; i++){
		this.spacer_els[i].remove()
	    }
	}
	this.spacer_els = null

	var n = current_job.get("active_nick")
	if(n){
	    var spacers = [n.get("spacerfwd"),
			   n.get("spacerrev")]
	    this.spacer_els = []
	    var xs = []
	    for (var i = 0 ; i < spacers.length ; i++){
		var spc = spacers[i]
		var y0 = this.offset_to_y(+.25 * spc.get("strand"))
		var y1 = y0 -10*spc.get("strand")
		var xbar = this.base_to_x(spc.cut_site())
		var spacer_path = this.svg.polygon([[xbar,y0],[xbar-5,y1],[xbar+5,y1]],
						   {fill:spc.quality_color()})
		var $spacer_path = $(spacer_path)
		$spacer_path.attr("class", "spacer active")
		this.spacer_els.push($spacer_path)
		xs.push(xbar)
		var text = this.svg.text(null, xbar,4+ y1 - 10*spc.get("strand"),"g" + spc.get("rank") )
		this.spacer_els.push(text)
		var connector=  this.svg.line(null,halfint(xbar),halfint(this.offset_to_y(0)),
					      halfint(xbar), y0)
		this.svg.configure(connector, {stroke:"black",
					       strokeWidth:1})
		this.spacer_els.push(connector)

	    }
	    var connector=  this.svg.line(null,xs[0],halfint(this.offset_to_y(0)),
					  xs[1], halfint(this.offset_to_y(0)))
	    this.svg.configure(connector, {stroke:"black",
					   strokeWidth:1})
	    this.spacer_els.push(connector)

	}
    },
    draw_selection:function(){
	var rb = current_job.region_bounds()
	if(rb != null){
	    l = this.svg.line(null,-1 + this.base_to_x(current_job.region_bounds()[0]),
			      .5+this.offset_to_y(0),
			      1 +  this.base_to_x(current_job.region_bounds()[1]),
			      .5+ this.offset_to_y(0))
	    this.svg.configure(l,{stroke:"rgba(0, 0, 255, .25)",strokeWidth:5})

	} 
    }
})




/* span view rendered into a nickase graphical view */
SpanSVGView = Backbone.View.extend({
    initialize:function(opts){
	this.model = opts.model
    },
    render:function(svg){
	var s = this.model
	var svg = s.parent.svg
	if (svg == null){ throw "no svg yet exists..."}
	var y = s.parent.offset_to_y(s.offset)
	var x0 = s.parent.base_to_x(s.fwd_strand.cut_site())
	var x1 = s.parent.base_to_x(s.rev_strand.cut_site())
	if(x0 > x1){
	    temp = x0
	    x0 = x1
	    x1 = temp
	}

	//first time rendered, create an element
	this.group = svg.group()
	var $g = $(this.group)

	var text = svg.text(this.group, x1+4,y+3,"score = " + Math.round(s.nick.get("score")))
	$(text).attr("class","score")
	/*
	var text2 = svg.text(this.group, x0-4,y+3,s.nick.get("name"),{textAnchor:"end"})
	$(text2).attr("class","name")
	*/

	var path = svg.line(this.group, x0,y,x1,y)
	svg.configure(path,{"strokeWidth":9,
			    "stroke":s.nick.quality_color()})

	var $path=$(path)
	$g.css("cursor","pointer")
	$g.attr("cid", s.nick.cid)
	$g.attr("class","nick-svg-view-group")
	/*
	$g.on("hover",function(ev){
	})
	    */
	$g.on("mouseenter",function(){
	    if(!current_job.get("hover_locked")){
		current_job.activateNick(s.nick, true)
	    }
	    $(".hover-helper").text("(click to select "+s.nick.get("range_name")+")")
	});

	$g.on("mouseleave",function(){
	    $(".hover-helper").text("")
	});

	$g.on("mousedown", function(ev){
	    ev.stopPropagation();
	    return false
	})
	$g.on("click",function(){
	    current_job.set("hover_locked",true)
	})

	if(s.nick.get("active")){
	    $g.attr("active", true)
	}
	s.nick.on("change:active",function(){
	    $g.attr("active", s.nick.get("active"))
	});

    }
})
