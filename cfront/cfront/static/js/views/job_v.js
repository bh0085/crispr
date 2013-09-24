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
    update_status:function(){
	var done_count = _.filter(this.model.get("spacers").models,function(e){return e.get("computed_hits")}).length
	var total_count = this.model.get("spacers").length
	
	if(done_count < total_count){
	    this.$(".status .text").empty().append($("<span>").text("found spacers, scoring offtargets ("+ done_count + " of " + total_count +")"))
	    frac = .33 + .33*(done_count/total_count)
	}  else if(!current_job.get("files_ready")){
	    ndone = _.filter(this.model.get("files").models,function(m){return m.get('ready')}).length
	    this.$(".status .text").empty().append($("<span>")
						   .append($("<p>").text('now running primer design to generate ')
							   .append($("<a>",{href:"#downloadable"})
								   .text('Downloadable results'))
							  )
						   .append($("<p>").text("this step may take several minutes ("+ndone + " of 2 files ready)"))
						   .append($("<p>").text('Interactive results are ready '))

						  )
	    frac = .66 + .33 * ndone /2
	} else {
	    frac = 1
	} 
	this.$(".status").toggleClass("done",current_job.get("files_ready")?true:false);
	this.$(".status .progress .bar").css("width"," "+ (frac * 100)+"%");
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
	this.update_status();

	var self = this
	_.each(this.model.get("spacers").models,function(s){
	    self.binder.bindTo(s, "change:score",self.update_status, self);
	});

	_.each(this.model.get("files").models,function(f){
	    self.binder.bindTo(f, "change:ready",self.update_status, self);
	});

	self.binder.bindTo(this.model, "change:files-ready", this.update_status,this)
	this.$(".files-area").empty().append(new FileListV({job:this.model}).render().$el);
	this.$(".svg-container").append(this.svgv.render().$el)
	this.$(".nickase-v-container").append(this.nsvgv.render().$el)
	
        return this;
    },

  
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
