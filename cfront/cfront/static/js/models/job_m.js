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
	}
    ],
    initialize:function(){
	this.set("poll_timeout",250)
	this.on("change:computed_spacers",this.compute_hits,this)
    },
    /** Rest URL for a Job */
    url: function () {
        var id = this.id ? this.id : -1;
        var url = '/r/job/' + id;
        return url;
    },
    compute_spacers:function(){
	$.getJSON("/j/compute_spacers/"+this.id,{},
		  $.proxy(function(done){
		      //done should be true. we fetch and let the "computed_spacers"
		      //callback handle the change of status
		      this.fetch();
		  },this)
		 )
    },
    compute_hits:function(){
	if (!this.get("computed_spacers")){
	    console.log("no spacers yet!")
	    return
	}
	$.getJSON("/j/compute_hits/"+this.id,
		  {},
		  $.proxy(function(done){
		      //done should be false. we await hits regardless.
		      this.await_hits()
		  },this))
    },
    await_hits:function(){
	$.getJSON("/j/check_hits/"+this.id,{},
		  $.proxy(function(val){
		      console.log(this.get("poll_timeout"))
		      if(val){
			  //done awaiting, fetches a new value for this job
			  this.fetch();
		      } else {
			  //continue waiting, poll the server after timeout
			  this.set("poll_timeout",this.get("poll_timeout") *1.25);
			  window.setTimeout($.proxy(this.await_hits,this), this.get("poll_timeout"));
		      }
		  },this)
		 )
    }
})
