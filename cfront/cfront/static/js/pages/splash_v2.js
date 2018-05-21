
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


	_.each(_.sortBy(genomes_info, "name"),
	       function(e,i){
		   if(e.name !="human"){
		       self.$el.find("#genome-v2-links").append(
			   $("<li>").html(_.template($("#splash-genome-link").html())(e))
		       )
		   }else{
		       self.$el.find("#genome-v2-links").prepend(
			   $("<li>",{"class":"human"}).html(_.template($("#splash-genome-link").html())(e))
		       )
		   }
	       });
	      
	    
	return this
    },
    on_server_error:function(data){
	console.log("unexpected server error.")
    },

    
})
