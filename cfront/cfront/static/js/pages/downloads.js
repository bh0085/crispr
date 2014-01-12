scurrent_job = null;
var APP
function init_page(){
    APP.fetch_spacers = false

    //if we have a subdomain prefix in the pathname, this will cause problems.
    init_state.job.nicks = init_state.nicks
    current_job = new JobM(init_state.job)
    APP = {}
    
    //SETUP BREADCRUMBS
    $(".breadcrumb").append($("<li>")
			    .append($("<a>",{"href":current_job.get("job_page_url")})
				    .text('Job "'+current_job.get("name")+'"'))
			    .append($("<span>",{"class":"divider"}).text("/"))
			   )

    $(".breadcrumb").append($("<li>",{"class":"active"})
			    .text("Downloads"))

    var dlview = new DownloadsV({model:current_job})
    $("#downloads-container").empty().append(dlview.render().$el)
    console.log("RUNNING INIT CODE") 
  
}

var DownloadsV = Backbone.View.extend({
    template:$("#downloads-v-template").html(),
    className:"downloads-view",
    render:function(){
	this.$el.html(_.template(this.template,this.model.toJSON()))
	return this
    }
})
