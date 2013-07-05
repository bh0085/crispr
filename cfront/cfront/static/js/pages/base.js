//basic setup for the crispr app

Backbone.emulateHTTP = true;

_.templateSettings = {
  interpolate : /\{\{(.+?)\}\}/g
};


exceptions = {
    nospacers:{"message":"no spacers in input sequence"}
}

section_names=["submit","readout"]


//fills in a section when THE previous section is passed 
function initialize_scrolly_section(name){
    if (name == "submit"){
	//no intialization required
    } else if( name == "readout"){
	//assumes we have a submitted sequence
	submit_read_input();
	//reads the sequence
	initialize_readout();
    } 
}

//resets a section when a _previous_ section is focused
function reset_scrolly_section(name){
    params = {"submit":{"name":"Submit",
			"description":"A sequence for CRISPR design and analysis."},
	      "readout":{"name":"Readout",
			 "description":"Best possible guide sequences."}
	     }
    $("#" + name).html(
	_.template($("#scrolly-section-template").html(),
		   params[name]))

    if (name == "submit"){
	$('#submit>.scrolly-content').html($("#submit-section-template").html())
	submit = null;
    } else if(name=="readout"){
	$('#readout>.scrolly-content').html($("#readout-section-template").html())
	//console.log("no more data readout objects");
	//readout_data = null;
	//readout_data = _.extend(readout_data_proto)
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
    $(document).on("click", "#submit .next",{},function(event){
	focus_scrolly_section("readout");	
    });
    //previous clickhandlers
    $(document).on("click","#readout .previous",{},function(event){
	focus_scrolly_section("submit");
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
