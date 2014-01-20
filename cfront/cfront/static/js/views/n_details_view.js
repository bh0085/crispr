
NickaseDetailView = Backbone.View.extend({
    className:"nickase-detail-view",
    template:$("#nickase-detail-v-template").html(),
    initialize:function(){
	this.model.on("change:active_nick",this.render,this)
	this.model.on("change:hover_locked",this.render,this)
    },
    render:function(){


	var nick = this.model.get("active_nick")
	if(nick == null){return this}
	this.nick =nick
	
	params = nick.toJSON()
	params.locked = this.model.get("hover_locked")

	params.forward_guide = nick.get("spacerfwd").toJSON()
	params.forward_guide.cut_site = nick.get("spacerfwd").cut_site()
	params.reverse_guide = nick.get("spacerrev").toJSON()
	params.reverse_guide.cut_site = nick.get("spacerrev").cut_site()

	this.$el.html(_.template(this.template,params))
	this.$el.toggleClass("locked",this.model.get("hover_locked"))


	$(window).on("resize", $.proxy(this.draw_dsvg, this))
	this.draw_dsvg()
	window.setTimeout($.proxy(this.draw_dsvg,this),1)
	APP.on("change:pacman",this.draw_dsvg,this)
	current_job.on("change:hover_locked",
		       function(){
			   APP.set("pacman", current_job.get("hover_locked"))
		       })
	

	return this;
    },
    draw_ruler:function(){

    },
    draw_dsvg:function(){
		
	console.log("RENDERING BASE NICKASE SVG")
	t0 = new Date()

	this.$(".details-svg-container").empty().append($("<div>").addClass("details-svg"))
	this.dsvg = $(this.$(".details-svg")).svg({}).svg("get")
	var ds = this.dsvg
	
	this.dw = this.$el.width()
	this.dh = 180

	//assigns an SVG renderer to this model so that it can be accessed by
	//child spans
	$(ds._svg).attr("height",this.dh + "px")
	$(ds._svg).attr("width",this.dw + "px")
	var hi = halfint
	var n = this.nick
	var midpoint= this.dh/2
	var spacers =[ this.nick.get("spacerfwd"),
		       this.nick.get("spacerrev")]
	var sorted_cuts = [Math.min(spacers[0].cut_site(),spacers[1].cut_site()),
			   Math.max(spacers[0].cut_site(),spacers[1].cut_site())]
	var width = sorted_cuts[1] - sorted_cuts[0] + 1
	var drawrange = [0, 
			 current_job.get("sequence").length]
	var xmargin = 25
	//converts a base to an x coord
	var dw = this.dw
	var b2x = function(base){
	    return xmargin + (base - drawrange[0])
		/(drawrange[1] - drawrange[0]) * (dw-xmargin*2)
	}


	strand_ofs = 8

	
	//gets y center of a spacer s
	var s2y = function(s){
	    return s.get("strand")  == 1? midpoint + strand_ofs+20: midpoint - strand_ofs -20;
	}

	
	var inc = 50
	var b = 0 
	while(b < drawrange[1]){
	    var x0 = b2x(b)
	    var y0 = hi(midpoint -strand_ofs )
	    var y1 = hi(midpoint )
	    var cl= ds.line(x0,y0,x0,y1,{stroke:"rgba(0, 0, 0, .5)",
				  strokeWidth:"1"})
	    var t = ds.text(null, x0+5, y1+5, ""+b,{color:"rgba(0, 0, 0, 1)"})
	    b+= inc;
	}

	var cl= ds.line(b2x(drawrange[1]),y0,(b2x(drawrange[1])),y1,{stroke:"rgba(0, 0, 0, .5)",
				     strokeWidth:"1"})
	var t = ds.text(null, b2x(drawrange[1])+5, y1+5, ""+drawrange[1],{color:"rgba(0, 0, 0, 1)"})
	

	//DRAWS THE SPACERS OVER THE STRANDS	
	var xcs = []
	//draws a spacer s
	var drawn_guide = function(s){


	    

	    var y = s2y(s)
	    var y0 = hi(y - 4)
	    var y1 = hi(y + 4)
	    if(s.get("strand") == 1){
		var x0 = hi(b2x(s.get("start")-.5))
		var x1 = hi(b2x(s.get("start") + 23.5))
		var xa = hi(x1 - 4 )
		var xc = hi(b2x(s.cut_site()+.5))
	    } else { 
		var x1 = hi(b2x(s.get("start")-.5))
		var x0 = hi(b2x(s.get("start") + 23.5))
		var xa = hi(x1 + 4)
		var xc = hi(b2x(s.cut_site()+.5))	
	    }
	    xcs.push(xc)
	    
	    ys = hi( midpoint + s.get("strand")*strand_ofs )
	    ys_comp = hi( midpoint + -1* s.get("strand")*strand_ofs )
	    yclose = s.get("strand") == +1 ? y0 : y1
	    


	    var l0 = ds.line(null,  b2x(drawrange[0]),ys,  b2x(s.cut_site()+ 0),ys)
	    var l0a = ds.line(null,  b2x(s.cut_site() + 1),ys,  b2x(drawrange[1]),ys)
	    var l1 = ds.line(null, x0,ys_comp, xc,ys_comp, {strokeWidth:3, stroke:"blue"})
	    var l2 = ds.line(null, xc,ys_comp, x1,ys_comp, {strokeWidth:3, stroke:"red"})
	    
	    ds.configure(l0,{"stroke":"black", strokeWidth:1})
	    ds.configure(l0a,{"stroke":"black", strokeWidth:1})


	    var p3 = ds.createPath()
	    p3.moveTo(xc,ys- 3*s.get("strand"))
	    p3.lineTo(xc+5,ys-7*s.get("strand"))
	    p3.lineTo(xc-5,ys-7*s.get("strand"))
	    p3.lineTo(xc,ys-3*s.get("strand"))
	    var path = ds.path(null, p3, {fill:"red"})

	    if(! APP.get("pacman")){
		var p = ds.createPath()
		p.moveTo(x0,y0)
		p.lineTo(xa,y0)
		p.lineTo(x1,(y0+y1)/2)
		p.lineTo(xa,y1)
		p.lineTo(x0,y1)
		p.lineTo(x0,y0)

		var path = ds.path(null, p)
		ds.configure(path,{stroke:"black",
				   strokeWidth:"1",
				   fill:s.quality_color()})

	    } else {
		var g = ds.group(null)
		grp = ds.add(g,$('#pacman-inline > *'));
		details_s =  ds
		details_g =  g
		xy = [x1,(y0 + y1) / 2 + .5]
		tstring = "translate("+xy[0]+" " + xy[1] + ")" + (s.get("strand") == 1 ? " rotate(180)": "") + " scale(1.5)"
		ds.configure(g,{transform:tstring})
		var p = ds.line(x0,(y0+y1)/2, x1, (y0+y1)/2, {stroke:"blue",strokeWidth:1.5})
		yclose = (y0 + y1) / 2
	    }

	    p2 = ds.createPath()
	    for (var i = 0; i < 20 ; i ++){
		p2.moveTo(b2x(s.get("start")+(i+(s.get("strand") == 1?0:4))) , yclose - (8*s.get("strand")))
		p2.lineTo(b2x(s.get("start")+(i+(s.get("strand") == 1?0:4))), ys + 8*s.get("strand"))
	    }
	    var path2 = ds.path(null, p2)
	    ds.configure(path2, {stroke:"rgba(0, 0, 0, .25)", strokeWidth:"1"})



	    return path
	}



	sp1 = drawn_guide(spacers[0])
	sp2 = drawn_guide(spacers[1])
	ds.text(10,midpoint-strand_ofs+5,"5'")
	ds.text(10,midpoint+strand_ofs+5,"3'")


	var sd = this.$(".sequence-details-container")
	str1 = current_job.get("sequence").slice(drawrange[0],sorted_cuts[0])
	str2 = current_job.get("sequence").slice(sorted_cuts[0],sorted_cuts[1])
	str3 = current_job.get("sequence").slice(sorted_cuts[1],drawrange[1])
	sd.empty()
	    .append($("<span>",{class:"sequence"}).text(str1))
	    .append($("<span>",{class:"selected sequence"}).text(str2))
	    .append($("<span>",{class:"sequence"}).text(str3))

	var so = this.$(".sequence-details-overhang-container")
	so.empty().append($("<span>").text(str2))

	console.log(new Date() - t0)

 
    },
})

