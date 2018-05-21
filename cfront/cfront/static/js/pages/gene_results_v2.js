

var genes
function init_page(){

    function get_data(){
	$.get("/v2/"+sessionInfo.assembly+"/"+sessionInfo.geneid+"/job.json",
	      function(data){
		  if (data){
		      sessionInfo.data = data
		      init_with_data()
		  } else{
		      window.setTimeout(get_data, 1000)
		  }
	      })
    }

    function init_with_data(){
	var sview = new GeneResultsV2V()
	$('#gene_results_v2-container').empty().append(sview.render().$el)
    }

    if (sessionInfo.data == null)
    {
	$("#gene_results_v2-container").html(
	    _.template($("#results-waiting-template").html())({"location":window.location})
	)
	get_data()
    } else{
	init_with_data()
    }
    
 

    
    $(document).on("click",".highlight.guide",
		   function(ev){
		       console.log("CLICKING")
		       $e = $(ev.currentTarget)
		       console.log($e)
		       //target = $e.attr('target')
		       guide_sequence=$e.attr("guide_sequence")

		       targets = [ "#spacer-mid-margin-"+guide_sequence,
				   "#spacer-margin-"+guide_sequence]
		       for (var i = 0; i < targets.length ; i++){
		       
			   $t = $(targets[i])
			   console.log($t)
			   is_highlighted = $t.hasClass("highlighted")
			   $t.toggleClass("highlighted",!is_highlighted)
		       }
		   })
    
}
   

function get_selected_spacers(tool){
    max_spacers = 500;

    data = sessionInfo.data
    console.log(tool)
    spacers_data = data[tool].exonic_spacers
    spacers_sorted = _.sortBy(spacers_data,"score")
    spacers_sorted.reverse()
    selected_spacers = spacers_sorted.slice(0,max_spacers)
    return selected_spacers

}

function get_exons(){
    data = sessionInfo.data
    exons = data.exons
    return exons
}


function render_letters_html(sequence){

    console.log("seq len "+ sequence.length)
    matches = []
    var tools = ["cas9", "cpcf1"]
    for (var j =0 ; j<tools.length; j++){
	tool = tools[j]

	pam_before_decompiled = tool=="cas9"?"":"TT[ATGC]";
	pam_after_decompiled = tool=="cas9"?"[ATGC]GG":"";
	
	spacers = get_selected_spacers(tool)
	for (var i = 0 ; i < spacers.length ; i++){
	    guide= spacers[i].guide_sequence
	    fwd_regex = RegExp(pam_before_decompiled+"("+guide+")"+pam_after_decompiled)
	    m1 = fwd_regex.exec(sequence);
	    if (m1==null){continue}
	    m1.tool=tool
	    m1.id = spacers[i].id
	    m1.pam_before=spacers[i].pam_before
	    m1.pam_after=spacers[i].pam_after
	    m1.score=spacers[i].score
	    m1.guide_sequence = spacers[i].guide_sequence
	    matches.push(m1)
	}
    }
    
    matches = _.sortBy(matches,"start")
    html_output = ""
    pointer = 0
    exon_pointer=0
    exons = get_exons()
    in_exon = null

    gene_start = sessionInfo.gene_info.start
    
    spacer_starts = _.map(matches,function(m,i){
	return [m.index,{type:"spacer_start",
			 data:m}]
    })
    spacer_ends = _.map(matches,function(m,i){
	return [m.index + m[1].length,{type:"spacer_end",
				       data:m}]
    })
    exon_starts = _.map(exons,function(e,i){
	return [e.start -gene_start, {type:"exon_start",
			  data:e}]
    })
    exon_ends = _.map(exons,function(e,i){
	return [e.end - gene_start , {type:"exon_end",
			data:e}]
    })

    merged_transitions = exon_starts.concat(spacer_starts).concat(spacer_ends).concat(exon_ends)
    
    all_transitions = _.sortBy(merged_transitions,
			    function(e1){
			       srtval =  e1[0]
			       if( e1[1].type=="exon_start" ){srtval-=.1}
				if( e1[1].type=="exon_end" ){srtval+=.1}
				return srtval
			    })
    all_transitions.reverse()

    all_transitions_copied = all_transitions.slice(0,all_transitions.length)
    
    
    while (all_transitions.length >0){
	
	transition = all_transitions.pop()
	if( transition[1].type=="exon_start" || transition[1].type=="exon_end"){continue}
	s = transition[0]
	dist = s - pointer
	html_output += sequence.slice(pointer,pointer + dist)

	if (transition[1].type=="exon_start"){
	    html_output+= '</span><span class="exon" id="exon-'+transition[1].data.id+'"><div class="exon-helper">exon '+transition[1].data.id+'</div>'
	} else if (transition[1].type=="exon_end"){
	    html_output+= '</span><span class="intron">'
	} else if (transition[1].type=="spacer_start"){
	    html_output+='<span score="'+transition[1].data.score+'"  spacer_id="'+transition[1].data.id +'" pam_before="'+(transition[1].data.pam_before  ? transition[1].data.pam_before : "") +'" target="#spacer-margin-'+transition[1].data.guide_sequence+'"  pam_after="'+(transition[1].data.pam_after  ? transition[1].data.pam_after : "")+'" guide_sequence="'+transition[1].data.guide_sequence+'" class="guide highlight '+transition[1].data.tool+'"><a class="white" >'
	} else if (transition[1].type=="spacer_end"){
	    html_output+='</a></span>'
	}
	pointer += dist
    }

    
    
    return html_output
}


var GeneResultsV2V = Backbone.View.extend({
    template:$("#gene-results-v2-section-template").html(),
    className:"scrolly-section",
   
    render:function(){
	genome_info = sessionInfo.genome_info
	gene_info = sessionInfo.gene_info


	data = sessionInfo.data
	status = sessionInfo.status
	
	params = {"name":"Gene Query Results",
		  "description":"Query results for "+ gene_info.Name,
		  "genome_name":genome_info["name"],
		  "genome_assembly":genome_info["assembly"],
		  "gene_info":gene_info,
		  "data":data,
		  "status":status  
		 }

	
	this.$el.html(_.template(this.template, params)).attr("id","gene_results_v2")
	self = this;
	this.$el.find(".genome-name").text(genome_info["name"])
	this.$el.find(".genome-assembly").text(genome_info["assembly"])

	for( var i = 0; i < 2; i++){
	    tool = ["cas9","cpcf1"][i]
	    $spacerlist = this.$el.find("."+tool).find(".spacer-list")
	    selected_spacers = get_selected_spacers(tool)
	    for (var j = 0; j < selected_spacers.length; j++){
		spacer = selected_spacers[j]
		$spacerlist.append(
		    $("<li>").html(_.template($("#spacer-oneline-result-template").html())(
			{"guide_sequence":spacer.guide_sequence,
			 "pam_before":spacer.pam_before?spacer.pam_before:"",
			 "pam_after":spacer.pam_after?spacer.pam_after:"",
			 "score":spacer.score?spacer.score:"",
			})).attr("id","spacer-oneline-"+spacer.guide_sequence)
		)
	    }
	}

	letters_html = render_letters_html(sessionInfo.seq_letters)
	this.$el.find(".gene-view .letters").html(letters_html)

	this.$el.find(".letters .intron").each(
	    function(i,e){
		$e = $(e)
		letters = $e.text()

		console.log(e)
		console.log(letters.length)
		
		if (letters.length <=160 ){
		    return
		} else{
		    firstline = letters.slice(0,60)
		    lastline = letters.slice(-60)
		    middle = letters.slice(60,-60)
		    $e.html("").append($("<span>",{"class":"firstline"}).text(firstline))
			.append($("<span>",{"class":"before-middle"}).text("..."))
			.append($("<span>",{"class":"middle"}).text(middle))
			.append($("<span>",{"class":"before-middle"}))
			.append($("<span>",{"class":"lastline"}).text(lastline))
		    
		}
	    }
	);
	this.$el.find(".letters .guide").each(
	    function(i,e){
		console.log(e)
		pam_before= $(e).attr("pam_before") ? $(e).attr("pam_before") : "";
		pam_after = $(e).attr("pam_after") ? $(e).attr("pam_after") : "";
		score = $(e).attr("score") ? $(e).attr("score") : "??";
		spacer_id = $(e).attr("spacer_id")
		gene_id = sessionInfo.gene_info.id
		assembly = sessionInfo.assembly
		guide_sequence = $(e).attr("guide_sequence")
		
		$(e).append(
		    $('<div class="margin-spacer hidden-xs">')
			.html(_.template($("#spacer-oneline-result-template").html())(
			    
			    {"guide_sequence":guide_sequence,
			     "pam_before":pam_before,
			     "pam_after":pam_after,
			     "score":score,

			    }))
			.attr("id","spacer-margin-"+guide_sequence)
			.append($('<div class="download-gb">')
				.append($('<a>',{"href":'/v2/'+assembly+'/'+gene_id+'/'+"cas9"+'/'+guide_sequence+'/gene.gb'}).text("download as genbank"))
			       )
		).append(
		    $('<div class="text-spacer hidden-sm hidden-md hidden-lg">')
			.html(_.template($("#spacer-oneline-result-template").html())(
			    
			    {"guide_sequence":guide_sequence,
			     "pam_before":pam_before,
			     "pam_after":pam_after,
			     "score":score,

			    }))
			.attr("id","spacer-mid-margin-"+guide_sequence)
			.append($('<div class="download-gb">')
				.append($('<a>',{"href":'/v2/'+assembly+'/'+gene_id+'/'+"cas9"+'/'+guide_sequence+'/gene.gb'}).text("download as genbank"))
			       )
		)
		
			       
				
		
	    }
	)

	   
	
	return this
    },
    
})
