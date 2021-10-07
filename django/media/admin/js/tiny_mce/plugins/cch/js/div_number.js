tinyMCEPopup.requireLangPack();

var DivNumberDialog = {
	init : function() {
		var f = document.forms[0];
		
		// Get the selected contents as text and place it in the input
		//f.someval.value = tinyMCEPopup.editor.selection.getContent({format : 'text'});
		//f.somearg.value = tinyMCEPopup.getWindowArg('some_custom_arg');
		f.number.value = this.getParamVal('number',  0);
	},

	insert : function() {
		// Insert the contents from the input into the document
		//tinyMCEPopup.editor.execCommand('mceInsertContent', false, document.forms[0].someval.value);
		// call the callback with the result
		
		var n = parseInt(document.forms[0].number.value);
		if (isNaN(n) || n < 0 || n > 1000) {
			$('#number-error').css('display', 'block');
			return false;
		}
		var f = this.getParamVal('callback', function() {});
		f(n);
		
		tinyMCEPopup.close();
	},
	
	getParamVal : function(key, def) {
		var ret = tinyMCEPopup.getWindowArg('params');
		if (ret != null) {
			ret = ret[key];
		} else {
			ret = def;
		}

		return ret;
	}
};

tinyMCEPopup.onInit.add(DivNumberDialog.init, DivNumberDialog);
