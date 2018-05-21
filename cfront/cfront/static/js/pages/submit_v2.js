

function render_gene_suggestion(){
    return _.template($("#typeahead-gene-suggestion-template").html())({"name":"GENE"})
}


var genes
function init_page(){
    var sview = new SubmitV2V()
    $('#submit_v2-container').append(sview.render().$el)
    function activate_gene_helpers(value){
	$(".download-gb").attr("href", "/v2/"+genome_info["assembly"]+"/"+value+"/gene.gb")
	$(".download-fa").attr("href", "/v2/"+genome_info["assembly"]+"/"+value+"/gene.fa")
	$(".gene-helpers").removeClass("hidden")
    }


    $(".updates-target").change(function(ev){
	console.log($(this).val())
	$("#submit-form").attr("target","/v2/"+genome_info["assembly"]+"/"+$("#gene_id_value").val()+"/"+$("#email-address").val()+"/query_gene")
	
    })
    
    $("#submit-form").submit(function(ev){
	$.post($(this).attr("target"), {} ,function(data){
	    window.location.replace("/v2/"+genome_info["assembly"]+"/"+$("#gene_id_value").val()+"/gene_results" );
	    
	})
	return false
    })
    
    $(".toggle-gene-info").on("click",function(){
	$(".gene-info-container").toggleClass("hidden",!$(".gene-info-container").hasClass('hidden'))
    })
    
    $("#prefetch .typeahead").selectize(
	{create: false,
	 valueField: 'id',
	 labelField: 'name',
	 searchField:'name',
	 maxItems:1,
	 maxOptions:100,
	 closeAfterSelect:true,
	 onItemAdd:function(value,$item){
	     matches = _.filter(sessionInfo.gene_infos,function(e){return e.id==value})
	     datum = matches[0]
	     //$(".gene-info").html(_.template($("#gene-info-template").html())(datum))
	     $.getJSON("/v2/"+genome_info["assembly"]+"/"+value+"/genbank.json",{},function(data){$(".gene-info").text(data)})
	     $("#gene_id_value").val(value)
	     $("#gene_id_value").change()
	     activate_gene_helpers(value)
	 },
	 options:sessionInfo["gene_infos"]})   
}
   



var SubmitV2V = Backbone.View.extend({
    template:$("#submit-v2-section-template").html(),
    className:"scrolly-section",
   


    render:function(){
	genome_info = sessionInfo.genome_info

	params = {"name":"Submit V2",
		  "description":"Knock out a target gene.",
		  "genome_name":genome_info["name"],
		  "genome_assembly":genome_info["assembly"]
		  
		 }

	
	this.$el.html(_.template(this.template, params)).attr("id","submit_v2")
	self = this;
	this.$el.find(".genome-name").text(genome_info["name"])
	this.$el.find(".genome-assembly").text(genome_info["assembly"])

	
	return this
    },
    
})
