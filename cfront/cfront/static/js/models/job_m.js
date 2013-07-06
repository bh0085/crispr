/** backbone model for a job */
var JobM = Backbone.RelationalModel.extend({
    sequence:null,
    id:null,
    genome:null,
    name:null,
    email:null,
    date_submitted:null,
    date_completed:null,
    poll_timeout:250,
    relations:[
	{
	    key:"spacers",
	    type:Backbone.HasMany,
	    relatedModel:"SpacerM",
	    includeInJSON:false,
	    reverseRelation:{
		key:"job",
		keySource:"jobid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	},
	{
	    key:"hits",
	    type:Backbone.HasMany,
	    relatedModel:"HitM",
	    includeInJSON:false,
	    reverseRelation:{
		key:"job",
		keySource:"jobid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	}
    ],
    initialize:function(){
	this.set("poll_timeout",250)
    },
    /** Rest URL for a Job */
    url: function () {
        var id = this.id ? this.id : -1;
        var url = '/r/job/' + id;
        return url;
    },
    await_hits:function(){
	$.getJSON("/j/check_hits/"+this.id,{},
		  $.proxy(function(val){
		      if(val){$.getJSON("/j/retrieve_hits/"+this.id,
				       {},
				       $.proxy(
					   function(data){
					       this.set("hits",data)
					   }
					   ,this))
			     } else {
				 this.set("poll_timeout",this.get("poll_timeout") *1.25);
				 window.setTimeout($.proxy(this.await_hits,this), 
						   this.get("poll_timeout"));
			     }},this))
    },
    await_spacers:function(){
	$.getJSON("/j/check_spacers/"+this.id,{},
		  $.proxy(function(val){
		      if(val){$.getJSON("/j/retrieve_spacers/"+this.id,
				       {},
				       $.proxy(
					   function(data){
					       this.set("spacers",data)
					   }
					   ,this))
			     } else {
				 this.set("poll_timeout",this.get("poll_timeout") *1.25);
				 window.setTimeout($.proxy(this.await_spacers,this), 
						   this.get("poll_timeout"));
			     }},this))
    },
})
