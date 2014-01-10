/** backbone model for a job */
var JobM = Backbone.RelationalModel.extend({
    defaults:{
	sequence:null,
	id:null,
	genome:null,
	name:null,
	email:null,
	date_submitted:null,
	date_completed:null,
	
	files_ready:true,
	computing_spacers:false,
	computed_spacers:false,	
	poll_timeout:1000,
	active_spacer:null,
	active_nick:null,
	active_region_start:null,
	active_region_end:null,

	hover_locked:false,
    },
    relations:[
	{
	    key:"spacers",
	    type:Backbone.HasMany,
	    relatedModel:"SpacerM",
	    collectionType:"SpacerC",
	    includeInJSON:"id",
	    reverseRelation:{
		key:"job",
		keySource:"jobid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	},
	{
	    key:"files",
	    type:Backbone.HasMany,
	    relatedModel:"FileM",
	    collectionType:"FileCollection",
	    includeInJSON:false,
	    reverseRelation:{
		key:"job",
		keySource:"jobid",
		includeInJSON:true,
		type:Backbone.HasOne
	    }
	}
    ],
    /** Rest URL for a Job */
    url: function () {
        return routes.route_path("job_rest",{job_key:this.get("key")})
    },
    compute_export_urls:function(){
	this.set("export_gb_nicks_url", 
		 routes.route_path("gb_all_nicks",{job_key:this.get("key")}))
    },
    //waiting for hits, polls. true when done.
    poll:function(){
	var self =this

	self.fetch(
	    {success:function(){
		self.set("poll_timeout",self.get("poll_timeout") + 200);
		window.setTimeout($.proxy(self.poll,self),
				  self.get("poll_timeout"));
	    }})
	    
    },
    activateSpacer:function(s,val){
	if( val){
	    _.each(this.get("spacers").models,function(s2, i2){
		if (s2.id != s.id)
		{s2.set("active",false)}
	    });
	    this.set("active_spacer",s);
	}
    },
    activateNick:function(s,val){
	if( val){
	    _.each(this.get("nicks").models,function(s2, i2){
		if (s2.id != s.id)
		{s2.set("active",false)}
	    });
	    s.set("active",true)
	    this.set("active_nick",s);
	} else {
	    s.set("active", false)
	    this.set("active_nick",null)
	}
    },
    initialize:function(){
	var self = this
	this.compute_export_urls()
	this.set("locus", this.locus())
	this.binder = new Backbone.EventBinder()
	_.each(self.get("spacers").models, function(s,i){
	    s.on("change:active",self.activateSpacer,self)
	    s.on("change:score",function(m,v){
		self.get("spacers").sort()
		//order is important here
		_.each(self.get("spacers").models,
		       function(s,i){
			   s.compute_rank_in_job(self);
		       });
	    })
	    s.compute_rank_in_job(self);
	});

	_.each(self.get("nicks").models, function(s,i){
	    //NICKS do not autupdate...
	    //would copy code from above as appropriate
	    s.on("change:active",self.activateNick,self)
	    s.compute_rank_in_job(self);
	});

    },
    update_region:function(start,end){
	this.set("active_region_start",start)
	this.set("active_region_end",end)
	if(this.get("active_region_start") != null){
	    this.set("active_region_hash", "["+this.get("active_region_start") + ":" + (this.get("active_region_end") !== null ? this.get("active_region_end") : this.get("active_region_start"))+"]")
	} else {
	    this.set("active_region_hash", "--")
	}
    },
    region_bounds:function(){
	if(this.get("active_region_start") == null){
	    return null
	} else if (this.get("active_region_end") === null){
	    return [this.get("active_region_start"),this.get("active_region_start")]
	} else {
	    return [this.get("active_region_start"),this.get("active_region_end")]
	}
    },
    locus:function(){
	return this.get("chr") +":"+ (this.get("strand") == -1?"-":"+")
		+ (this.get("start") + (this.get("strand") == 1?-1:-4))
    },
    status_frac:function(){
	var done_count = _.filter(this.get("spacers").models,function(e){return e.get("computed_hits")}).length
	var total_count = this.get("spacers").length

	if (!this.get("computed_spacers") ){
	    frac = 0
	} else if(done_count < total_count){
	    frac = .25 + .75 *(done_count/total_count)
	} else {
	    frac = 1
	} 
	return frac
    },
    status_message:function(){
	
	var message
	if (frac == 0){
	    message = "... computing guides. this may take a few minutes jobs submitted in a batch"
	} else if( frac < 1){
	    var done_count = _.filter(this.get("spacers").models,function(e){return e.get("computed_hits")}).length
	    var total_count = this.get("spacers").length
	    message = "found guides in query sequence, scoring offtargets ("+ done_count + " of " + total_count +")";
	} else {
	    message = "done"
	}
	return message
    }				  
})			  

function spacer_select(event){
    var cid = $(this).attr("cid")
    spacer = current_job.get("spacers").getByCid(cid)
    spacer.set("active", true)
}

function nick_select(event){
    var cid = $(this).attr("cid")
    nick = current_job.get("nick").getByCid(cid)
    nick.set("active", true)
}
