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
