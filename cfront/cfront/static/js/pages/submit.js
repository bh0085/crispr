function init_page(){
    //next clickhandlers
    $(document).on("click", "#submit .next",{},function(event){
	submit_read_input();
    });
    var sview = new SubmitV()
    $('#submit-container').append(sview.render().$el)
    sview.configureForm()
}

var SubmitV = Backbone.View.extend({
    template:$("#submit-section-template").html(),
    className:"scrolly-section",
    configureForm:function(){
	$form= this.$el.find('form');
	$form.submit(
	    $.proxy(function(a,b){
		var self = this;
		content = {}
		_.each($form.serializeArray(),
		       function(e){
			   content[e.name] = e.value;
		       });	    
		$.ajax({
		    dataType:"json",
		    data:content,
		    url:routes.route_path("job_post_new"),
		    type:"POST",
		    success:$.proxy(function(data){
			if (data.status == "success"){
			    if(data.job_key == null){throw "hi"}
			    window.location.assign("http://" + location.host + "/job/" + data.job_key)
			} else {
			    console.log("failed")
			    alert(data.message);
			}
			return false
		    },this), 
		    error:$.proxy(function(data){
			this.on_server_error()
			return false
		    },this)
		
		})
		return false
	    }, this))

    },
    render:function(){
	params = {"name":"Submit",
		  "description":"A sequence for CRISPR design and analysis."
		 }
	this.$el.html(_.template(this.template, params)).attr("id","submit")
	return this
    },
    on_server_error:function(data){
	console.log("unexpected server error.")
    },


})
 





