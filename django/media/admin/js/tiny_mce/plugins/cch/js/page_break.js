tinyMCEPopup.requireLangPack();

var PageBreakDialog = {
	init : function() {
		var f = document.forms[0];
		this.m_fields = tinyMCEPopup.getWindowArg('fields');
		//this.setFormFromString();
		this.initSelects(tinyMCEPopup.getWindowArg('witnesses'));
	},

	insert : function() {
		// Insert the contents from the input into the document		
		tinyMCEPopup.getWindowArg('callback')(this.getFieldsFromForm());
		
		tinyMCEPopup.close();
	},
	
	setFormFromString : function() {
		//$('#witidid').val(this.m_fields.witid);
		//$('#locid').val(this.m_fields.loc);
	},

	getFieldsFromForm : function() {
		var ret = {};
		ret.witid = $('#witidid').val();
		ret.loc = $('#locid').val();
		return ret;
	},
	
	initSelects: function (witnesses) {
		var witnesses_html = '';
		for (i in witnesses) {
			var sel = (witnesses[i].id == this.m_fields.witid) ? 'selected="selected"' : '';
			witnesses_html += '<option '+sel+' value="' + witnesses[i].id + '">' + witnesses[i].name + '</option>';
		}
		$('#witidid').html(witnesses_html);
		
		document.getElementById('witidid').m_defaultid = this.m_fields.witid;
		document.getElementById('locid').m_defaultid = this.m_fields.loc;

		//
		function refresh_page_list() {
			var pg_html = '';
			var witid = $('#witidid').val();
			var locid = document.getElementById('locid').m_defaultid; 
			for (i in witnesses) {
				if (witnesses[i].id == witid) {
					var pages = witnesses[i].pages;
					for (j in pages) {
						var sel = (pages[j] == locid) ? 'selected="selected"' : '';
						pg_html += '<option '+sel+' value="' + pages[j] + '">' + pages[j] + '</option>';
					}
					break;
				}
			}
			$('#locid').html(pg_html)
		}
		
		$('#witidid').click(refresh_page_list);
		refresh_page_list();
	}
	
};

tinyMCEPopup.onInit.add(PageBreakDialog.init, PageBreakDialog);
