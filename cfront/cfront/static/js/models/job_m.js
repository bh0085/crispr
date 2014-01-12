/** backbone model for a job */
session_start = new Date().getTime()
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
	poll_count:0,
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

	this.set("export_gb_guides_url", 
		 routes.route_path("gb_all_guides",{job_key:this.get("key")}))

	this.set("export_all_csv_offtargets_url", 
		 routes.route_path("csv_all_guides",{job_key:this.get("key")}))
    },
    compute_page_urls:function(){
	this.set("job_page_url",
		 routes.route_path("job", {job_key:this.get("key")}))

	this.set("readout_page_url",
		 routes.route_path("readout", {job_key:this.get("key")}))

	this.set("nickase_page_url",
		 routes.route_path("nickase", {job_key:this.get("key")}))

	this.set("downloads_page_url",
		 routes.route_path("downloads", {job_key:this.get("key")}))
    },
    compute_stats:function(){
	this.set("n_spacers_done",_.filter(this.get("spacers").models,
					   function(e){return e.get("computed_hits")}).length)
	this.set("status_hash","" +this.get("n_spacers_done"))

	var submitted_ms = this.get("submitted_ms")/1000;
	var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
	d.setUTCSeconds(submitted_ms);
	this.set("date_submitted", sprintf("%s",d));

	var completed_ms = this.get("completed_ms")/1000;
	if(completed_ms != 0){
	    var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
	    d.setUTCSeconds(completed_ms);
	    this.set("date_completed", sprintf("%s",d));
	} else { this.set("date_completed",  "N/A") }
	
    },
    compute_all:function(){
	this.compute_export_urls()
	this.compute_page_urls()
	this.compute_stats()

	

    },
    //waiting for hits, polls. true when done.
    poll:function(){
	var self =this
	self.fetch(
	    {success:function(){
		self.compute_stats()
		if(self.stop_polling()){
		} else {
		    self.set("poll_count",self.get("poll_count")+1)
		    self.set("poll_timeout",self.get("poll_timeout") * 1.25);
		    
		    window.setTimeout($.proxy(self.poll,self),
				      self.get("poll_timeout"));
		}
	    }}
	)
    },
    stop_polling:function(){
	return this.get("poll_count") > 2000 || this.status_frac() >= 1
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
	this.compute_all()
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
    get_n_spacers_done:function(){
	return this.get("n_spacers_done");
    },
    status_frac:function(){
	var done_count = this.get_n_spacers_done()
	var total_count = this.get("spacers").length

	if (!this.get("computed_spacers") ){
	    frac = 0
	} else if(done_count < total_count){
	    frac = .1 + .8 *(done_count/total_count)
	} else {
	    frac = 1
	} 
	return frac
    },
    status_message:function(){
	var frac = this.status_frac();
	var message
	var frac = this.status_frac()
	console.log("printing frac: ", frac)
	if (frac == 0){
	    message = "Finding guides in the query."
	} else if( frac < 1){
	    var done_count = this.get_n_spacers_done();
	    var total_count = this.get("spacers").length
	    var remaining_string = ""
	    var seconds = ( total_count - done_count ) * 20 
	    if(seconds > 60){
		remaining_string =""+ Math.round(seconds / 60) + " minutes"
	    } else {
		remaining_string = "" + seconds + " seconds"
	    }
	    message = "About " + remaining_string + " remaining. (Analyzed "+ done_count + " of " + total_count + " guides.)";
	} else {
	    message = "Job is complete."
	}
	return message
    }, 
    fetch_all_hits:function(){
	/*

	 //was called after fetch_spacer_hits ....
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

	    for (var i = 0 ; i < genic.length ; i++){
		var hjson = genic[i]
		if (! this.get("hits").get(hjson.id)){ h = new HitM(hjson);}
		else { h = this.get("hits").get(hjson.id) }
		this.genic.add(h)
	    }
	    
	}
	*/

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
