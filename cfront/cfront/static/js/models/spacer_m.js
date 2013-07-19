/** backbone model for a spacer */
var SpacerM = Backbone.RelationalModel.extend({
    sequence:null,
    id:null,
    guide:null,
    strand:null,
    position:null,

    computed_hits:false,
    computing_hits:false,
    active:false,
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
        var id = this.id ? this.id : -1;
        var url = '/r/spacer/' + id;
        return url;
    },
    initialize:function(){
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
	    }

	    for (var i = 0 ; i < genic.length ; i++){
		var hjson = genic[i]
		if (! this.get("hits").get(hjson.id)){ h = new HitM(hjson);}
		else { h = this.get("hits").get(hjson.id) }
		this.genic.add(h)
	    }
	    
	}
	if(this.get("computed_hits")){
	    $.getJSON("/s/retrieve_hits/"+this.id,{},
		      $.proxy(parse_hits,this))
	} else {
	    this.on("change:computed_hits",function(){
		$.getJSON("/s/retrieve_hits/"+this.id,{},
			  $.proxy(parse_hits,this))
	    },this)
	}
    },
    locus:function(){
	return this.get("job").get("chr") +":"
	    +(this.get("strand") == 1?"+" : "-")+ (this.get("position") + this.get("job").get("start"))
    },
    rank:function(){
	return current_job.get("spacers").indexOf(this) +1
    }
})




SpacerC = Backbone.Collection.extend({
    model:SpacerM,
    comparator:function(m){
	return -1 * m.get("score")
    }
})
SpacersDisplayC = Backbone.Collection.extend({
    model:SpacerM,
    comparator:function(m){
	return -1 * m.get("score")
    }
})
