/** backbone model for a hit */
var HitM = Backbone.RelationalModel.extend({
    defaults:{
	ontarget:null,
	similarity:null,
	chr:null,
	start:null,
	gene:"NA",
	score:-1}
})


var HitC = Backbone.Collection.extend({
    model:HitM,
    url:function(a,b){
	throw "not yet implemented"
    }
})
