//scripts powering find

var find_statuses = null
var find_current_id = 0
var find_polling_delay = null;

function find_initialize(){
    
    queries = _.map(identify_data.spacers,function(e){return e.seq});
    if (queries.length == 0){throw exceptions.nospacers.messages}
    
    
    _.each(queries,function(s,i){
	$.getJSON("/find/submit/"+s,
		  {},
		  $.proxy(function(data){
		      find_statuses[data.job_id] = data.status
		      window.setTimeout(
			  $.proxy(find_check_job,{
			      job_id:data.job_id}),250)
		  }),{sequence:s})
    });
}

function find_reset(){
    //sets states to default values
    find_statuses = {}
    //offsets the current_id so that outdated asynch calls will be ignored
    find_current_id += 1
    find_polling_delay = 250
}


function find_check_job(){
    //outdated async process
    if(this.find_id < find_current_id){return;}
    
    //checks on the job and submits a new timeout if needbe
    $.getJSON("/find/check/"+this.job_id,
	      {},
	      $.proxy(function(result){
		  console.log(this.job_id, result)
		  if (result != "DONE"){
		      window.setTimeout($.proxy(find_check_job,this),500)
		  }
	      },this))
}
	   

	   
	   
	  
