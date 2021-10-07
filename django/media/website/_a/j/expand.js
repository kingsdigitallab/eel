$(document).ready(function(){
	var showAllText = 'Show all data';
	var hideAllText = 'Hide all data';
	
	$('#mainContent .resourceList a.g3').click(function () {
		if ($(this).text() == showAllText) {
			$(this).attr({
				title: hideAllText
			});
			$(this).text(hideAllText);
			$(this).addClass('s02');
			$(this).removeClass('s01');
			$("#mainContent .resourceList li.s01").addClass('s02');
			$("#mainContent .resourceList li.s01").removeClass('s01');
		} else {
			$(this).attr({
				title: showAllText
			});
			$(this).text(showAllText);
			$(this).addClass('s01');
			$(this).removeClass('s02');
			$("#mainContent .resourceList li.s02").addClass('s01');
			$("#mainContent .resourceList li.s02").removeClass('s02');
		}
	});


	$("#mainContent .resourceList ul.t01 li.s01 a.x01").click(function () {
		var $this = $(this);
		if ($this.parent('li').is('.s01')) {
			$this.text('Collapse');
			$this.attr({
				title: "Click to collapse extended data"
			});
			$this.parent('li').removeClass('s01');
			$this.parent('li').addClass('s02');
		} else {
			$this.text('Expand');
			$this.attr({
				title: "Click to expand extended data"
			});
			$this.parent('li').removeClass('s02');
			$this.parent('li').addClass('s01');
		}
		return false;
	});
});