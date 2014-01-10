scurrent_job = null;
var APP
function init_page(){
    APP.fetch_spacers = false

    //if we have a subdomain prefix in the pathname, this will cause problems.
    init_state.job.nicks = init_state.nicks
    current_job = new JobM(init_state.job)
    APP = new AppM({job:current_job, id:1})
    if(!current_job.get("start")){
	$("#nickase-container").text("job is not mapped to the genome")
    }
    //polling is disabled for the nickase view... for now...
    //current_job.poll()

 
    $(document).on("click",".explain-this-view",function(){
	$(".explanation").toggle(!$(".explanation").is(":visible"));
    });

    $(document).on("click",".explain-scores",function(){
	$(".scores-explanation").toggle(!$(".scores-explanation").is(":visible"));
    });
    
    /*
    $(document).on("click",".export",function(){
	alert("apologies, but export is not yet complete")
    });
    */
    

    current_job.on("change:active_region_nicks_count", function(){$(".active-region-nicks-count-display").text(current_job.get("active_region_nicks_count" ))})



    //CLICK STEALING LOGIC
    current_job.on("change:hover_locked",
		   function(){
		       $(".graphics").toggleClass("locked", current_job.get("hover_locked")) 
		       $("body").toggleClass("locked", current_job.get("hover_locked")) 
		       $(".pane2").toggleClass("locked", current_job.get("hover_locked")) 
		       
		   })    

    $(document).on("mouseenter",".click-grabber",function(){
	$(".hover-helper").text("click to deselect Pair "+APP.get_active_nick_name())
    })
    
    $(document).on("click",".click-grabber",function(){
	current_job.set("hover_locked",false)
    })

    $(document).on("mouseleave",".click-grabber",function(){
	$(".hover-helper").text("")
    })
    


    var rview = new NickaseV({job:current_job})
    rview.render().$el.attr("id","nickase").appendTo($("#nickase-container"))	
    $(document).on("mouseover", ".nick", {}, nick_select)

}



var AppM  = Backbone.RelationalModel.extend({
    relations:[
	{
	    key:"included_nicks",
	    type:Backbone.HasMany,
	    relatedModel:"NickM",
	    collectionType:"NickC",
	    reverseRelation:{
		key:"included",
		relatedModel:AppM,
		type:Backbone.HasOne
	    }
	},
    ],
    initialize:function(){
	current_job.on("change:active_region_hash",this.changed_region, this)
	this.compute_nicks();
    },
    changed_region:function(){
	this.compute_nicks()
	this.trigger("changed_region_or_nicks")
    },
    compute_nicks:function(){
	var all_nicks = current_job.get("nicks").models
	var rb = current_job.region_bounds()
	var changed = false;
	for (var i = 0; i < all_nicks.length ; i++){
	    var n = all_nicks[i]
	    start = Math.min(n.get("spacerfwd").cut_site(),n.get("spacerrev").cut_site())
	    end = Math.max(n.get("spacerfwd").cut_site(),n.get("spacerrev").cut_site())

	    
	    if ( rb == null || ( start < rb[0]	&& end > rb[1] ) ){
		if(n.get("included") != this.id){
		    n.set("included",this.id)
		    changed = true
		}
	    } else {
		if(n.get("included") == this){
		    n.set("included",null)
		    changed = true
		    if(n.get("active")){
			current_job.activateNick(n,false)
		    }
		}
	    }
	}
	current_job.set("active_region_nicks_count", this.get("included_nicks").length)
	if(changed){
	    this.trigger("changed_nicks")
	}
    },

    get_included_nicks:function(){
	if(this.get("included_nicks") == null){
	    this.compute_nicks()
	}
	return this.get("included_nicks").models
    },
    get_active_nick_name:function(){
	var n = current_job.get("active_nick")
	if (n == null){ return "--"}
	return "" + n.get("spacerfwd").get("rank") + "<-->" + n.get("spacerrev").get("rank")
    }
})
