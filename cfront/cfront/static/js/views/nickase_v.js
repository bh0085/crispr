NickaseSVGV = JobSVGV.extend({
    template:$("#nickase-svg-view-template").html(),
    initialize:function(){
       this.binder = new Backbone.EventBinder();
    },
    render:function(){
       this.$el.html(_.template(this.template, {}))

       return this
    },
    register_listeners:function(){},
    initial_draw:function(){},
})

var NickaseTLOptionsV =Backbone.View.extend({
    className:"nickase-tl-options",
    template:$("#nickase-tl-options-template").html(),
    last_range: null, /// stores the last used bounds outside of the active state
    events:{
	"change .spanning-region":"spanning_changed",
	"change .entire-region":"entire_changed"
    },
    initialize:function(){
	this.job = this.model
	this.last_range = [Math.floor(this.job.get("sequence").length / 2),
			   Math.floor(this.job.get("sequence").length/2)]
	this.job.on("change:active_region_hash",this.region_changed,this)
    },
    region_changed:function(){
	var bounds = this.job.region_bounds()

	if (bounds == null){
	    if(!this.$("entire-region").prop("checked")){
		this.$(".entire-region").prop("checked",true).trigger("change")

	    }

	} else {

	    this.last_range = [bounds[0],bounds[1]]
	    if(!this.$(".spanning-region").prop("checked")){
		this.$(".spanning-region").prop("checked",true).trigger("change")
	    }
	}

	this.$(".active-region-start-display").text(this.last_range[0])
	this.$(".active-region-end-display").text(this.last_range[1])
    },
    spanning_changed:function(ev){
	if($(ev.target).prop("checked")){
	    this.job.update_region(this.last_range[0],this.last_range[1])
	}
    },
    entire_changed:function(ev){
	if($(ev.target).prop("checked")){
	    this.job.update_region(null)
	}	
    },
    render:function(){
	this.$el.html(this.template)
	this.region_changed()

	return this
    }
})


/* html view for the nickase model */
NickaseV = Backbone.View.extend({
    className:"nickase-view",
    template:$("#nickase-v-template").html(),
    initialize:function(){
	this.job = current_job;
	//initializes a new graphics (SVG) view with this job
	this.tloptions_view = new NickaseTLOptionsV({model:this.job})
	this.ngraphics_view = new NickaseGraphicalV({model:this.job})
	this.job_nicks_view = new NickaseListView({model:this.job})
	this.detail_view = new NickaseDetailView({model:this.job})

    },
    render:function(){
	params = current_job.toJSON()
	this.$el.html(_.template(this.template,params))
	this.tloptions_view.render().$el.appendTo(this.$(".nickase-tl-options-container"))

	//SVG seems to have an issue with JQ prerendering
	this.ngraphics_view.$el.appendTo(this.$(".graphics"))
	var ng = this.ngraphics_view
	window.setTimeout($.proxy(ng.render,ng),1)

	this.job_nicks_view.render().$el.appendTo(this.$(".nicks-list"))
	this.detail_view.render().$el.appendTo(this.$(".details"))
	return this
    }	
})

