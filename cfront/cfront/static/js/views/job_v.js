/* job view that listens to joined relations of job to render spacers, hits as they come in */
JobV = Backbone.View.extend({
    template:$("#job_v_template").html(),
    className:"job_v",
    tagName:"div",
    initialize:function(){
	jv = this
	//right now, just assumes that the spacers are initialized on launch
	this.rendered_spacers = {}

	if(!this.model.get('computed_spacers')){
	    throw "for now we assume that spacers are already computed (hits need not be)"
	    //this.model.on("add:spacers", this.draw_spacer, this)
	}
	_.each(this.model.get("spacers"), function(e){
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
        var selt = this.$(".selection-svg");  

	this.canvas_w = 400 
	this.canvas_h = 200

	this.svg = selt.svg(null, 0, 0, this.canvas_w,this.canvas_h,0,0,this.canvas_w,this.canvas_h).svg('get');
	$(this.svg._svg).attr("height",""+ this.canvas_h + "px");
	$(this.svg._svg).attr("width", ""+ this.canvas_w + "px");
        return this;
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
	this.spacer_width = "5"
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
	this.rendered_spacers[spacer.id] = this.svg.path(p,opts);
    },
    update_query_spacer:function(spacer){
	hits = spacer.get("hits")
	
	max_sim = _.max(hits.pluck("similarity"))
	qthreshold = score_threshold
	score = max_sim
	color = "rgba("+ [score < score_threshold ? 255: 0 , 
			  score >= qthreshold ? Math.floor(score * 255):0,
			  0,
			  score >.75?1:.25].join(",") + ")"
	p = this.svg.configure(this.rendered_spacers[spacer.id],{stroke:color})
    }
})
var score_threshold = .75
/** views spacers within a job as a grouped list 
 * uncategorized
 * good
 * bad
 */

SpacersDisplayC = Backbone.Collection.extend({
    model:SpacerM
})
JobSV = Backbone.View.extend({
    template:$("#job-s-v-template").html(),
    initialize:function(options){
	jsv = this;
	this.views_by_id = {}
	this.model.on("computed_one",
		      function(e){
			  console.log("computed one")
			  this.spacers.remove(e)
			  this.spacers.add(e)
		      }, this)
	this.spacers = new SpacersDisplayC()
	this.spacers.on("add", this.add_one, this)
	this.spacers.on("remove", this.remove_one, this)
    },
    render:function(){
	this.$el.html(_.template(this.template,{}))
	_.each(this.model.get("spacers").models,
	       $.proxy(function(e){this.spacers.add(e)},this))
	return this
    },
    add_one:function(spacer){
	var view, $parent
	view = new SpacerListV({model:spacer})
	this.views_by_id[spacer.id] = view;
	if (spacer.get("score")==null){
	    $parent = this.$(".uncategorized.section")
	} else if (spacer.get("score")<score_threshold){
	    $parent = this.$(".bad.section")
	} else if (spacer.get("score")>=score_threshold){
	    $parent = this.$(".good.section")
	}
	$parent.append(view.render().$el)
    },
    remove_one:function(spacer){
	var v = this.views_by_id[spacer.id]
	delete this.views_by_id[spacer.id]
	v.remove()
    }
})

/** */
SpacerListV = Backbone.View.extend({
    template: $("#spacer-list-v-template").html(),
    className: "spacer-list-v",
    tagName: "li",
    render:function(){
	model_json = this.model.toJSON()
	model_json["rank"] = 1
	this.$el.html(_.template(this.template,model_json))
	return this
    }
})

function halfint(number){return Math.floor(number) + .5}
