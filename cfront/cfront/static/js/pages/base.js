//basic setup for the crispr app

_.templateSettings = {
  interpolate : /\{\{(.+?)\}\}/g
};

//data structures for app state
submit_data_proto = {
    input_sequence:null
}
identify_data_proto = {
    spacers:null, /** list -- each query include an "id", "seq", "strand", "offset" **/
    collisions:null /** obj -- stores collisions of spacers sorted along strand **/
}
find_data_proto = {
    hits:null /** list -- each hit includes a query id, a hitid, a sequence (from DB) **/
}

//instances
find_data = _.extend(find_data_proto)

section_names=["submit","identify","find"]


//fills in a section when THE previous section is passed 
function initialize_scrolly_section(name){
    if (name == "submit"){
	//no intialization required
    } else if( name == "identify"){
	//assumes we have a submitted sequence
	submit_read_input();
	//reads the sequence
	identify_sequence();
    } else {
	//finds the sequence by submitting jobs to db
	find_initialize();

	
    }
}

//resets a section when a _previous_ section is focused
function reset_scrolly_section(name){
    params = {"find":{"name":"Find",
		      "description":"off-target binding sites in the genome."},
	      "identify":{"name":"Identify",
			  "description":"candidate spacers within the input sequence."},
	      "submit":{"name":"Submit",
			"description":"a query sequence to ID and characterize spacers."}
	     }
    $("#" + name).html(
	_.template($("#scrolly-section-template").html(),
		   params[name]))

    if (name == "submit"){
	$('#submit>.scrolly-content').html($("#submit-section-template").html())
	submit_data = null;
	submit_data = _.extend(submit_data_proto)
    } else if(name=="identify"){
	$('#identify>.scrolly-content').html($("#identify-section-template").html())
	identify_data = null;
	identify_data = _.extend(identify_data_proto)
    } else if(name =="find"){
	$('#focus>.scrolly-content').html($("#focus-section-template").html())
	find_reset();
	find_data = null;
	find_data = _.extend(find_data_proto);
    }
}


//focus on a section. blurs others.
function focus_scrolly_section(name){

    index = section_names.indexOf(name)
    for (var i = index + 1 ; i < section_names.length ; i++){
	reset_scrolly_section(section_names[i])
    }
    initialize_scrolly_section(name)
    $(".scrolly-section").addClass("inactive");
    $("#"+name).removeClass("inactive");
    smoothscroll(name);
}

//init script to reset all sections filling in templates.
$(function(){
    _.each($(".scrolly-section"),function(e,i){
	reset_scrolly_section(e.id);
    });
    focus_scrolly_section("submit");
})

//defines clickhandlers
$(function(){
    //next clickhandlers
    $("#submit .next").click(function(event){
	focus_scrolly_section("identify");	
    });
    $("#identify .next").click(function(event){
	focus_scrolly_section("find");
    });
    //previous clickhandlers
    $("#identify .previous").click(function(event){
	focus_scrolly_section("submit");
    });
    $("#find .previous").click(function(event){
	focus_scrolly_section("identify");
    });
})

//smooth scrolls to make everything look pretty
function smoothscroll(name){
    event.preventDefault();
    //calculate destination place
    var desired_top=$("#" + name).offset().top - 50;
    var dest=0;
    
    if(desired_top < 0){
	dest = 0;
    } else if(desired_top > $(document).height()-$(window).height()){
        dest=$(document).height()-$(window).height();
    }else{
        dest=desired_top;
    }
    //go to destination
    $('html,body').animate({scrollTop:dest}, 400,'swing');
}
