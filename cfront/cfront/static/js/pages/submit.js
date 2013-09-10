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
	_.each(this.$el.find('form'),
	       $.proxy(function(e,i){
		   var $form= $(e)
		   console.log($form)
		   $form.submit(
		       $.proxy(function(a,b){
			   var self = this;
			   var content, url;

			   if($form.attr("name") == "submit-fasta"){
			       url = routes.route_path("jobs_from_fasta")
			       console.log("setting up from FA")
			       content = new FormData($form[0]);
			       form_opts = {
				   cache: false,
				   contentType: false,
				   processData: false,
			       }
			   } else {
			       content = {}
			       _.each($form.serializeArray(),
				      function(e){
					  content[e.name] = e.value;
				      });
			       url = routes.route_path("job_post_new")
			       form_opts = {
				   dataType:"json",
			       }
			   }		
			   
			   ajax_opts = {
			       data:content,
			       //Options to tell jQuery not to process data 
			       //or worry about content-type.
			       url:url,
			       type:"POST",
			       success:$.proxy(function(data){
				   if (data.status == "success"){
				       if(data.job_key != null){
					   window.location.assign(
					       routes.route_path("readout",
								 {job_key:data.job_key}))

				       } else if( data.batch_key != null){
					   window.location.assign(
					       routes.route_path("batch",
								 {batch_key:data.batch_key}))
				       } else {
					   alert ("something unexpected seems to have gone wrong. this should be fixed!")
				       }
				       
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
			   }
			   
	   
			   $form.addClass("submitted")
			   $.ajax(_.extend(form_opts,ajax_opts))
			   return false

		       }, this)
		   )
	       },this))
	    },
    render:function(){
	params = {"name":"Submit",
		  "description":"Submit a single sequence for CRISPR design and analysis."
		 }

	this.$el.html(_.template(this.template, params)).attr("id","submit")

	self = this;
	genome_names = sessionInfo.genome_names
	descriptive_names = {hg19:"human", mm9:"mouse", danRer7:"zebrafish", rn5:"rat",  ce10:"c. elegans"}

	control_template =  $("#genome-control-template").html()
	_.each(this.$(".genome-controls"),
	       function(controls){
		   $controls = $(controls)
		   _.each(genome_names,function(g, i){
		       params = {name:g,
				 checked_string: i == 0 ? "checked" : "",
				 descriptive_name:descriptive_names[g]}
		       $controls.append(
			   $("<label>",{class:"radio genome"}).html(
			       _.template(control_template,params)))
		   });
	       }
	      );
	return this
    },
    on_server_error:function(data){
	console.log("unexpected server error.")
    },


})
 





