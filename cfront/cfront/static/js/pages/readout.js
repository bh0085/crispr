current_job = null;
function init_page(){
    APP.fetch_spacers=true
    


    //if we have a subdomain prefix in the pathname, this will cause problems.
    current_job = new JobM(init_state.job)
    current_job.poll()

  
    //SETUP BREADCRUMBS
    $(".breadcrumb").append($("<li>")
			    .append($("<a>",{"href":current_job.get("job_page_url")})
				    .text('Job "'+current_job.get("name")+'"'))
			    .append($("<span>",{"class":"divider"}).text("/"))
			   )

    $(".breadcrumb").append($("<li>",{"class":"active"})
			    .text("Guides & Offtargets"))


    var rview = new ReadoutV({job:current_job})
    rview.render().$el.attr("id","readout").appendTo($("#readout-container"))
    rview.draw_job()
    current_job.get("spacers").models[0].set('active',true);
    $(document).on("mouseover", ".spacer", {},spacer_select)



}

