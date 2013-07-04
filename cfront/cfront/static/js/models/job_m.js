/** backbone model for a job */
var JobM = Backbone.Model.extend({
    relations:[
	{
	    key:"spacers",
	    type:Backbone.HasMany,
	    relatedModel:"SpacerM",
	    includeInJSON:false,
	    reverseRelation:{
		key:job,
		keySource:"jobid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	}
    ]
})

/** backbone model for a spacer */
var SpacerM = Backbone.RelationalModel.extend({
    relations:[
	{
	    key:"hits",
	    type:Backbone.HasMany,
	    relatedModel:"HitM",
	    includeInJSON:false,
	    reverseRelation:{
		key:job,
		keySource:"spacerid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	}
    ]
})

/** backbone model for a hit */
var HitM = Backbone.RelationalModel.extend({

})
