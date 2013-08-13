function init_page(){
    //next clickhandlers
    $(document).on("click", "#submit .next",{},function(event){
	submit_read_input();
    });
    var sview = new SubmitV()
    $('#submit-container').append(sview.render().$el)
    sview.configureForm()
}

$(document).on("click", ".show-example", function(){
    $("#sequence_submission_area").text("GAACTTACCTGGTTAGTTAGAGG DYRK1A_23\n"+
"GGAGTATCAGAAATGACTATTGG DYRK1A_24\n"+
"GGTCACTGTACTGATGTGAATGG DYRK1A_25\n") 
})

$(document).on("click", ".show-genome-example", function(){
    $("#sequence_submission_area").text("GGAGCTGCAGGGACCTCCATGTCCTGGGACTGTTTGTGCAGGGCTCCGAGGGGACCCATGTGGCTCAGGGTGGCTAAGGGGGCAATGCTGCCCCCACCCGCTGGATGAC") 
})

$(document).on("click", ".show-other-example", function(){
    $("#sequence_submission_area").text("GTCGCTCGTCGGAGCTGCAGGGACCGGCGCGAGCGAGTGCTGGACTGTTTGTGCAGGGCTCCGAGGGGACCCATGTGGCTCAGGGTGGCTAAGGGGGCAATGCTGCGTCGTCGTAGTTTTTTGGGGG") 
})

$(document).on("click", "#sequence_submission_area",function(){
    $(this).focus()
    $(this).select()
})


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

		if(content["inputRadios"] == "guides_list"){
		    url = routes.route_path("job_from_spacers")
		} else {
		    url = routes.route_path("job_post_new")
		}
		
		$form.addClass("submitted")

		$.ajax({
		    dataType:"json",
		    data:content,
		    url:url,
		    type:"POST",
		    success:$.proxy(function(data){
			if (data.status == "success"){
			    if(data.job_key == null){throw "hi"}
			    window.location.assign("http://" + location.host + "/job/" + data.job_key)
			} else {
			    $form.removeClass("submitted");
			    alert(data.message);
			}
			return false
		    },this), 
		    error:$.proxy(function(data){
			this.on_server_error()
			$form.removeClass("submitted")
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
 





