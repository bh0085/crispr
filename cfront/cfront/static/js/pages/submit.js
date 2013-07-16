$(function(){
    //next clickhandlers
    $(document).on("click", "#submit .next",{},function(event){
	submit_read_input();
    });


    init();
});
function init(){
    console.log("empty init for submit.js")
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
		    url:"/j/post_new",
		    type:"POST",
		    success:$.proxy(function(data){
			if (data.status == "success"){
			    if(data.job_id == null){throw "hi"}
			    window.location.assign("http://" + location.host + "/job/" + data.job_id)
			} else {
			    console.log("unhandled error:")
			    console.log(data)
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
	throw 'unimplemented';
    },


})
 





