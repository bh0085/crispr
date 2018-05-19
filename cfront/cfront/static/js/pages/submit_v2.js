

var substringMatcher = function(strs) {
          console.log("outer func!!")

    return function findMatches(q, cb) {
	
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push(str);
      }
    });

            console.log("trying!!")

      cb(matches);
  };
};


function render_gene_suggestion(){
    return _.template($("#typeahead-gene-suggestion-template").html())({"name":"GENE"})
}


var genes
function init_page(){
    var sview = new SubmitV2V()
    $('#submit_v2-container').append(sview.render().$el)

    genes = new Bloodhound({
	datumTokenizer: function(datum){return [datum.name]},
	queryTokenizer: Bloodhound.tokenizers.whitespace,
	// url points to a json file that contains an array of country names, see
	// https://github.com/twitter/typeahead.js/blob/gh-pages/data/countries.json
	local:sessionInfo["gene_infos"]
    });
    
    
    // passing in `null` for the `options` arguments will result in the default
    // options being used
    $('#prefetch .typeahead').typeahead({
	hint: true,
	highlight: true,
	minLength: 1
    }, {
	limit: 100,
	name: 'genes',
	source:genes,
	display:function(datum){return datum.name },
	templates:{suggestion:function(data) {
    return '<p><strong>' + data.name + '</strong> – ' + data.chrom + '</p>';
	}}
    }).bind('change blur', function () {
    // custom function for check existing value in listing
    match = false
    for (var i = sessionInfo["gene_infos"].length - 1; i >= 0; i--) {
        if ($(this).val() == sessionInfo["gene_infos"][i].name) {
            match = true;
        }
    }
    if (!match) {
        $(this).val('');
    }
});;




    $('.typeahead').bind('typeahead:select', function(ev, suggestion) {
	console.log("selecting")
	$(".gene-info").html(_.template($("#gene-info-template").html())(suggestion))
	$("#gene_id_value").val(suggestion.id)
    });

    $('.typeahead').bind('typeahead:cursorchange', function(ev, suggestion) {
	console.log("cursor changing")
	$(".gene-info").html(_.template($("#gene-info-template").html())(suggestion))
	$("#gene_id_value").val(suggestion.id)
    });
    
    
    //init_typeahead()
    
}


    







var SubmitV2V = Backbone.View.extend({
    template:$("#submit-v2-section-template").html(),
    className:"scrolly-section",
   


    render:function(){
	params = {"name":"Submit V2",
		  "description":"Knock down or knock out a gene or genomic locus."
		 }

	this.$el.html(_.template(this.template, params)).attr("id","submit_v2")

	self = this;
	genome_info = sessionInfo.genome_info
	console.log(genome_info["name"])
	this.$el.find(".genome-name").text(genome_info["name"])
	this.$el.find(".genome-assembly").text(genome_info["assembly"])

	return this
    },
    on_server_error:function(data){
	console.log("unexpected server error.")
    },

    
})
