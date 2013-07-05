/** backbone model for a job */
var JobM = Backbone.Model.extend({
    sequence:null,
    id:null,
    genome:null,
    name:null,
    email:null,
    date_submitted:null,
    date_completed:null,
    relations:[
	{
	    key:"spacers",
	    type:Backbone.HasMany,
	    relatedModel:"SpacerM",
	    includeInJSON:false,
	    reverseRelation:{
		key:"job",
		keySource:"jobid",
		includeInJSON:"id",
		type:Backbone.HasOne
	    }
	}
    ],
    /** Rest URL for a Job */
    url: function () {
        var id = this.id ? this.id : -1;
        var url = '/r/job/' + id;
        return url;
    },
})
