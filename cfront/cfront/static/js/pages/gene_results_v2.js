x1 = 0
x2 = 0
trans = null
exon_elts = []
selection_start = null
selection_end = null
letters_timer = null
max_spacers = 20
selection_timer = null
exon_line = null
exon_select_line = null

draw = null

function draw_svg(){

    //globals
    svg_w = 600
    svg_h = 200
    svg_margin = 100
    svg_inner_w = svg_w - svg_margin *2
    svg_slider_y = 50
    svg_exon_y = 75
    svg_handle_w = 10

    svg_handle_h = 50
    
    svg_handle_lim_left = svg_margin
    svg_handle_lim_right = svg_w - svg_margin
    
    letters = sessionInfo.seq_letters
    selection_start = 0
    selection_end = Math.floor(sessionInfo.seq_letters.length / 2)
    
    
    
     draw = SVG('drawing').size(svg_w, svg_h)
    x1 = svg_margin
    x2 = svg_w - svg_margin
    
    handle1 = draw.rect(svg_handle_w,svg_handle_h).move(svg_margin - svg_handle_w / 2, svg_slider_y).attr({"class":"drag-handle"})
    handle2 = draw.rect(svg_handle_w,svg_handle_h).move(svg_w - svg_margin -svg_handle_w/2, svg_slider_y).attr({"class":"drag-handle"})
    handle1.draggable({
	minX: svg_margin - svg_handle_w/2
	, minY: svg_slider_y
	, maxX: svg_w - svg_margin + svg_handle_w/2
	, maxY: svg_slider_y+svg_handle_h
    })
    handle2.draggable({
	minX: svg_margin - svg_handle_w/2
	, minY: svg_slider_y
	, maxX: svg_w - svg_margin + svg_handle_w/2
	, maxY: svg_slider_y+svg_handle_h
    })

    window_left_text = draw.text("GGGCCC").attr({"class":"selection-left"}).move(x1,svg_slider_y)
    window_right_text = draw.text("AAAATTT").attr({"class":"selection-right"}).move(x2,svg_slider_y)
    
    // bind
    handle1.on('dragmove.namespace', function(e){
	x1 = Math.min(Math.max(e.detail.p.x,svg_handle_lim_left),svg_handle_lim_right)

	
	if( ! selection_timer){
	    selection_changed()
	    selection_timer = window.setTimeout(function(){
		selection_timer = null
		selection_changed()
	    },250)
	}
    
    })
    // bind
    handle2.on('dragmove.namespace', function(e){
	x2 = Math.min(Math.max(e.detail.p.x,svg_handle_lim_left),svg_handle_lim_right)
	if( ! selection_timer){
	    selection_changed()
	    selection_timer = window.setTimeout(function(){
		selection_timer = null
		selection_changed()
	    },500)
	}
    })
    
    exons = get_exons()
    
    exon_line = draw.line(svg_margin, svg_exon_y, svg_w - svg_margin, svg_exon_y).stroke({ width: .5 })
    exon_elts = _.map(exons,function(e){
	left = transform_exon_x(e.start)
	right = transform_exon_x(e.end)
	return draw.rect( right - left, 10).move(left,svg_exon_y-5)
	
    })

    selection_changed()




}

function selection_changed(){
    left = Math.min(x1,x2)
    right = Math.max(x1,x2)
    selection_start = reverse_transform_exon_x(left)
    selection_end = reverse_transform_exon_x(right)

    seq = sessionInfo.seq_letters
    //$(".selection-left-viewer").text(seq.slice(selection_start - 10, selection_start + 10))
    //$(".selection-right-viewer").text(seq.slice(selection_end - 10, selection_end + 10))

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
    
    
    window_left_text.text(init_slice).move(left - 64,svg_slider_y - 20)
    window_right_text.text(end_slice).move(right -64, svg_slider_y +80)

    exons = get_exons()
    for (var i = 0; i< exons.length; i++){
	elt = exon_elts[i]
	exon = exons[i]
	gene_start =  sessionInfo.gene_info.start

	if(exon.start-gene_start < selection_end && exon.end-gene_start > selection_start){
	    elt.attr({"class":"selected"})
	} else{
	    elt.attr({"class":""})
	}

	    
    }
    
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


    if (! exon_select_line){	
	exon_select_line =  draw.line(svg_handle_w/2 + transform_exon_x(selection_start),svg_exon_y,-svg_handle_w/2 + transform_exon_x(selection_end),svg_exon_y).attr({"class":"exon-line"})
    } else {
	exon_select_line.plot(svg_handle_w/2 + transform_exon_x(selection_start+sessionInfo.gene_info.start),svg_exon_y,-svg_handle_w/2 + transform_exon_x(selection_end+sessionInfo.gene_info.start),svg_exon_y)
    }
    
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
    })

    
    $(document).on("change",".export",function(ev){
	$(".export-all").prop("checked",false)
    })

    
    $(document).on("click",".highlight.guide",
		   function(ev){
		       $e = $(ev.currentTarget)
		       guide_sequence=$e.attr("guide_sequence")
		       targets = [ "#spacer-mid-margin-"+guide_sequence,
				   "#spacer-margin-"+guide_sequence]
		       for (var i = 0; i < targets.length ; i++){
		       	   $t = $(targets[i])
			   is_highlighted = $t.hasClass("highlighted")
			   $t.toggleClass("highlighted",!is_highlighted)
		       }
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
    selected_spacers = spacers_sorted.slice(0,max_spacers)
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
	//if( transition[1].type=="exon_start" || transition[1].type=="exon_end"){continue}
	s = transition[0]
	dist = s - pointer
	html_output += sequence.slice(pointer,pointer + dist)

	if (transition[1].type=="exon_start"){
	    html_output+= '</span><span class="exon" id="exon-'+transition[1].data.id+'">'
	} else if (transition[1].type=="exon_end"){
	    html_output+= '</span><span class="intron">'
	} else if (transition[1].type=="spacer_start"){
	    html_output+='<span class="guide highlight '+transition[1].data.tool+'">'
	   // html_output+='<span score="'+transition[1].data.score+'"  spacer_id="'+transition[1].data.id +'" pam_before="'+(transition[1].data.pam_before  ? transition[1].data.pam_before : "") +'" target="#spacer-margin-'+transition[1].data.guide_sequence+'"  pam_after="'+(transition[1].data.pam_after  ? transition[1].data.pam_after : "")+'" guide_sequence="'+transition[1].data.guide_sequence+'" class="guide highlight '+transition[1].data.tool+'"><a class="white" >'
	} else if (transition[1].type=="spacer_end"){
	    html_output+='</span>'
	    
	   // html_output+='</a></span>'
	} else if( transition[1].type=="start"){
	    html_output +='<span class="intron">'
	} else if( transition[1].type=="end"){
	    html_output +='</span class="intron">'
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
	
	params = {"name":gene_info.Name+ " KNOCKOUT GUIDE",
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
	    tool = ["cas9","cpf1"][i]
	   
	    $spacerlist = this.$el.find("."+tool).find(".spacer-list")
	    selected_spacers = get_selected_spacers(tool)
	    for (var j = 0; j < selected_spacers.length; j++){
		spacer = selected_spacers[j]
		$spacerlist.append(
		    $("<li>").html(_.template($("#spacer-oneline-header-template").html())(
			{"guide_sequence":spacer.guide_sequence,
			 "pam_before":spacer.pam_before?spacer.pam_before:"",
			 "pam_after":spacer.pam_after?spacer.pam_after:"",
			 "score":spacer.score?spacer.score:"",
			})).attr("id","spacer-oneline-"+spacer.guide_sequence)
		)
	    }
	}

	rerender_letters(this)
	   
	
	return this
    },
    
})
