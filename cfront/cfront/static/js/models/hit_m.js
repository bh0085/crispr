/** backbone model for a hit */
var HitM = Backbone.RelationalModel.extend({
    id:null,
    ontarget:null,
    similarity:null,
    chr:null,
    start:null,
})


var HitC = Backbone.Collection.extend({
    model:HitM,
    url:function(a,b){
	throw "not yet implemented"
    }
})
