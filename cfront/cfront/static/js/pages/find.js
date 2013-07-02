//scripts powering find

var find_current_id = 0
var find_polling_delay = null;
var find_results = []


function find_initialize(){
    
    queries = _.map(identify_data.spacers,function(e){return e.seq});
    if (queries.length == 0){throw exceptions.nospacers.messages}
    
    console.log("LOGGING FIND")
    console.log(queries.length)
    _.each(queries,function(s,i){
	$.getJSON("/find/submit/"+s,
		  {},
		  $.proxy(function(data){
		      var sm = new SpacerM({
			  sequence:this.sequence,
			  status:data.status,
			  job_id:data.job_id,
			  find_id:find_current_id,
		      })
		      
		      var sv = new SpacerOffTargetsV({model:sm})
		      sv.render().$el.appendTo($("#find"))
		      window.setTimeout($.proxy(find_check_job,sm),250)
		  }),{sequence:s})
    });
}

function find_reset(){
    //sets states to default values
    //offsets the current_id so that outdated asynch calls will be ignored
    find_current_id += 1
    find_polling_delay = 250
};


function find_check_job(){
    //outdated async process
    if(this.get("find_id") < find_current_id){
	this.destroy();
	return
    }
    
    //checks on the job and submits a new timeout if needbe
    $.getJSON("/find/check/"+this.get("job_id"),
	      {},
	      $.proxy(function(result){
		  
		  if (result == "DONE"){
		      $.getJSON("/find/retrieve/"+this.get("job_id"),
				{},
				$.proxy(this.retrieveHitsJSON,this))
		  } else if (result == "RUN") {
		      window.setTimeout($.proxy(find_check_job,this), find_polling_delay+=250)
		  } else if (result == "FAILED") {
		      throw "fucked!"
		  }
	      },this))
    
    
}
	   

	   
	   
	  
