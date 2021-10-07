/*
 * Author:		geoffroy.noel@kcl.ac.uk
 * Requires:	jquery.js
 * Tested with:	FF 3, IE 7, SAFARI, OPERA
 * Usage:
 * 
 * [TODO]
 * 
 */

var g_autocomp_timeout = 7000;
var g_autocomp_limit = 10;

function autoCompleteTextBox() {
	
	this.result = null;
	this.selTable = null;
	this.txtQuery = null;
	this.selResult = null;
	this.imgQuery = null;
	this.div = null;
	this.focus_transition = false;
	this.tinyMce = null;
	this.tinyMceBm = null;
	this.tinyMceHasFocus = false;
	this.onSelectCallBack = null;
	this.has_focus = 0;
	this.focused_element = null;
	this.replaced_select = null;
	this.m_references = [['bibliographic_entry', 'Reference'], ['person', 'Person'], ['text', 'Text'], ['glossary_term', 'Glossary']];

	this.createWidget = function(parentElement, references) {
		this.attachToWidget(null, null, null, parentElement, null, references);
	}
	
	this.setReferences = function(references) {
		if (references != null) {
			this.m_references = references;
		}
	}
	
	this.addToTinyMce = function(tinyMceEditor, references) {
		var td = document.createElement('td');
		var td2 = $('#'+tinyMceEditor.getContainer().id+' .mceToolbarEnd:last').before(td);
		//td = td2;
		this.createWidget(td, references);
		this.tinyMce = tinyMceEditor;
		var t = this;
		// FF
		//$(this.tinyMce.getDoc()).bind('blur', function(){t.saveTinyMceSelection();});
		//$(this.tinyMce.getDoc()).bind('blur', function(){t.saveTinyMceSelection();});
		// IE
		if ($.browser.msie) {
			// When you click any element outside the wysiwyg, first IE7 triggers a 'mousedown' event on the element then the wysiwyg's selection is lost then the wysiwyg's iframe triggers the 'blur' event.
			// We bookmark the selection when the widget is clicked on and restore it just before before changing it.
			$(this.tinyMce.getContainer()).find('iframe').bind('blur', function(){t.tinyMceHasFocus=false;});
			$(this.tinyMce.getContainer()).find('iframe').bind('focus', function(){t.tinyMceHasFocus=true;});
			$(this.txtQuery).mousedown(function(){t.saveTinyMceSelection();});
			// mouse down occurs before onclick
			$(this.imgQuery).mousedown(function(){t.saveTinyMceSelection();});
			$(this.selTable).mousedown(function(){t.saveTinyMceSelection();});
		}
	}

	this.addToForeignKey = function(foreignKeyName, searchModel, label) {
	    this.attachToWidget(null, null, searchModel, '#ac_parent_'+foreignKeyName, label);
        var rel = document.getElementById('id_'+foreignKeyName);
	    var t = this;
	    t.replaced_select = rel;
	    this.setSelectCallBack( 
	        function(record) {
	            rel.options[1] = new Option(record[1], record[0]);
	            for (var i = rel.length - 1; i > 1; i--) {
	                rel.remove(i);
	            }
	            rel.selectedIndex = 1;
	            rel.options[1].selected = true;
	    		t.txtQuery.focus();
	            
	            return record[1];
	        }	        
	    );
	    // dismissAddAnotherPopup() will populate the FK field with the new record without triggering an onchange() event.
	    // only way to intercept it is to hook the function.
	    $.aop.after( {target: window, method: 'dismissAddAnotherPopup'}, function() {t.setValue(rel.options[rel.selectedIndex].text);});
	    this.addFocusCue();
	}
	
	// this function adds detection for when the widget has the focus
	// manual edition of the text in the box will be reverted when the widget looses focus
	this.addFocusCue = function() {
		var t = this;
	    var on_blur = function() {
	    	var val = '';
	        if (t.replaced_select && t.replaced_select.selectedIndex >= 0) {
	        	val = t.replaced_select.options[t.replaced_select.selectedIndex].text;
	        }
	        t.setValue(val);
	    };

		$(this.txtQuery).bind('blur', on_blur);
		$(this.txtQuery).bind('keydown', function(){$(t.txtQuery).toggleClass('autocomp-changed', true);});
	}
	
	this.attachToWidget = function(txtQueryid, selResultid, selTableid, parentElement, initialValue, references) {
		this.setReferences(references);
		var parent = this.getElementFromParam(parentElement);
		this.selTable = this.getElementFromParam(selTableid);
		if (parent != null && this.selTable == null) {
			this.selTable = this.createElement({'parent': parent, 'tag': 'select', 'options': this.m_references, 'attrs': [['class', 'autocomp-model']]});
		}
		this.txtQuery = this.getElementFromParam(txtQueryid);
		if (parent != null && this.txtQuery == null) {
			this.div = this.createElement({'parent': parent, 'tag': 'div', 'attrs': [['class', 'autocomp-querydiv']]});
			this.imgQuery = this.createElement({'parent': this.div, 'tag': 'span', 'attrs': [['class', 'autocomp-imgquery']]});
			this.txtQuery = this.createElement({'parent': this.div, 'tag': 'input', 'attrs': [['class', 'autocomp-query'], ['type', 'text']]});
			var t = this;
			$(this.imgQuery).click(function(){t.txtQuery.focus(); return false;});
		}
		this.selResult = this.getElementFromParam(selResultid);
		if (parent != null && this.selResult == null) {
			this.createElement({'parent': this.div ? this.div : parent, 'tag': 'br'}); 
			this.selResult = this.createElement({'parent': this.div ? this.div : parent, 'tag': 'select', 'options': [['-1', 'No result']], 'attrs': [['class', 'autocomp-result'], ['size', '5']]});
		}
		this.txtQuery.ac = this;
		if (initialValue != null) this.setValue(initialValue);
		this.selResult.ac = this;
		$(this.txtQuery).keydown(this.queryKeyPressed);
		this.txtQuery.onblur = this.queryOnBlur;
	}
	
	this.setValue = function(value) {
		if (value.match(/^-+$/)) value = '';
		this.txtQuery.value = value;
		$(this.txtQuery).toggleClass('autocomp-changed', false);
	}
	
	this.setSelectCallBack = function(onSelectCallBack) {
		this.onSelectCallBack = onSelectCallBack; 
	}
	
	this.saveTinyMceSelection = function() {
		// IE hack. when mce loses the focus, the selection is lost. We bookmark it just before the focus is moved to our widget.
		if (this.tinyMce && this.tinyMceHasFocus) {
			this.tinyMceBm = this.tinyMce.selection.getBookmark();
		}
	}
	
	this.createElement = function(info) {
		var ret = document.createElement(info.tag);
		if ('options' in info) {
			for (var i = 0; i < info.options.length; i++) {
				ret.options[i] = new Option(info.options[i][1], info.options[i][0]);
			}
		}
		if ('attrs' in info) {
			for (var i = 0; i < info.attrs.length; i++) {
				$(ret).attr(info.attrs[i][0], info.attrs[i][1]);
			}
		}
		if ('parent' in info) {
			info.parent.appendChild(ret);
		}
		return ret;
	}
	
	this.getElementFromParam = function(ret) {
		if (ret != null) {
			ret = (typeof(ret) != 'string') ? ret : ((ret.length > 0 && ret.substring(0,1) == '#') ? document.getElementById(ret.substring(1)) : ret);
		}
		return ret;
	}

	// ----------- EVENTS ------------------
	// note that 'this' is the object triggering the event not autoCompleteTextBox
	
	this.queryKeyPressed = function(e) {
		var ret = true;
		var keynum = window.event ? e.keyCode : (e.which ? e.which : 0);
		if (keynum == 13) {
			this.ac.ajaxGetRecords();
			ret = false;
		}
		if (keynum == 40) {
			// DOWN arrow
			var sel = this.ac.selResult; 
			if (sel != null && sel.size > 0 && sel.style.display == 'inline') {
				this.ac.startFocusTransition();
				sel.focus();
			}
		} else {
			this.ac.hideResult();
		}
		return ret;
	}

	this.queryOnBlur = function() {
		this.ac.hideResult();
	}

	this.selOnBlur = function() {
		this.ac.hideResult();
	}
	
	this.selGetFocus = function() {
		if ($.browser.msie && this.selectedIndex < 0) this.selectedIndex = 0;
		this.ac.stopFocusTransition();
	}

	this.selOnMouseDown = function() {
		this.ac.startFocusTransition();
	}

	this.selKeyPressed = function(e) {
		var ret = true;
		var keynum = window.event ? e.keyCode : (e.which ? e.which : 0);
		if (keynum == 13) {
			// TODO: selection!
			this.ac.selectedRecord();
			ret = false;
		}
		if (keynum == 38) {
			// UP arrow
			if (this.selectedIndex == 0) {
				this.ac.txtQuery.focus();
			}
		}
		if (keynum != 38 && keynum != 40 && keynum != 13 && keynum != 33 && keynum != 34) {
			this.ac.txtQuery.focus();
		}
		return ret;
	}

	this.selOnClick = function() {
		this.ac.selectedRecord();
	}
	
	// --------------------------------------------------

	this.hideResult = function() {
		if (!this.focus_transition) {
			this.selResult.style.display = 'none';
		}
	}
	
	this.startFocusTransition = function() {
		this.focus_transition = true;
	}
	this.stopFocusTransition = function() {
		this.focus_transition = false;
	}
	
	this.selectedRecord = function() {
		var rec = this.result.records[this.selResult.selectedIndex];
		this.txtQuery.focus();
		
		if (this.tinyMce != null) {
			var ed = this.tinyMce;

			ed.focus();
			if (this.tinyMceBm) {
				ed.selection.moveToBookmark(this.tinyMceBm);
			}
			var link_name = '';
			
			if (ed.selection.isCollapsed()) {
				link_name = rec[1];
			} else {
				link_name = ed.selection.getContent();
				//removeAllSpans(ed, span_class_name);
				// remove all the elements in the current selection
				//sel_cont = sel_cont.replace(/<[^>]*>/g, '');
			}
			
			//ed.selection.setContent('<span class="cch-ref ref-'+this.result.content_type+'-'+rec[0]+'">' + link_name + '</span>');
			ed.selection.setContent('<span class="cch-r'+this.getModelName()+' tei-ref teia_type__'+this.getModelName()+' teia_rid__'+rec[0]+'">' + link_name + '</span>');
		}
		
		if (this.onSelectCallBack) {
			var val = this.onSelectCallBack(rec);
			if (val != null) this.setValue(val);
		}
	}

	this.fillListBoxWithSearchResult = function(result, textStatus, errorThrown) {
		if (textStatus == "timeout" || textStatus == "error" || textStatus == "parsererror") {
			this.setValue('ERROR (ajax '+textStatus+')');
			this.result = null;
		} else {
			this.result = result;
			if (result != null) {
				if (result.error.length > 0) {
					this.setValue('ERROR (server '+escape(result.error)+')');
				} else {
					var sel = this.selResult;
					var newsel = null;
					if (sel != null && result.records.length) {
						var newsel = sel.cloneNode(false);
						for (var i = 0; i < result.records.length; i++) {
							newsel.options[i] = new Option(result.records[i][2], i);
						}
			
						var selParent = sel.parentNode;
						selParent.replaceChild(newsel, sel);
						newsel.style.zIndex = 10;
						this.selResult = newsel;
						this.selResult.ac = this;
						this.selResult.onfocus = this.selGetFocus;
						this.selResult.onblur = this.selOnBlur;
						this.selResult.onmousedown = this.selOnMouseDown;
						this.selResult.onclick = this.selOnClick;
						$(this.selResult).keydown(this.selKeyPressed);
						
						newsel.style.display = 'inline';
					}
				}
			}
		}
		this.txtQuery.style.backgroundColor = '';
	}
	
	this.ajaxGetRecords = function() {
		this.txtQuery.style.backgroundColor = 'LightPink';

		//var query_string = "/db/admin/json/search?limit="+g_autocomp_limit+"\x26model="+escape(this.getModelName())+"\x26q="+escape(this.txtQuery.value);
		var query_string = '/db/admin/json/search';
		data = {'limit': g_autocomp_limit, 'model': this.getModelName(), 'q': this.txtQuery.value}
		// if (this.tinyMce == null) query_string += "\x26fmt=rpr";
		if (this.tinyMce == null) data.fmt = "rpr";
		$('#id_query_string').html(query_string);
		$('#id_query_string').attr('href', query_string);	

		var t = this;
		$.ajax({
			async: true,
			type: "GET",
			data: data,
		 	url: query_string,
			success: function(data, textStatus) {
				if (data != null && typeof data == "string" && data.length > 2) { 
					var ret = $.parseJSON(data.substring(1, data.length - 1));
					t.fillListBoxWithSearchResult(ret,textStatus,null);
				} 
			},
			error:function(XMLHttpRequest, textStatus, errorThrown){
				t.fillListBoxWithSearchResult(null,textStatus,errorThrown);
			}
		 });
	}
	
	this.getModelName = function() {
		return (typeof(this.selTable) == 'string') ? this.selTable : this.selTable.value;
	}
}
