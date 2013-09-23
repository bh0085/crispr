function init_page(){
    var aview = new AboutV()
    $('#about-container').append(aview.render().$el)
}

var AboutV = Backbone.View.extend({
    template:$("#about-section-template").html(),
    className:"scrolly-section",
    render:function(){
	params = {}
	this.$el.html(_.template(this.template, params))
	return this
    },
    on_server_error:function(data){
	console.log("unexpected server error.")
    },
})
				  





