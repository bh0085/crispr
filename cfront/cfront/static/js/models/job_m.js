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
    
	computing_spacers:false,
	computed_spacers:false,	
	poll_timeout:250,
	active_spacer:null
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
	}
    ],
    /** Rest URL for a Job */
    url: function () {
        var id = this.id ? this.id : -1;
        var url = '/r/job/' + id;
        return url;
    },
    //waiting for hits, polls. true when done.
    poll:function(){
	var self =this

	self.fetch(
	    {success:function(){
		self.set("poll_timeout",self.get("poll_timeout") + 100);
		window.setTimeout($.proxy(self.poll,self),
				  self.get("poll_timeout"));
	    }})
	    
    },
    activateOne:function(s,val){
	if( val){
	    console.log("activating a spacer")
	    _.each(this.get("spacers").models,function(s2, i2){
		if (s2.id != s.id)
		{s2.set("active",false)}
	    });
	    this.set("active_spacer",s);
	}
    },
    initialize:function(){
	var self = this
	this.set("locus", this.locus())
	this.binder = new Backbone.EventBinder()
	_.each(self.get("spacers").models, function(s,i){
	    s.on("change:active",self.activateOne,self)
	})
    },
    locus:function(){
	return this.get("chr") +":"+ (this.get("strand") == -1?"-":"+")
		+ (this.get("start") + (this.get("strand") == 1?-1:-4))
    }
   
})			  


function spacer_mouse(event){
    var cid = $(this).attr("cid")
    spacer = current_job.get("spacers").getByCid(cid)
    spacer.set("active", true)
}
$(document).on("mouseover", ".spacer", {},spacer_mouse)
