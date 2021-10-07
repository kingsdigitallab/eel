tinyMCEPopup.requireLangPack();

var GapDialog = {
	init : function() {
		var f = document.forms[0];
		this.setFormFromString(tinyMCEPopup.getWindowArg('fields'));
	},

	insert : function() {
		// Insert the contents from the input into the document		
		tinyMCEPopup.getWindowArg('callback')(this.getFieldsFromForm());
		
		tinyMCEPopup.close();
	},
	
	setFormFromString : function(fields) {
		$('#extentid').val(fields.extent);
		$('#unitid').val(fields.unit);
		$('#reasonid').val(fields.reason);
	},

	getFieldsFromForm : function() {
		var ret = {};
		ret.extent = $('#extentid').val();
		ret.unit = $('#unitid').val();
		ret.reason = $('#reasonid').val();
		return ret;
	}
	
};

tinyMCEPopup.onInit.add(GapDialog.init, GapDialog);
