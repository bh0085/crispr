//scripts powering crispr identification

test_seq = "AGAGAGGGAGATGTGATCGCTAGCATGCATCGACTAGCATCAGCTACGACTACGATCAGCTATTTATTATTATTAGAGAGCGCGCGCGACTACGACTAGAGAGATCGCATAGAGAGAGAGAGAGAGAGAGGAGAGAATGCATGCGATGAGGAGATGATGATGGATTCGGGCGCTAGCCGATGCTAGCTAG"

//fake function to compute collisions
function identify_compute_collisions(){
    var ranges, spacers
    spacers = identify_data.spacers;
    identify_data.collisions = {}
    ranges = []
    _.each(spacers,function(e){
	identify_data.collisions[e.id] = _.filter(ranges,
						  function(r){
						      return !(r[0] > (e.start+23) || r[1] < e.start)
						  }).length;
	ranges.push([e.start,e.start+23])
	
    });
}

//draws spacers with SVG
function identify_draw_spacers(){
    var el, canvas_w, canvas_h, svg;
    
    //config and create for SVG
    el = $("#identify .spacers-svg-container")
    canvas_w = 400, canvas_h = 200
    svg = el.svg(null, 0, 0, canvas_w,canvas_h,0,0,canvas_w,canvas_h).svg('get');
    $(svg._svg).attr("height",""+ canvas_h + "px");
    $(svg._svg).attr("width", ""+ canvas_w + "px");
    
    //draw functions and config
    strand_ofs = 5;
    collision_ofs = 3;
    spacer_color = "blue"
    strand_color = "black"
    function draw_query_spacer(spacer){
	var left_f,right_f, opts, left, right,top;
	if(spacer.strand==1){
	    left_f = spacer.start / submit_data.input_sequence.length;
	    right_f = (spacer.start +23) / submit_data.input_sequence.length;
	    top = canvas_h / 2 - strand_ofs - collision_ofs*identify_data.collisions[spacer.id]
	} else {
	    left_f = (submit_data.input_sequence.length - spacer.start - 23) / submit_data.input_sequence.length;
	    right_f = ( submit_data.input_sequence.length - spacer.start) / submit_data.input_sequence.length;
	    top = canvas_h/2 + strand_ofs + collision_ofs * identify_data.collisions[spacer.id]
	}
	left = left_f * canvas_w;
	right = right_f * canvas_w;
	console.log(left, right, top)
	p = svg.createPath();
	p.moveTo(left,top);
	p.lineTo(right,top);
	opts = {stroke:spacer_color,strokeWidth:1};
	svg.path(p,opts);
    }
  
    function draw_query_strands(){
	var left_f,right_f,left,right,opts,p;
	left_f = 0;
	right_f = 1;
	left = left_f * canvas_w;
	right = right_f * canvas_w;
	top_plus = canvas_h/2 - strand_ofs * .5
	top_minus = canvas_h/2 + strand_ofs *.5
	
	opts = {stroke:strand_color, strokeWidth:1}
	p = svg.createPath();
	p.moveTo(left, top_plus)
	p.lineTo(right,top_plus)
	svg.path(p,opts)

	p = svg.createPath();
	p.moveTo(left,top_minus)
	p.lineTo(right,top_minus)
	svg.path(p,opts)
    }

    //draw loop
    draw_query_strands()
    _.each(identify_data.spacers,
	   function(e,i){
	       draw_query_spacer(e);
	   });
    
}

function identify_sequence(){
    var spacers;
    
    // splits the input into plus, minus strands
    sequence = submit_data.input_sequence; 
    plus_strand = sequence
    minus_strand = reverse_complement(sequence)
    rep = RegExp(".\{20\}[ATGC][GA][T]","g")
    rem = RegExp(".\{20\}[ATGC][GA][T]","g")
    
    //checks strands for spacers
    var pluses = [],  minuses = [];
    while (m = rep.exec(plus_strand)){pluses.push(m)}
    while (m = rem.exec(minus_strand)){minuses.push(m)}    
    
    //appends strand lists, strands to the section
    $el = $("#identify")
    plus_section = $("<div>").html(
	_.template($("#ident_strand_template").html(),{strand_name:"plus strand"}))
	.appendTo($el)

    minus_section = $("<div>").html(
	_.template($("#ident_strand_template").html(),{strand_name:"minus strand"}))
	.appendTo($el)

    spacers = []
    _.each(pluses,function(e,i){
	plus_section.find("ul")
	    .append($("<li>")
		      .html(
			  _.template(
			      $("#spacer_seed_template").html(),
			      {"query_id":i,
			       "index":e.index,
			       "seq":e}
			  )
		      )
		     )
	spacers.push({"id":spacers.length,
		      "start":e.index,
		      "seq":e,
		      "strand":1})

    });
    _.each(minuses,function(e,i){
	minus_section.find("ul")
	    .append($("<li>")
		      .html(
			  _.template(
			      $("#spacer_seed_template").html(),
			      {"query_id":i,
			       "index":e.index,
			       "seq":e}
			  )
		      )
		     )
	spacers.push({"id":spacers.length,
		      "start":e.index,
		      "seq":e,
		      "strand":-1})
    });
    identify_data.spacers = spacers;

    // draws the spacers
    identify_compute_collisions();
    identify_draw_spacers();

}

function reverse_complement(sequence){
    rev = sequence.split("").reverse().join("")
    repl = rev.replace(/./g,function(letter){
	return {"A":"T",
		"T":"A",
		"G":"C",
		"C":"G"}[letter]
	
    });
    return repl
}

