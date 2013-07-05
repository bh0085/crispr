//scripts powering submission
function submit_read_input(){
    submit = new JobM({
	sequence: $("#sequence_submission_area").val().toUpperCase()
    });
    submit.save({},
		function(e){
		    console.log("hi");
		    console.log(this.toJSON());
		})
};
