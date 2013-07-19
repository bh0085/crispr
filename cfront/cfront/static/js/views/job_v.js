/* job view that listens to joined relations of job to render spacers, hits as they come in */
JobV = Backbone.View.extend({
    template:$("#job-v-template").html(),
    className:"job-v",
    tagName:"div",
    initialize:function(){
	jv = this
	//right now, just assumes that the spacers are initialized on launch
	this.rendered_spacers = {}
	this.compute_collisions()
	this.binder = new Backbone.EventBinder()
    },   
    update_status:function(){
	
	var done_count = _.filter(this.model.get("spacers").models,function(e){return e.get("computed_hits")}).length
	var total_count = this.model.get("spacers").length
	
	if(done_count < total_count){
	    this.$(".status .text").empty().append($("<p>").text("aligning spacers, ("+ done_count + " of " + total_count +")"))
	}  else {
	    this.$(".status").addClass("done");
	    this.$(".status .text").empty().append($("<p>").text("done aligning spacers"))
	}
	this.$(".status .progress .bar").css("width"," "+ (done_count/total_count * 100)+"%")

    },
    render:function(){
	var done_count = _.filter(this.model.get("spacers").models,
				  function(e){return e.get("computed_hits")}).length
	var total_count = this.model.get("spacers").length
	
	params = this.model.toJSON()
	params.done = total_count == done_count;
	this.$el.html(_.template(this.template,params))
        var selt = this.$(".selection-svg");  
	this.canvas_w= 500
	this.canvas_h = 150
	this.svg = selt.svg(null, 0, 0,this.canvas_w,this.canvas_h,0,0,this.canvas_w,this.canvas_h).svg('get');
	$(this.svg._svg).attr("height",""+ this.canvas_h + "px");
	$(this.svg._svg).attr("width", ""+ this.canvas_w + "px");
	this.update_status();

	this.draw_spacers();
	var self = this
	_.each(this.model.get("spacers").models,function(s){
	    self.update_spacer(s)
	    self.binder.bindTo(s, "change:score",self.update_spacer, self);
	    self.binder.bindTo(s, "change:active",self.update_spacer,self);
	})
        return this;
    },
    destroy:function(){
	this.binder.undbindAll();
	delete this.binder;
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
    },

    draw_spacers:function(){
	
	//draw functions and config
	this.strand_ofs = 5;
	this.collision_ofs = 5;
	this.spacer_color = "lightgray"
	this.spacer_width = 5
	this.strand_color = "black"
	


	//draw loop
	this.draw_query_strands()
	var spacers = this.model.get("spacers")
	for (var i = 0 ; i < spacers.length ; i++){
	       this.draw_query_spacer(spacers.models[i]);
	}
	
    },
    draw_query_strands:function(){
	var left_f,right_f,left,right,opts,p;
	left_f = 0;
	right_f = 1;
	left = left_f * this.canvas_w;
	right = right_f * this.canvas_w;
	top_plus = halfint(this.canvas_h/2 - this.strand_ofs * .5)
	top_minus = halfint(this.canvas_h/2 + this.strand_ofs *.5)
	
	opts = {stroke:this.strand_color, strokeWidth:1}

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
	var left_f,right_f, opts, left, right,top, input_sequence;
	input_sequence = spacer.get("job").get("sequence")
	if(spacer.get("strand")==1){
	    left_f = spacer.get("start") /input_sequence.length;
	    right_f = (spacer.get("start") +23) / input_sequence.length;
	    top =halfint( this.canvas_h / 2 - this.strand_ofs - this.collision_ofs*(this.collisions[spacer.id] + 1))
	} else {
	    left_f = (input_sequence.length - spacer.get("start") - 23) / input_sequence.length;
	    right_f = ( input_sequence.length - spacer.get("start")) / input_sequence.length;
	    top =halfint(this.canvas_h/2 + this.strand_ofs + this.collision_ofs * (this.collisions[spacer.id] + 1))
	}
	left = left_f * this.canvas_w;
	right = right_f * this.canvas_w;
	p = this.svg.createPath();
	p.moveTo(left,top);
	p.lineTo(right,top);
	opts = {stroke:this.spacer_color,strokeWidth:this.spacer_width};
	el = this.svg.path(p,opts);
	$(el).attr("cid", spacer.cid);
	$(el).on("mouseover", spacer_mouse)
	this.rendered_spacers[spacer.id] = el;
    },
    update_spacer:function(spacer){	

	//max_sim = _.max(hits.pluck("similarity"))
	/*
	qthreshold = high_threshold
	score = spacer.get("score")

	color = "rgba("+ [score < score_threshold ? 255: 0 , 
			  score >= score_threshold ? Math.floor(score * 255):0,
			  0,
			  score >score_threshold?1:.25].join(",") + ")"
	*/
	color = "lightgray"
	color = spacer.get("active")?  "rgba(122, 122, 255, .7)" : color;
	swidth = spacer.get("active") ? 10 : this.spacer_width; 


	p = this.svg.configure(this.rendered_spacers[spacer.id],{stroke:color, strokeWidth:swidth})
    }
})

JobSV = Backbone.View.extend({
    template:$("#job-s-v-template").html(),
    className:"job-spacer-list-v",
    initialize:function(options){
	jsv = this;
	this.views_by_id = {}
	this.binder = new Backbone.EventBinder()

	this.binder.bindTo(this.model, "change:score", 
			   function(m,v){this.spacers.remove(m);this.spacers.add(m);}
			   , this)

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
