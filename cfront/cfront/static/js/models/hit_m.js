/** backbone model for a hit */
var HitM = Backbone.RelationalModel.extend({
    defaults:{
	ontarget:null,
	similarity:null,
	chr:null,
	start:null,
	gene:null,
	score:-1},
    initialize:function(){
	this.set("locus",this.locus());
	this.set("mismatches",this.mismatches());
    },
    locus:function(){
	//sprintf('%6s:%s%d',data.chr, data.strand == 1 ? "+" : "-", data.start)
	
	loc =  this.get("chr") +":"+ (this.get("strand") == -1?"-":"+")
		+ (this.get("start") + (this.get("strand") == 1?-1:-4))
	loc += Array(18 - loc.length).join("&nbsp;")
	return loc
    },
    mismatches:function(){
	guide_seq = this.get("spacer").get("sequence")
	diffs = []
	for(var i = 0 ; i < 20 ; i++){
	    if( guide_seq[i] != this.get("sequence")[i]){diffs.push(i+1)}
	}
	return diffs.join(":")
    }
})


var HitC = Backbone.Collection.extend({
    model:HitM,
    url:function(a,b){
	throw "not yet implemented"
    }
})
