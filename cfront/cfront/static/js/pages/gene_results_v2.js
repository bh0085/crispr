
var GeneResultsV2V = Backbone.View.extend({
    template:$("#gene-results-v2-section-template").html(),
    className:"scrolly-section",
   
    render:function(){
	genome_info = sessionInfo.genome_info
	gene_info = sessionInfo.gene_info
	data = sessionInfo.data
	status = sessionInfo.status
	
	params = {"name":gene_info.Name+ " KNOCKOUT GUIDE",
		  "genome_name":genome_info["name"],
		  "genome_assembly":genome_info["assembly"],
		  "gene_info":gene_info,
		  "data":data,
		  "status":status ,
		  "assembly":genome_info["assembly"],
		  "geneid":sessionInfo.geneid,
		  "gene_name":gene_info["Name"][0],
		 }
	
	this.$el.html(_.template(this.template, params)).attr("id","gene_results_v2")
	self = this;
	this.$el.find(".genome-name").text(genome_info["name"])
	this.$el.find(".genome-assembly").text(genome_info["assembly"])
	rerender_letters(this)
	return this
    },
    
})


x1=0
x2=1000
r1=null
r2=null
exon_elts = []
selection_start = null
selection_end = null
letters_timer = null
max_spacers = 20
min_per_guide = 5
selection_timer = null
exon_line = null
exon_select_line = null

draw = null


function draw_svg(){

    var slider = document.getElementById('slider');

    noUiSlider.create(slider, {
	start: [0, sessionInfo.seq_letters.length],
	connect: true,
	margin:50,
	step:1,
	range: {
	    'min': 0,
	    'max': sessionInfo.seq_letters.length
	}
    });


    //globals
    svg_w = 600
    svg_h = 100
    svg_margin = 0
    svg_inner_w = svg_w - svg_margin *2
    svg_exon_y = 75
    letters = sessionInfo.seq_letters
    
   
    draw = SVG('drawing').size(svg_w, svg_h)

   
    exons = get_exons()
    exon_line = draw.line(svg_margin, svg_exon_y, svg_w - svg_margin, svg_exon_y).stroke({ width: .5 })
    exon_elts = _.map(exons,function(e){
	left = transform_exon_x(e.start)
	right = transform_exon_x(e.end)
	return draw.rect( right - left, 10).move(left,svg_exon_y-5)
	
    })

    slider.noUiSlider.on("update",function(vals,handle){
	r1 = Number(vals[0])
	r2 = Number(vals[1])
	selection_changed()
    })
    
    

}

function selection_changed(){

    $(".range-start").text(r1)
    $(".range-end").text(r2)
    
    selection_start =  r1
    selection_end = r2

    seq = sessionInfo.seq_letters
    slice_start = selection_start - 10
    if( slice_start <0){
	
	init_slice = seq.slice(0,selection_start + 10)
	for (var i = 0 ;  i< -1* slice_start; i++){
	    init_slice="-"+init_slice
	}
    } else{
	init_slice = seq.slice(slice_start,selection_start + 10)
    }

    slice_end = selection_end + 10
    if( slice_end >seq.length){
	
	end_slice = seq.slice(selection_end-10,seq.length)
	for (var i = 0 ;  i< slice_end - seq.length; i++){
	    end_slice=end_slice+"-"
	}
    } else{
	end_slice = seq.slice(selection_end - 10,slice_end)
    }
    

    n_exons = 0;
    exons = get_exons()
    for (var i = 0; i< exons.length; i++){
	elt = exon_elts[i]
	exon = exons[i]
	gene_start =  sessionInfo.gene_info.start

	if(exon.start-gene_start < selection_end && exon.end-gene_start > selection_start){
	    elt.attr({"class":"selected"})
	    n_exons+=1;
	} else{
	    elt.attr({"class":""})
	}

	    
    }
    $(".exon-count").text(n_exons)
    
    if( ! letters_timer){
	rerender_letters(rendered)
	letters_timer = window.setTimeout(function(){
	    letters_timer = null
	    rerender_letters(rendered)
	},500)
    }
    
    
    $("#hero-spacers").html($("#hero-spacers-table-template").html())
			    
    spacers = get_selected_spacers("all")
    for ( var i = 0 ; i < spacers.length ; i++){
	s = spacers[i]
	$("#hero-spacers").find("table").append($("<tr>").html(_.template($("#hero-spacer-template").html())(s)))
    }
    $(".start-base").text(selection_start)
    $(".end-base").text(selection_end)
    
}

function transform_exon_x(start){
    gene_start =  sessionInfo.gene_info.start
    seq_len = sessionInfo.seq_letters.length
    return ((start-gene_start) / seq_len)*svg_inner_w + svg_margin
}
function reverse_transform_exon_x(x){
    return Math.floor(((x - svg_margin) / svg_inner_w) * sessionInfo.seq_letters.length)
}

function rerender_letters(ctx){
	letters_html = render_letters_html(sessionInfo.seq_letters)
	ctx.$el.find(".gene-view .letters").html(letters_html)

	ctx.$el.find(".letters .intron").each(
	    function(i,e){
		$e = $(e)
		letters = $e.text()

		
		if (letters.length <=160 ){
		    return
		} else{
		    firstline = letters.slice(0,80)
		    lastline = letters.slice(-80)
		    middle = letters.slice(80,-80)
		    $e.html("").append($("<span>",{"class":"firstline"}).text(firstline))
			.append($("<span>",{"class":"before-middle"}).text("..."))
			.append($("<span>",{"class":"middle"}).text(middle))
			.append($("<span>",{"class":"before-middle"}))
			.append($("<span>",{"class":"lastline"}).text(lastline))
		    
		}
	    }
	);
	ctx.$el.find(".letters .guide").each(
	    function(i,e){
		pam_before= $(e).attr("pam_before") ? $(e).attr("pam_before") : "";
		pam_after = $(e).attr("pam_after") ? $(e).attr("pam_after") : "";
		score = $(e).attr("score") ? $(e).attr("score") : "??";
		spacer_id = $(e).attr("spacer_id")
		gene_id = sessionInfo.gene_info.id
		assembly = sessionInfo.assembly
		guide_sequence = $(e).attr("guide_sequence")
		
		$(e).append(
		    $('<div class="text-spacer">')
			.html(_.template($("#spacer-oneline-result-template").html())(
			    
			    {"guide_sequence":guide_sequence,
			     "pam_before":pam_before,
			     "pam_after":pam_after,
			     "score":score,

			    }))
			.attr("id","spacer-mid-margin-"+guide_sequence)
			.append($('<div class="download-gb">')
				.append($('<a>',{"target":"_blank","href":'/v2/'+assembly+'/'+gene_id+'/'+"cas9"+'/'+guide_sequence+'/gene.gb'}).text("download as genbank"))
			       )
		)
		
			       
				
		
	    }
	)

}
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
	rendered = sview.render()
	$rendered = rendered.$el
	$('#gene_results_v2-container').empty().append($rendered)
	draw_svg()
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

    $(document).on("change",".export-all",function(ev){
	$(".export").prop("checked",$(ev.currentTarget).prop("checked"))
	$("#download-selected").attr("href","/v2/"+sessionInfo.assembly+"/"+sessionInfo.geneid+"/selected_spacers.gb?"+$.param({ 'spacers' : JSON.stringify(_.map($(".export:checked"),function(e){return $(e).attr("name")})) }))
	$("#download-selected").toggleClass("disabled", $(".export:checked").length ==0)

    })

    
    $(document).on("change",".export",function(ev){
	$(".export-all").prop("checked",false)
	$("#download-selected").attr("href","/v2/"+sessionInfo.assembly+"/"+sessionInfo.geneid+"/selected_spacers.gb?"+$.param({ 'spacers' : JSON.stringify(_.map($(".export:checked"),function(e){return $(e).attr("name")})) }))
	$("#download-selected").toggleClass("disabled", $(".export:checked").length ==0)
	
    })

    $(document).on("change", ".show-details",
		   function(ev){
		       seq = $(ev.currentTarget).attr("guide_sequence")
		       
		       spacer = _.filter(get_selected_spacers("all"),function(e){
			   return e.guide_sequence==seq
		       })[0]
		       $("#spacer-details-container").html(
			   _.template($("#spacer-detail-view-template").html())(
			       {
				   "spacer":spacer,
				   "gene":sessionInfo.gene_info,
				   "assembly":sessionInfo.assembly
			       }))

		       for(var i = 0; i < spacer.offtarget_alignments.length; ++i) {
			   $("#spacer-details-container .ot-table-container").addClass('full')
			   var a = spacer.offtarget_alignments[i]
			   $("#spacer-details-container").find("table").append(_.template($("#offtarget-spacer-row-template").html())({"a":a}))
		       }
		       
		       $("#download-guide-gb").attr("href","/v2/"+sessionInfo.assembly+"/"+sessionInfo.geneid+"/"+spacer.tool+"/"+spacer.guide_sequence+"/guide.gb")
		       $("#download-guide-gb").toggleClass("disabled",false)
		   })
}
   

function get_selected_spacers(tool){
    data = sessionInfo.data

    if (tool=="all"){
	spacers_data = data["cas9"].spacers.concat(spacers_data = data["cpf1"].spacers)
    } else{
	spacers_data = data[tool].spacers
    }

    gene_start =  sessionInfo.gene_info.start

    selected_spacers = _.filter(spacers_data,
				function(s){
				    return (s.guide_start + s.region_start -gene_start) <selection_end && (s.guide_start + s.region_start - gene_start + s.guide_length)>selection_start; 
				})
    
    spacers_sorted = _.sortBy(selected_spacers,"score")
    spacers_sorted.reverse()

    var cas9_count = 0
    var cpf1_count=0
    var total_count =0

    // adds at least "min_per_guide" spacers of each type to the list.
    // maes out at max_spacers + min_per_guide * n-1
    selected_spacers =_.filter(_.map(spacers_sorted,function(e){
	if(e.tool == "cpf1"){
	    if( cpf1_count <min_per_guide){
		cpf1_count+=1
		total_count+-1
		return e
	    }
	} else{
	    if( cas9_count < min_per_guide){
		cas9_count+= 1
		total_count+=1
		return e
	    }
	}
	if(total_count <max_spacers){
	    total_count+=1
	    return e
	}
    }), function(e){return e!=null})
    
    //selected_spacers = spacers_sorted.slice(0,max_spacers)
    return selected_spacers

}

function get_exons(){
    data = sessionInfo.data
    exons = data.cas9.search_regions
    return exons
}


function render_letters_html(sequence){
    matches = []
    var tools = ["cas9", "cpf1"]
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
    all_transitions=[[0,{"type":"start",
			 "data":{}}]].concat( all_transitions)
    all_transitions = all_transitions.concat([[sequence.length,{"type":"end",
								"data":{}}]])
    
    all_transitions.reverse()
    all_transitions_copied = all_transitions.slice(0,all_transitions.length)
    
    while (all_transitions.length >0){	
	transition = all_transitions.pop()
	s = transition[0]
	dist = s - pointer
	html_output += sequence.slice(pointer,pointer + dist)

	if (transition[1].type=="exon_start"){
	    html_output+= '</span><span class="exon" id="exon-'+transition[1].data.id+'">'
	} else if (transition[1].type=="exon_end"){
	    html_output+= '</span><span class="intron">'
	} else if (transition[1].type=="spacer_start"){
	    html_output+='<span class="guide highlight '+transition[1].data.tool+'">'
	} else if (transition[1].type=="spacer_end"){
	    html_output+='</span>'
	} else if( transition[1].type=="start"){
	    html_output +='<span class="intron">'
	} else if( transition[1].type=="end"){
	    html_output +='</span class="intron">'
	}
	pointer += dist
    }

    
    
    return html_output
}

