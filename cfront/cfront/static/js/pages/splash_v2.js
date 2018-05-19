
function init_page(){
    var sview = new SplashV2V()
    $('#splash_v2-container').append(sview.render().$el)
}

var SplashV2V = Backbone.View.extend({
    template:$("#splash-v2-section-template").html(),
    className:"scrolly-section",

    render:function(){
	params = {"name":"Splash",
		  "description":"Choose a Crispr workflow."
		 }

	this.$el.html(_.template(this.template, params)).attr("id","splashV2")

	self = this;
	genomes_info = sessionInfo.genomes_info

	control_template =  $("#genome-control-template").html()
	_.each(this.$(".genome-controls"),
	       function(controls){
		   $controls = $(controls)
		   _.each(genomes_info,function(g, i){
		       params = {name:g["assembly"],
				 checked_string: i == 0 ? "checked" : "",
				 descriptive_name:g["name"]}
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
