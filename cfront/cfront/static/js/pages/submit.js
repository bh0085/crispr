//scripts powering submission
function submit_read_input(){
    submit = new JobM({
	sequence: $("#sequence_submission_area").val().toUpperCase()
    });
    submit.save(null,
		{success:$.proxy(function(e){
		    this.compute_spacers();
		},submit)})
};
