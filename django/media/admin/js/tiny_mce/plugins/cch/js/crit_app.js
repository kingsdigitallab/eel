tinyMCEPopup.requireLangPack();

var CritAppDialog = {
	init : function() {
		var f = document.forms[0];
		
		// Get the selected contents as text and place it in the input
		//f.someval.value = tinyMCEPopup.editor.selection.getContent({format : 'text'});
		//f.somearg.value = tinyMCEPopup.getWindowArg('some_custom_arg');
		// f.number.value = this.getParamVal('number',  0);
		$('#ca-table-div').html(tinyMCEPopup.getWindowArg('table'));
		this.setFormFromString(tinyMCEPopup.getWindowArg('readings'));
		// tinyMCEPopup.getWindowArg('win').handle = window;

	    // var winID = tinyMCEPopup.id;
	    // var wm = tinyMCEPopup.editor.windowManager;

	    // does not work!
	    // wm.resizeBy(800, 300, winID);
	},

	insert : function() {
		// Insert the contents from the input into the document
		//tinyMCEPopup.editor.execCommand('mceInsertContent', false, document.forms[0].someval.value);
		// call the callback with the result
		
//		var n = parseInt(document.forms[0].number.value);
//		if (isNaN(n) || n < 0 || n > 1000) {
//			$('#number-error').css('display', 'block');
//			return false;
//		}
//		this.getParamVal('callback', function() {})(n);
		
		// call the main module back to insert the new tag
		tinyMCEPopup.getWindowArg('callback')(this.getStringFromForm());
		
		tinyMCEPopup.close();
	},
	
	getParamVal : function(key, def) {
//		var ret = tinyMCEPopup.getWindowArg('params');
//		if (ret != null) {
//			ret = ret[key];
//		} else {
//			ret = def;
//		}

		var ret = '';
		return ret;
	},
	
	clearForm : function() {
		$('#ca-table-div input[type=text]').val('');
		$('#ca-table-div input[type=checkbox]').each(function() {this.checked = '';});		
	},
	
	setFormFromString : function(readings) {
		// sets the form from a json string
		//readings = '['lemma', ["r1","W2"],["r3","W4","A3"]]';
		readings = $.evalJSON(readings);
		if (!(readings instanceof Array)) return;
		
		this.clearForm();
		
		$('#lemmaid').val(readings[0]);
		
		for (var i = 1; i < readings.length; i++) {
		    $('#ca-table-div input[name=ca-r-'+(i)+']').val(readings[i][0]);
		    for (var j = 1; j < readings[i].length; j++) {
		        var item_name = 'ca-d-' + (i) + '-' + readings[i][j].substring(0, 1) + '-' + readings[i][j].substring(1);
		        $('#ca-table-div input[name='+item_name+']').attr('checked', 'checked');
		    }
		}
	},

	getStringFromForm : function() {
		// returns a json string from the form
		// e.g. '[["r1","W2"],["r3","W4","A3"]]'
		// ca-r-1
		// ca-d-1-W-1
		var readings = [$('#lemmaid').val()];
		var reading = null;
		$('#ca-table-div input').each( 
			function () {
			    var el = $(this);
			    var nparts = this.name.split('-');
			    if (nparts[1] == 'r') {
			        text = el.val();
			        reading = null;
			        if (text) {
			            reading = [text];
			            readings.push(reading);
			        }
			    }
			    if ((nparts[1] == 'd') && (this.checked)) {
			        if (reading) reading.push(nparts[3] + nparts[4]);
			    }
			}
		);
		return $('<div/>').text($.toJSON(readings)).html();
	}
	
};

tinyMCEPopup.onInit.add(CritAppDialog.init, CritAppDialog);
