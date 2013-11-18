/* job view that listens to joined relations of job to render spacers, hits as they come in */
JobV = Backbone.View.extend({
    template:$("#job-v-template").html(),
    className:"job-v",
    tagName:"div",
    initialize:function(){
	jv = this
	//right now, just assumes that the spacers are initialized on launch
	this.binder = new Backbone.EventBinder()
	this.compute_collisions();
	this.svgv = new JobSVGV({model:this.model})
	this.nsvgv = new NickaseV({model:this.model})
    },   
    compute_collisions:function(){
	var ranges, spacers
	spacers = this.model.get("spacers").models
	this.collisions = {}
	
	ranges_fwd = []
	ranges_rev = []

	_.each(spacers,$.proxy(function(e){
	    if(e.get("strand") == 1){ranges = ranges_fwd}
	    else{ranges = ranges_rev}
	    this.collisions[e.id] = _.filter(ranges,
					     function(r){
						 return !(r[0] > (e.get("start")+23) || r[1] < e.get("start"))
					     }).length;
	    ranges.push([e.get("start"),e.get("start")+23])
	},this));
	this.ranges_fwd = ranges_fwd
	this.ranges_rev = ranges_rev
    },
    render:function(){
	var self = this;
	this.left_f = .25;
	this.right_f = .75;
	params = this.model.toJSON()

	var seq = params.sequence
	inc = 40 
	iters = Math.ceil(seq.length /inc)
	var ranges = this.ranges_fwd.concat(this.ranges_rev)
	var occupied = new Array(seq.length)

	for (var i = 0; i<seq.length;  i++){
	    occupied[i] = 0;
	}
	for (var i = 0 ; i <  ranges.length ; i++){
	    for(var j = ranges[i][0]+20; j< ranges[i][0]+23 ; j++){
		occupied[j] = Math.max(occupied[j],2);
	    }
	    for(var j = ranges[i][0]; j< ranges[i][0]+20 ; j++){
		occupied[j] = Math.max(occupied[j],1);
	    } 
	}
	seq_html = ""
	for (var i = 0 ; i < seq.length ; i++){
	    switch(occupied[i]){
	    case 0:seq_html+=seq[i];break;
	    case 1:seq_html+="<span class=occupied>"+seq[i]+"</span>";break;
	    case 2:seq_html+="<span class=nrg>"+seq[i]+"</span>";break;
	    }
	}
	params.seq_html=seq_html
	
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
	this.canvas_w=900;

	this.canvas_h = 100 + (16 * 2 * _.max(_.map(self.collisions,function(e){return e})))
	this.$(".files-area").empty().append(new FileListV({job:this.model}).render().$el);
	this.$(".svg-container").append(this.svgv.render().$el)
	this.$(".nickase-v-container").append(this.nsvgv.render().$el)
	
        return this;
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
	this.texts = []
	for (var i = 0 ; i < spacers.length ; i++){
	       this.draw_query_spacer(spacers.models[i]);
	}
	this.draw_query_annotations()
	
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
	this.svg.text(null,0,-5+(top_plus+top_minus)/2,current_job.get("genome_name")+" " + (current_job.get("mapped") ? current_job.get("chr") : "unmapped") )

	//p = this.svg.line(null,left-3,top_avg-15, left-3, top_avg+15,{stroke:"lightgray",strokeWidth:1})
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
	var self = this;
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
		self.texts.push({left:left,
				top:halfint(top +15),
				string:sprintf("#%s",spacer.get("rank")),
				opts:{fontSize:11}})
	    }else{
		
		self.texts.push({left:right,
				top:halfint(top -8),
				string:sprintf("#%s",spacer.get("rank")),
				opts:{fontSize:11,textAnchor:"end"}})

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
	$(el).on("mouseover", spacer_mouse)
	this.rendered_spacers[spacer.id] = el;
    },
    draw_query_annotations:function(){
	var self = this;
	_.each(self.texts,function(t){
	    self.svg.text(null, t.left,t.top,t.string,t.opts)
	})
    },
    update_spacer:function(spacer){	
	color = spacer.get("active")?  "rgba(122, 122, 255, .7)" : this.spacer_color;
	p = this.svg.configure(this.rendered_spacers[spacer.id],{fill:color,stroke:"black",strokeWidth:1})
    }
})

JobSV = Backbone.View.extend({
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




function halfint(number){return Math.floor(number) + .5}
