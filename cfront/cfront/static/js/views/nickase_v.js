
NickaseSVGV = JobSVGV.extend({
    template:$("#nickase-svg-view-template").html(),
    initialize:function(){
	this.binder = new Backbone.EventBinder();
    },
    render:function(){
	this.$el.html(_.template(this.template, {}))

	return this
    },
    register_listeners:function(){},
    initial_draw:function(){},
})



var N ={
    demo_score_consort:function(consort){
	var k = N.kernels.std
	
	//generates 200 random regions
	regions = [] 
	for (var i = 0 ; i < 200 ; i ++){
	    regions[i] =  _.map(_.range(200),function(){
		return "ATGC"[Math.floor(Math.random() * 4)]
	    }).join("")
	}

	scores = _.map(regions,
		       function(r){
			   return k(consort, r)
		       })
	return scores
	
    },
    kernels:{
	std:function(consort, region){
	    l = consort.length
	    sims = 
		_.map(_.range(region.length - l),
		      function(i){
			  return _.reduce(
			      _.range(l), 
			      function(cur, j){
				  return cur + (consort[i] == region[j+i]?1:0)
			      })//ends box_smoothing
		      })//ends scan, returning max similarity of "l" bases in region
	    return _.max(sims)
	},
    },
}

