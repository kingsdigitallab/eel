/**
 * Display a graph of relationships among texts as a SVG graph.
 *  
 * Requires: 
 * 		Raphael js library.
 * 		A <div id="rel-tooltip"> in the html
 * 		A <div id="canvas"> in the html
 * 
 * Date: Nov 2011
 * Author: Geoffroy Noel
 */
var glow = null;

function get_color_from_language(languageid, graph_data) {
	var ret = '#fff';
	if (languageid in graph_data.languages) ret = '#'+graph_data.languages[languageid].color;
	return ret;
}

function hideTooltip() {
	$('#rel-tooltip').hide();
}

function showTooltip(x, y, html) {
	$('#rel-tooltip').show();
	$('#rel-tooltip').offset({top: y, left: x});
	$('#rel-tooltip').html(html);
}

function on_mouse_over_element(element, event, out, graph_data) {
	var padding = 5;
	var offset = $('#canvas').offset();
	if (out) {
		for (var i = 0; i < glow.length; i++) glow[i].remove(); 
		glow.clear();
		hideTooltip();
	} else {
		glow = element.ctrl.glow();					
		if (element.type == 'circle') {
			showTooltip(offset.left + element.attrs.cx + element.attrs.r + padding, 
					offset.top + element.attrs.cy - element.attrs.r + padding, 
					element.text.title + '<br/>' + element.text.date);
		}
		if (element.type == 'path') {
			var point0 = element.getPointAtLength(1);
			var point = element.getPointAtLength(element.getTotalLength()-1);
			if (point0.x > point.x) point = point0;						
			showTooltip(offset.left + point.x + padding, 
					offset.top + point.y - padding, 
					'' + graph_data.rel_types[element.link.typeid].name + '<br/>' + element.link.description);
		}
	}
}

function get_arrow_path_between_bubbles(x0, y0, x1, y1, head_angle, head_length, radius, gpaper) {
	ret = gpaper.path('M'+x0+','+y0+'L'+x1+','+y1);
	point0 = ret.getPointAtLength(radius);
	point1 = ret.getPointAtLength(ret.getTotalLength() - radius);
	ret.remove();
	ret = get_arrow_path(point0.x, point0.y, point1.x, point1.y, head_angle, head_length);
	return ret;
}

function get_arrow_path(x0, y0, x1, y1, head_angle, head_length) {
	var ret = '';
	ret += 'M'+x0+','+y0;
	ret += 'L'+x1+','+y1;
	
	var angle = Raphael.angle(x0, y0, x1, y1);
	var degrad = 1 / 180 * Math.PI; 
	var x2 = x1 + head_length * Math.cos((angle - head_angle) * degrad);
	var y2 = y1 + head_length * Math.sin((angle - head_angle) * degrad);
	ret += 'L'+Math.floor(x2)+','+Math.floor(y2);
	ret += 'L'+x1+','+y1;
	var x2 = x1 + head_length * Math.cos((angle + head_angle) * degrad);
	var y2 = y1 + head_length * Math.sin((angle + head_angle) * degrad);
	ret += 'L'+Math.floor(x2)+','+Math.floor(y2);
	ret += 'L'+x1+','+y1;
	
	return ret;
}

function show_links(graph_data) {
	var gpaper = Raphael('canvas', graph_data['image']['width'], graph_data['image']['height']);
	gpaper.clear();
	var rad = graph_data['image']['radius'];
	var border = 1;
	var rade = rad + border;

	// draw the nodes
	for (i in graph_data['texts']) {
		var text = graph_data['texts'][i];
		
		// compute the location on a grid
		var y = text.y;
		var x = text.x;
		
		// show the bubble
		text.ctrl = gpaper.circle(x, y, rad).attr({'fill': get_color_from_language(text.languageid, graph_data), 'stroke': '#000'});
		
		// show the label
		gpaper.text(text.ctrl.attr('cx'), text.ctrl.attr('cy'), text.short_title).attr({'font-size': 12, 'fill': '#fff'});

		text.ctrlHover = gpaper.circle(x, y, rad).attr({'fill': get_color_from_language(text.languageid, graph_data), 'stroke': '#000'});
		text.ctrlHover.attr('fill-opacity', 0);
		text.ctrlHover.ctrl = text.ctrl;
		text.ctrlHover.text = text;

		text.ctrlHover.mouseover(function (event) { on_mouse_over_element(this, event, false, graph_data); });
		text.ctrlHover.mouseout(function (event) { on_mouse_over_element(this, event, true, graph_data); });
		text.ctrlHover.click(function (event) { location = '/laws/texts/' + this.text.slug + '/relationships/'; });
	}
	
	// draw the links
	for (i in graph_data['links']) {
		var link = graph_data['links'][i];
		//gpaper.path('M');
		var texts = [graph_data['texts'][link.from], graph_data['texts'][link.to]];
		//gpaper.path('M'+texts[0]);
		var head_angle = 30;
		var head_length = rad / 2;
		//var path = get_arrow_path(texts[0].ctrl.attr('cx') + rade, texts[0].ctrl.attr('cy'), texts[1].ctrl.attr('cx') - rade, texts[1].ctrl.attr('cy'), head_angle, head_length);
		var path = get_arrow_path_between_bubbles(texts[0].ctrl.attr('cx'), texts[0].ctrl.attr('cy'), texts[1].ctrl.attr('cx'), texts[1].ctrl.attr('cy'), head_angle, head_length, rade, gpaper);
		link.ctrl = gpaper.path(path);
		link.ctrl.attr({'fill': '#f00', 'stroke': '#000'});
		
		//link.ctrlHover = gpaper.path(path).attr({'fill': '#f00', 'stroke': '#f00', 'stroke-width': 3, 'fill-opacity': 0, 'stroke-opacity': 0});
		link.ctrlHover = gpaper.path(path).attr({'fill': '#f00', 'stroke': '#f00', 'stroke-width': 7});
		link.ctrlHover.attr({'fill-opacity': 0, 'stroke-opacity': 0});
		link.ctrlHover.ctrl = link.ctrl;
		link.ctrlHover.link = link;
										
		link.ctrlHover.mouseover(function (event) { on_mouse_over_element(this, event, false, graph_data); });
		link.ctrlHover.mouseout(function (event) { on_mouse_over_element(this, event, true, graph_data); });
	}
	
	// draw the timeline
	draw_timeline(gpaper, graph_data, rad);
}

function draw_timeline(gpaper, graph_data, rad) {
	var y = graph_data['image']['height'] - rad * 2;
	var xd = graph_data['timeline']['maxp'] - graph_data['timeline']['minp'];
	var td = graph_data['timeline']['maxt'] - graph_data['timeline']['mint'];
	
	// 1. find the time scale/resolution (tr)
	//var trs = [1, 5, 10, 50, 100, 500, 1000];
	var trs = [5, 10, 50, 100, 500, 1000];
	// This is the minimum space that we want to have between consecutive date marker on the timeline
	var xd_min = 50;
	var marker_height = 10;
	var color = '#89400a';
	var font_size = 12;
	
	var tr = 0;
	for (var i in trs) {
		tr = trs[i];
		if ((xd / td * tr) >= xd_min) break;
	}
	
	// 2. find the starting date based on that time resolution
	// e.g. mint = 1120, tr = 1 => 1120
	// e.g. mint = 1120, tr = 10 => 1120
	// e.g. mint = 1120, tr = 50 => 1100
	// e.g. mint = 1120, tr = 1000 => 1000
	var d0 = graph_data['timeline']['mint'] - graph_data['timeline']['mint'] % tr;
	
	// 3. draw the dates based on that time resolution
	for (var d = d0; d <= graph_data['timeline']['maxt']; d += tr) {
		//console.log(d);
		var x = graph_data['timeline']['minp'] + xd / td * (d - graph_data['timeline']['mint']);
		var mark = gpaper.path('M'+x+','+y+'l0,'+marker_height);
		mark.attr('stroke', color);
		gpaper.text(x, y + marker_height * 2, d).attr({'font-size': font_size, 'fill': color});
	}
	
	var path = get_arrow_path(graph_data['timeline']['minp'], y, graph_data['timeline']['maxp'] + rad, y, 30, rad / 2);
	path = gpaper.path(path);
	path.attr('stroke', color);
}
