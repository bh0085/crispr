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
	computed_hits:false,
	computing_hits:false,

	n_hits_computed:0,
	n_hits_ready:0,
	computed_n_hits:0,
	
	poll_timeout:250
    },
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
	this.on("change:computed_spacers",this.on_all_spacers_ready,this)
	this.on("change:computed_n_hits",this.on_one_hit_ready,this)
	this.on("add:spacers",this.on_spacer_added, this)
    },
    fetched:function(){
	this.await_hits()
	this.await_spacers()
	var rview = new ReadoutV({job:this})
	rview.render().$el.appendTo($("#readout .readout-v-container"))
    },
    /** Rest URL for a Job */
    url: function () {
        var id = this.id ? this.id : -1;
        var url = '/r/job/' + id;
        return url;
    },
    //waiting for hits, polls. true when done.
    await_hits:function(){
	$.getJSON("/j/check_hits/"+this.id,{},
		  $.proxy(function(val){
		      this.fetch()

		      if(!val){
			  this.set("poll_timeout",this.get("poll_timeout") + 100);
			  window.setTimeout($.proxy(this.await_hits,this), 
					    this.get("poll_timeout"));
		      }},this))
    },
    //waiting for spacers, polls. true when done
    await_spacers:function(){
	$.getJSON("/j/check_spacers/"+this.id,{},
		  $.proxy(function(val){
		      this.fetch()
		      if(!val){
			  this.set("poll_timeout",this.get("poll_timeout") + 100);
			  window.setTimeout($.proxy(this.await_spacers,this), 
					    this.get("poll_timeout"));
		      }},this))
    },

    //fires a change to n_hits
    on_one_hit_ready:function(){
	$.getJSON("/j/retrieve_hits/"+this.id,
		  {},
		  $.proxy(
		      function(data){
			  for (var i = 0 ; i < data.length ; i++){
			      var h = data[i]
			      if (! this.get("hits").get(h.id)){
				  h = new HitM(h);
			      }
			  }
			  
			  _.each(this.get("spacers").models,
				 $.proxy(function(e,i){
				     if(e.get("hits").length >0){
					 if (! e.get("computed_hits")){
					     e.fetch();
					 }
				     }
				 },this)
				)
			      },this))
    },
    //fires a trigger "all_spacers_ready
    on_all_spacers_ready:function(){
	$.getJSON("/j/retrieve_spacers/"+this.id,
		  {},
		  $.proxy(
		      function(data){
			  for (var i = 0; i < data.length ; i++){
			      var s = data[i]
			      if (! this.get("spacers").get(s.id)){
				  model = new SpacerM(s)
			      }
			  }
			  this.trigger("all_spacers_ready")
		      }
		      ,this))
    }
})
