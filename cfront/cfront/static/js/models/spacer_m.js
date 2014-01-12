/** backbone model for a spacer */
var SpacerM = Backbone.RelationalModel.extend({
    defaults:{
	sequence:null,
	id:null,
	guide:null,
	strand:null,
	position:null,
	computed_hits:false,
	computing_hits:false,
	active:false,
    },
    relations:[
	{
	    key:"hits",
	    type:Backbone.HasMany,
	    relatedModel:"HitM",
	    includeInJSON:"id",
	    reverseRelation:{
		key:"spacer",
		keySource:"spacerid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	}
    ],
    /** Rest URL for a Job */
    url: function () {
        return routes.route_path("spacer_rest",{spacer_id:this.id?this.id:-1})
    },
    initialize:function(){
	last_spacer = this
	this.genic = new HitCollection()
	this.top = new HitCollection()
	this.set("locus",this.locus())
	function parse_hits(data){
	    var top, genic
	    top = data.top
	    genic = data.genic

	    var h
	    
	    for (var i = 0 ; i < top.length ; i++){
		var hjson = top[i]
		if (! this.get("hits").get(hjson.id)){ h = new HitM(hjson);}
		else { h = this.get("hits").get(hjson.id) }
		this.top.add(h)
		if(h.get("ontarget")){this.set("locus",this.locus())}
	    }

	    for (var i = 0 ; i < genic.length; i++){
		var hjson = genic[i]
		if (! this.get("hits").get(hjson.id)){ h = new HitM(hjson);}
		else { h = this.get("hits").get(hjson.id) }
		this.genic.add(h)
	    }
	    
	}

	if(this.get("computed_hits") && APP.fetch_spacers){
	    $.getJSON(routes.route_path("spacer_retrieve_hits",{spacer_id:this.id}),{},
		      $.proxy(parse_hits,this))
	} else {
	    this.on("change:computed_hits",function(){
		$.getJSON(routes.route_path("spacer_retrieve_hits",{spacer_id:this.id}),{},
			  $.proxy(parse_hits,this))
	    },this)
	}	

	this.compute_quality()
	this.on("change:score",this.compute_quality,this);
    },
    locus:function(){
	if(this.get("job").get("chr")){
	    return this.get("job").get("chr") +":"
		+(this.get("strand") == 1?"+" : "-")+ (this.get("position") + this.get("job").get("start"))
	} else { return "unknown" }
    },
    compute_rank_in_job:function(job){
	this.set("rank",job.get("spacers").indexOf(this) +1)
    },
    compute_quality:function(){
	var s = this.get("score")
	if(s >= SpacerM.high_quality_threshold){
	    this.set("quality","high")
	} else if ( s>= SpacerM.low_quality_threshold){
	    this.set("quality","medium")
	} else if ( s>0){
	    this.set("quality","low")
	} else {
	    this.set("quality","no")
	}
    },
    cut_site:function(){
	return this.get("strand") == 1 ? this.get("start") + 20 : this.get("start") + 3
    },
    quality_color:function(){
	if (this.get("quality") == "high"){return "green"}
	else if (this.get("quality") == "medium"){return "yellow"}
	else if (this.get("quality") == "low"){return "red"}
	else{return "black"}
    }
})

SpacerM.high_quality_threshold = .5;
SpacerM.low_quality_threshold = .2;


SpacerC = Backbone.Collection.extend({
    model:SpacerM,
    comparator:function(m){
	return -1 * m.get("score")
    }
})
