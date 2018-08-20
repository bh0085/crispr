
var GeneResultsV2V = Backbone.View.extend({
    template:$("#gene-results-v2-section-template").html(),
    className:"scrolly-section",
   
    render:function(){
	genome_info = sessionInfo.genome_info
	gene_info = sessionInfo.gene_info
	data = sessionInfo.data
	status = sessionInfo.status
	
	params = {"name":gene_info.Name,
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
	render_letters()

	
	return this
    },
    
})


r1=null
r2=null
exon_elts = []
letters_timer = null
max_spacers = 10
min_per_guide = 5
selection_timer = null
exon_line = null
exon_select_line = null
selected_spacer = null
draw = null
STATE = {
    drawn_details:false,
}

function draw_svg(){

    var slider = document.getElementById('slider');

    noUiSlider.create(slider, {
	start: [get_range()[0], get_range()[1]],
	connect: true,
	margin:50,
	step:50,
	range: {
	    'min': 0,
	    'max': get_gene_sequence().length
	}
    });


    //globals
    svg_w = 600
    svg_h = 100
    svg_margin = 0
    svg_inner_w = svg_w - svg_margin *2
    svg_exon_y = 75
    draw = SVG('drawing').size(svg_w, svg_h)

    exons = get_exons()
    exon_line = draw.line(svg_margin, svg_exon_y, svg_w - svg_margin, svg_exon_y).stroke({ width: .5 })
    exon_elts = _.map(exons,function(e,i){
	left = transform_exon_x(e.start)
	right = transform_exon_x(e.end)

	

	grp = draw.group().addClass("exon-group").attr("exon_range_start",get_exon_start_in_gene(e)).attr("exon_range_end",get_exon_end_in_gene(e))
	rect = grp.rect( right - left, 10).move(left,svg_exon_y-5)
	text = grp.text( function(add) {
		     add.tspan('EXON '+i).newLine()
		     add.tspan("start: "+ get_exon_start_in_gene(e)).newLine()
		     add.tspan("end: "+ get_exon_end_in_gene(e)).newLine()

		 }).move(left, svg_exon_y - 75)
	
	return { "group":grp,
		 "exon": rect,
		 "text": text,
	       }
	
    })

   
    slider.noUiSlider.on("update",function(vals,handle){
	set_range(_.map(vals,function(e){return Number(e)}))
	// this is a little awkward, because this function needs to be called to
	// update the view elements, so when the range is first initialized in "init_with_data",
	// that is not done. It is done here, driven by the slider event which
	// is called not only on update but also on init
	update_on_range_changed()

    })
    
    

}

function get_gene_sequence(){
    return sessionInfo.seq_letters
}
function get_range(){
    return [r1,r2]
}

function set_range(range){
    r1 = range[0]
    r2 = range[1]
    // no longer calls range_changed.
    // this is left to the ui
}

function exon_in_range(exon){
    gene_start =  sessionInfo.gene_info.start
    return ( exon.start - gene_start < r2 && exon.end - gene_start > r1)
}

function update_on_range_changed(){
    var r = get_range()
    var r1 = r[0]
    var r2 = r[1]

    spacers = spacers_in_range()
    $(".range-in-genome").text(sessionInfo.gene_info.chrom + ":"+(r1+sessionInfo.gene_info.start)+"-"+(sessionInfo.gene_info.start+r2))
    $(".range-start").text(r1)
    $(".range-end").text(r2)
    $(".guides-in-range-count").text(spacers.length)

    seq = sessionInfo.seq_letters

    n_exons = 0;
    exons = get_exons()
    for (var i = 0; i< exons.length; i++){
	elt = exon_elts[i].exon
	text_elt =  exon_elts[i].text

	
	exon = exons[i]
	if(exon_in_range(exon)){
	    elt.attr({"class":"selected"})
	    text_elt.attr({"class":"selected"})
	    n_exons+=1;
	} else{
	    elt.attr({"class":""})
	    text_elt.attr({"class":""})

	}

	    
    }
    
    $(".exon-count").text(n_exons)

    target_exons = _.filter(_.map(get_exons(),function(e,i){
	     return exon_in_range(e)?i+1:null
    }),function(e){return e!=null?true:false})

    if (target_exons.length >1){
	exons_string = "EXON(s) " + ( target_exons.slice(0,-1).join(", ") + " & " + target_exons.slice(-1)[0])
    } else if (target_exons.length == 1) {
	exons_string = "EXON " +  target_exons[0]
    } else {
	exons_string = "zero exons"
    }
    
    
    $("#hero-spacers").html(_.template($("#hero-spacers-table-template").html())(
	{gene_name:sessionInfo.gene_info["Name"][0],
	 exons_string:exons_string,
	 genome_name:sessionInfo.genome_info.name,
	 assembly:sessionInfo.assembly,
	 geneid:sessionInfo.geneid,
	}
    ))
    for ( var i = 0 ; i < spacers.length ; i++){
	s = spacers[i]
	exon = get_spacer_exon(s)
	exon_name = get_exon_name(exon)
	s.exon_name = exon_name
	$("#hero-spacers").find("table").append($("<tr>",{"class":"spacer-row"}).html(_.template($("#hero-spacer-template").html())(s)))
    }
    $(".start-base").text(r1)
    $(".end-base").text(r2)


    sel = get_selected_spacer()

    if (!sel){
	var $e = $($(".show-details")[0])
	$e.prop("checked",true)
	$e.trigger("change")
    }else{
	
	var sel_inputs = _.filter($(".show-details"),function(e){return $(e).attr("guide_sequence")==sel.guide_sequence})
	
	if(sel_inputs.length >0){
	    $(sel_inputs[0]).prop("checked",true)
	    if ( !STATE.drawn_details){
		var $e = $(sel_inputs[0])
		$e.trigger("change")
		STATE.drawn_details = true;
	    } else {
		var $e = $(sel_inputs[0])
		$e.trigger("change")
	    }


	    
	} else {
	    var $e = $($(".show-details")[0])
	    $e.prop("checked",true)
	    $e.trigger("change")
	}
    }
    
}



function set_selected_spacer(spacer){
    selected_spacer = spacer
    selection_changed()
}

function get_selected_spacer(){
    return selected_spacer

}
function get_exon_name(exon){
    all_exons = get_exons()
    index = _.filter(_.map(
	all_exons,function(e,i){
	    return (e.start ==exon.start) ? i: null
	}),function(e){
	    return e != null
	})[0]
    
    return "EXON_" + index
}

function selection_changed(){
    spacer = get_selected_spacer()
    spacer_exon = get_spacer_exon(spacer)
    exon_start =  get_exon_start_in_gene(spacer_exon)
    exon_name = get_exon_name(spacer_exon)

    $("#spacer-details-container").html(
	_.template($("#spacer-detail-view-template").html())(
	    {
		"spacer":spacer,
		"gene":sessionInfo.gene_info,
		"assembly":sessionInfo.assembly,
		"exon_start":exon_start,
		"exon_name":exon_name,
	    }))



    
    for(var i = 0; i < spacer.offtarget_alignments.length; ++i) {
	$("#spacer-details-container .ot-table-container").addClass('full')
	var a = spacer.offtarget_alignments[i]
	$("#spacer-details-container").find("table").append(_.template($("#offtarget-spacer-row-template").html())({"a":a}))
    }
    
    $("#download-guide-gb").attr("href","/v2/"+sessionInfo.assembly+"/"+sessionInfo.geneid+"/"+spacer.tool+"/"+spacer.guide_sequence+"/guide.gb")
    $("#download-guide-gb").toggleClass("disabled",false)
    $(".selectable").removeClass("selected")

    
    $(".selectable").filter(
	function(e){
	    return $(e).attr("guide_sequence")==spacer.guide_sequence;}
    ).addClass("selected")
    
    render_letters()
    
    setTimeout(function(){
	render_cutsite()
    }, 100)
    
}


    function transform_exon_x(start){
	gene_start =  sessionInfo.gene_info.start
	seq_len = sessionInfo.seq_letters.length
	return ((start-gene_start) / seq_len)*svg_inner_w + svg_margin
    }
    function reverse_transform_exon_x(x){
	return Math.floor(((x - svg_margin) / svg_inner_w) * sessionInfo.seq_letters.length)
    }


function get_exon_start_in_gene(e){
    gene_start = sessionInfo.gene_info.start
    return e.start - gene_start
}

function get_exon_end_in_gene(e){
  
    gene_start = sessionInfo.gene_info.start
    return e.end - gene_start
}

function get_spacer_start_in_gene(s){
    return s.guide_start + s.region_start - sessionInfo.gene_info.start + 1
}

function get_spacer_end_in_gene(s){
    return s.guide_start + s.region_start - sessionInfo.gene_info.start + s.guide_length +1

}
function get_spacer_start_in_exon(s){
    return s.guide_start +1
}
function get_spacer_end_in_exon(s){
    return s.guide_start  + s.guide_length +1
}



function get_spacer_exon(s){
    exons = get_exons()
    overlaps = _.filter(exons, function(e){
	return get_exon_start_in_gene(e) < get_spacer_end_in_gene(s) && get_exon_end_in_gene(e) > get_spacer_start_in_gene(s)
    })

    
    
    if( overlaps.length == 0 ){
	throw "no overlapping exons"
    } else if(overlaps.length >1){
	throw "multiple overlapping exons"
    } else{
	return overlaps[0]
    }
}

function render_letters (){
    var s = get_selected_spacer()
    var exon = get_spacer_exon(s)
    var start = get_exon_start_in_gene(exon)
    var end = get_exon_end_in_gene(exon)
    var letters = sessionInfo.seq_letters.slice(start,end)
    var pam_before_length  =s.pam_before? s.pam_before.length : 0;
    var pam_after_length =s.pam_after? s.pam_after.length :0;

    var s_ex_start = get_spacer_start_in_exon(s)


    var rev = false
    if( s.guide_strand == 1){

	letters_before = letters.slice(0, s_ex_start - pam_before_length)
	pam_letters_before = letters.slice(s_ex_start - pam_before_length, s_ex_start)
	guide_letters = letters.slice(s_ex_start,s_ex_start+s.guide_length)
	pam_letters_after = letters.slice(s_ex_start+s.guide_length,s_ex_start+s.guide_length+pam_after_length)
	letters_after = letters.slice(s_ex_start+s.guide_length+pam_after_length)
				      
    } else{

	letters_before = letters.slice(0,s_ex_start)
	pam_letters_before = letters.slice(s_ex_start - pam_after_length, s_ex_start)
	guide_letters = letters.slice(s_ex_start,s_ex_start+s.guide_length)
	pam_letters_after = letters.slice(s_ex_start+s.guide_length,s_ex_start+s.guide_length+pam_before_length)
	letters_after = letters.slice(s_ex_start+s.guide_length)
	rev = true
    }

    

    
    
    $(".exon-sequence-container").empty()
	.append( $('<span class="letters-before">').text(letters_before))
	.append( $('<span class='+(rev?"pam-letters-after":"pam-letters-before")+'>').text(pam_letters_before))
	.append( $('<span class="guide guide-letters '+s.tool+'">').text(guide_letters))
	.append( $('<span class='+(rev?"pam-letters-before":"pam-letters-after")+'>').text(pam_letters_after))
	.append( $('<span class="letters-after">').text(letters_after))



    
}



function render_cutsite(){
    spacer = get_selected_spacer()

    $("#cutsite").empty();
    draw= SVG('cutsite').size(svg_w, 100)


    // pam before and after will refer to the sense strand of the guide sequence
    // pam5 and pam3 will refer to the sense strand of the coding sequence
    
    var letter_width = 10
    var pam_before_length = spacer.pam_before?spacer.pam_before.length:0
    var pam_after_length = spacer.pam_after?spacer.pam_after.length:0


    var pam_before_width = pam_before_length * letter_width
    var pam_after_width = pam_after_length * letter_width

    var poly_annotation_height = letter_width
    var arrowhead_width= poly_annotation_height/2
    var guide_strand = spacer.guide_strand
    var guide_length = spacer.guide_width
    

    
    
    //currently broken for reverse strand
    var is_fwd = spacer.guide_strand == 1
    if (is_fwd){
	var pam5_width = pam_before_width
	var pam3_width = pam_after_width
    }else{
	var pam3_width = pam_before_width
	var pam5_width = pam_after_width
    }

    var has_pam5 = pam5_width > 0 ? true: false;
    var has_pam3 = pam3_width > 0 ? true: false;
    
    var  guide_width = spacer.guide_length * letter_width



    s = spacer
    var n_letters =60
    middle_letter_idx = Math.floor((get_spacer_start_in_gene(spacer) + get_spacer_end_in_gene(spacer)) / 2)
     start_letter_idx = middle_letter_idx - n_letters / 2 + 0
    var end_letter_idx = start_letter_idx + n_letters + 0

    guide_sequence_idx_in_letters = get_spacer_start_in_gene(s)- start_letter_idx - 1

    
     gs_x0 = guide_sequence_idx_in_letters  * letter_width
     gs_dx = guide_width
    gs_x1 = gs_x0 + gs_dx

    y_ofs = is_fwd?0:70

    if (is_fwd){
	
	var guide_xys = [
	    [gs_x0,0],
	    [gs_x1-arrowhead_width,0 + y_ofs],
	    [gs_x1,poly_annotation_height/2 + y_ofs],
	    [gs_x1-arrowhead_width,poly_annotation_height + y_ofs],
	    [gs_x0,poly_annotation_height + y_ofs],
	]
    } else{
	
	var guide_xys = [
	    [gs_x0,poly_annotation_height/2 + y_ofs],
	    [gs_x0+arrowhead_width,0 + y_ofs],
	    [gs_x1,0 +y_ofs],
	    [gs_x1,poly_annotation_height + y_ofs],
	    [gs_x0+arrowhead_width,poly_annotation_height + y_ofs],
	]
    }

    if (has_pam5 && has_pam3){
	throw "multiple pams not supported"
    }

    pam_width = has_pam5?pam5_width:pam3_width
    
    
    var pam_xys
    if (has_pam5){
	var p_offset = gs_x0 - pam_width 
    } else {
	var p_offset = gs_x1
    }

    var aleft = p_offset
    var aright = p_offset + pam_width

    if(is_fwd){
    pam_xys = [
	[aleft,0+ y_ofs],
	[aright-arrowhead_width,0+ y_ofs],
	[aright,poly_annotation_height/2+ y_ofs],
	[aright-arrowhead_width,poly_annotation_height+ y_ofs],
	[aleft,poly_annotation_height],
    ]
    } else {
	pam_xys = [
	    [aleft,poly_annotation_height/2+ y_ofs],
	    [aleft+arrowhead_width,0+ y_ofs],
	    [aright,0+ y_ofs],
	    [aright,poly_annotation_height+ y_ofs],
	    [aleft+arrowhead_width,poly_annotation_height+ y_ofs],
	]
    }

    cut1 = [[0,0],
	    [6,0],
	    [3,4]]

    
    cut2 = [[3,0],
	    [6,4],
	    [0,4]]
    
    guide_xys_str = _.map(guide_xys,function(e){return e.join(",")}).join(" ")
    pam_xys_str = _.map(pam_xys,function(e){return e.join(",")}).join(" ")
    cut1_str =_.map(cut1,function(e){return e.join(",")}).join(" ")
    cut2_str =_.map(cut2,function(e){return e.join(",")}).join(" ")
    
    var g_offset_y = 10;
    var seq_top_offset_y = 18;
    var seq_bottom_offset_y =56

    var cut_idx_5 = 18
    var cut_idx_ofs_5 = is_fwd ? cut_idx_5: 31 - cut_idx_5
    var cut5_base = guide_sequence_idx_in_letters + cut_idx_ofs_5

    
    
    cut5_pos = cut5_base * letter_width-3
    cut3_pos = cut5_base * letter_width + 4*letter_width-3
    
    //gs_x0
    //gs_x1
    
    guide_poly= draw.polygon(guide_xys_str).fill('blue').stroke({ width: 1 })
    pam_poly  = draw.polygon(pam_xys_str).fill(pam_before_length>0?'green':'red').stroke({ width: 1 })
    cut1_poly  = draw.polygon(cut1_str).fill('red').stroke({ width: 0 }).move(cut5_pos,seq_top_offset_y)
    cut2_poly  = draw.polygon(cut2_str).fill('red').stroke({ width: 0 }).move(cut3_pos,seq_bottom_offset_y)

    
    
   
    
    fwd_letters = sessionInfo.seq_letters.slice(start_letter_idx,end_letter_idx)
    rev_letters = _.map(fwd_letters.split("").reverse(),function(e){
	return {"A":"T",
		"T":"A",
		"G":"C",
		"C":"G"}[e]
    
    }).join("")
    
    dna_letters_text = draw.text(function(add) {
		     add.tspan(fwd_letters).newLine()
		     add.tspan(rev_letters).newLine()

		 }).move(0,20)
    

    console.log(fwd_letters)
    
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
	letters = sessionInfo.seq_letters
	set_range([0,letters.length])
	set_selected_spacer(spacers_in_range()[0])
	rendered = sview.render()
	$rendered = rendered.$el
	$('#gene_results_v2-container').empty().append($rendered)
	draw_svg()
    }

    $(document).on("mouseover", "rect",function(ev){
	$tgt = $(ev.currentTarget).parent()
	$tgt.attr("class", $tgt.attr("class").replace("focused","") + " focused")
    })
    $(document).on("mouseout", "rect",function(ev){
	$tgt = $(ev.currentTarget).parent()
	$tgt.attr("class", $tgt.attr("class").replace("focused",""))
    })

    $(document).on("click", "rect",function(ev){
	
	$tgt = $(ev.currentTarget).parent()

	classes = $tgt.attr("class")
	if (classes.search("ranged") > 0)
	{

	    letters = sessionInfo.seq_letters
	    slider.noUiSlider.set([0,letters.length])
	    $tgt.attr("class", $tgt.attr("class").replace("ranged",""))

	    
	} else {
	    exon_range_start = $tgt.attr("exon_range_start")
	    exon_range_end = $tgt.attr("exon_range_end")
	    slider.noUiSlider.set([Number(exon_range_start),Number(exon_range_end)])
	    $tgt.attr("class", $tgt.attr("class").replace("ranged","") + " ranged")

	}
    })

	
    
    
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

    $(document).on("click", ".spacer-row",function(ev){
	$row = $(ev.currentTarget)
	$e= $($row.find(".show-details")[0])
	$e.prop("checked",true)
	$e.trigger("change")
    })
    $(document).on("change", ".show-details",
		   
		   function(ev){

		       
		       $(".spacer-row").removeClass("selected")
		       var $row = $(ev.currentTarget).parents(".spacer-row")
		       $row.addClass("selected")
		       seq = $(".show-details:checked").attr("guide_sequence")
		       sel =  _.filter(spacers_in_range(),function(e){
			   return e.guide_sequence==seq
		       })[0]
		       set_selected_spacer(sel)
		   })
    

    
    if (sessionInfo.data == null)
    {
	$("#gene_results_v2-container").html(
	    _.template($("#results-waiting-template").html())({"location":window.location})
	)
	get_data()
    } else{
	init_with_data()
    }


  

    
}



function spacers_in_range(){
    data = sessionInfo.data
    spacers_data = data["cas9"].spacers.concat(spacers_data = data["cpf1"].spacers)
    gene_start =  sessionInfo.gene_info.start


  
    
    selected_spacers = _.filter(spacers_data,
				function(s){
				    return (s.guide_start + s.region_start -gene_start) <r2 && (s.guide_start + s.region_start - gene_start + s.guide_length)>r1; 
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
    
    return selected_spacers

}

    function get_exons(){
	data = sessionInfo.data
	exons = data.cas9.search_regions
	return exons
    }

