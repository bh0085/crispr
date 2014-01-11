var NickM = Backbone.RelationalModel.extend({
    defaults:{
	unorm_score:null,
	score: null,
	n_offtargets:null,
	n_genic_offtargets:null,
	rank:null,
    },
    relations:[
	{
	    key:"spacerfwd",
	    keySource:"spacerfwdid",
	    type:Backbone.HasOne,
	    relatedModel:"SpacerM",
	    includeInJSON:"id",
	},

	{
	    key:"spacerrev",
	    keySource:"spacerrevid",
	    type:Backbone.HasOne,
	    relatedModel:"SpacerM",
	    includeInJSON:"id",
	},
	{
	    key:"job",
	    type:Backbone.HasOne,
	    relatedModel:JobM,
	    includeInJSON:"id",
	    reverseRelation:{
		key:"nicks",
		includeInJSON:"id",
		collectionType:"NickC",
		type:Backbone.HasMany,
	    }
	}
    ],
   
    initialize:function(){
	this.compute_quality()
	this.compute_export_urls()
	this.get("spacerfwd").on("change:rank",this.compute_name, this)
	this.get("spacerrev").on("change:rank",this.compute_name, this)
	
	var cuts = [this.get("spacerfwd").cut_site(), this.get("spacerrev").cut_site()]
	this.set("start", Math.min(cuts[0],cuts[1]))
	this.set("end", Math.max(cuts[0], cuts[1]))
	this.compute_name()

	
    },
    compute_export_urls:function(){
	this.set("export_gb_url", 
		 routes.route_path("gb_one_nick",{job_key:this.get("job").get("key"),
						 spacerfwdid:this.get("spacerfwd").id,
						 spacerrevid:this.get("spacerrev").id}))

	this.set("export_csv_forward_guide_url", 
		 routes.route_path("csv_one_spacer",{job_key:this.get("job").get("key"),
						     spacerid:this.get("spacerfwd").id}))
	this.set("export_csv_reverse_guide_url", 
		 routes.route_path("csv_one_spacer",{job_key:this.get("job").get("key"),
						     spacerid:this.get("spacerrev").id}))
    },
    compute_name:function(){
	this.set("name","g" + this.get("spacerfwd").get("rank") + "<-->g" + this.get("spacerrev").get("rank"))
	this.set("range_name",this.get("start") + ".." + this.get("end"))

    },
    //computes rank by score
    compute_rank_in_job:function(job){
	this.set("rank",job.get("nicks").indexOf(this) +1)
    },
    // colors the nick by quality
    compute_quality:function(){
	var s = this.get("score")
	if(s >= NickM.high_quality_threshold){
	    this.set("quality","high")
	} else if ( s>= NickM.low_quality_threshold){
	    this.set("quality","medium")
	} else if ( s>0){
	    this.set("quality","low")
	} else {
	    this.set("quality","no")
	}
	this.set("color",this.quality_color())
    },
    quality_color:function(){
	if (this.get("quality") == "high"){return "green"}
	else if (this.get("quality") == "medium"){return "yellow"}
	else if(this.get("quality") == "low"){return "red"}
	else{return "black"}
    }
})

NickM.high_quality_threshold = 20;
NickM.low_quality_threshold = 10;

var NickC = Backbone.Collection.extend({
    comparator:function(m){
	return -1 * m.get("score")
    }
})
