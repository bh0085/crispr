//scripts powering submission
function submit_read_input(){
    submit = new JobM({
	sequence: $("#sequence_submission_area").val().toUpperCase()
    });
    submit.save(null,
		{success:$.proxy(function(e){
		    this.await_hits()
		    this.await_spacers()
		},submit)})
};

