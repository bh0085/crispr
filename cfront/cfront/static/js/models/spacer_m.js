/** backbone model for a spacer */
var SpacerM = Backbone.RelationalModel.extend({
    sequence:null,
    id:null,
    guide:null,
    strand:null,
    position:null,
    relations:[
	{
	    key:"hits",
	    type:Backbone.HasMany,
	    relatedModel:"HitM",
	    includeInJSON:false,
	    reverseRelation:{
		key:"spacer",
		keySource:"spacerid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	}
    ]
})


var SpacerC = Backbone.Collection.extend({
    model:SpacerM,
    url:function(a , b){
	console.log(this)
	console.log(this.id)
	console.log(a)
	console.log(b)
	throw hi
    }
})
