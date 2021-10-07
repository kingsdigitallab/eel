tinyMCEPopup.requireLangPack();

var LinkDialog = {
	init : function() {
		// load the list of witnesses and editions
		this.m_info = tinyMCEPopup.getWindowArg('info');
		//
		var f = document.forms[0];
		// add range of numbers for the drop downs 
		$(".sel-num").each(function() {
			var i;
			var options = '';
			var max = 5;
			if (this.id == "schapterid" || this.id == "echapterid") max = 100;
			if (this.id == "sdivisionid" || this.id == "edivisionid") max = 30;
			for (i = 1; i <= max; i++) {
				options = options + '<option value="' + i + '">' + i + '</option>';
			}
			$(this).append(options);
		});
		this.initForm();
		var self = this;
		$('#text_typeidid').change(function() {self.refreshTextOptions()});
		self.refreshTextOptions();
		
		$('#textidid').change(function() {self.onSelectText()});
		
		$('#location-typeid').change(function() {self.onChangeLocationType()});
	},
	
	onSelectText: function() {
		this.m_info.textid = $('#textidid').val();
		var t= 0;
	},

	insert : function() {
		// Insert the contents from the input into the document		
		tinyMCEPopup.getWindowArg('callback')(this.getFieldsFromForm());
		tinyMCEPopup.close();
	},
	
	refreshTextOptions: function() {
		var options = tinyMCEPopup.getWindowArg($('#text_typeidid').val().substr(0,1) == 'w' ? 'witnesses' : 'versions');
		var options_html = '';
		for (var i in options) {
			options_html = options_html + '<option value="' + options[i][0] + '">' + options[i][1] + '</option>';
		}
		$('#textidid').html(options_html);
		$('#textidid').val(this.m_info.textid);
	},
	
	onChangeLocationType: function() {
		var location_type = $('#location-typeid').val();
		$('#locationid').toggle(location_type > 0);
		$('#range-endid').toggle(location_type > 1);
		
		if (location_type < 2) this.setLocation(null, '#range-endid');
		if (location_type < 1) this.setLocation(null, '#range-startid');
		
		$('#cell-from').html((location_type == 2) ? 'from' : 'at');
	},
	
	initForm : function() {
		$('#text_typeidid').val(this.m_info.text_typeid);
		$('#textidid').val(this.m_info.textid);
		$('#relationshipid').val(this.m_info.rel);
		this.setLocation(this.m_info.from, '#range-startid');
		this.setLocation(this.m_info.to, '#range-endid');
		
		if (this.m_info.from.search(/[^0.]/) == -1) {
			$('#location-typeid').val(0);
		} else {
			if (this.m_info.to.search(/[^0.]/) == -1) {
				$('#location-typeid').val(1);
			} else {
				$('#location-typeid').val(2);
			}
		};
		
		this.onChangeLocationType();
	},
	
	setLocation: function(location, rowid) {
		if (!location) location = '0.0.0.0.0';
		location = location.split('.');
		var i = 0;
		$(rowid + ' select').each(function() {
			$(this).val(location[i]);
			i++;
		});
	},

	getFieldsFromForm : function() {
		var ret = {};
		ret.text_typeid = $('#text_typeidid').val();
		ret.textid = $('#textidid').val();
		ret.rel = $('#relationshipid').val();
		ret.from = '';
		$('#range-startid select').each(function() {
			if (ret.from.length) ret.from += '.';
			ret.from += $(this).val();
		});
		ret.to = '';
		$('#range-endid select').each(function() {
			if (ret.to.length) ret.to += '.';
			ret.to += $(this).val();
		});
		ret.rel = $('#relationshipid').val();
		return ret;
	}
	
};

tinyMCEPopup.onInit.add(LinkDialog.init, LinkDialog);
