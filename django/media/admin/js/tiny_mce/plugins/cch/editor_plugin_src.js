(function() {
    // Load plugin specific language pack
    //tinymce.PluginManager.requireLangPack('cch');
    // TODO: prevent overlaps (but not nesting)
    // TODO: p within divs

    tinymce.create('tinymce.plugins.CCHPlugin', {
        /**
         * Initializes the plugin, this will be executed after the plugin has been created.
         * This call is done before the editor instance has finished it's initialization so use the onInit event
         * of the editor instance to intercept that event.
         *
         * @param {tinymce.Editor} ed Editor instance that the plugin is initialized in.
         * @param {string} url Absolute URL to where the plugin is located.
         */
        init : function(ed, url) {
            var buttons = [
                {'name': 'Author', 'class_name': 'tei-author', 'unique': 0, 'color': 0x800000}, 
                {'name': 'Editor', 'class_name': 'tei-editor', 'unique': 0, 'color': 0xFFA500}, 
                {'name': 'TitleArticle', 'class_name': 'tei-title teia-level__a', 'unique': 1, 'color': 0x0000FF}, 
                {'name': 'TitleMonograph', 'class_name': 'tei-title teia-level__m', 'unique': 1, 'color': 0x0000FF}, 
                {'name': 'Date', 'class_name': 'tei-date', 'unique': 1, 'color': 0x008000} 
                //{'name': 'Unmark', 'class_name': 'NONE', 'unique': false}
            ];

            /*
             * <supplied reason="illegible">le</supplied>
             *                     <=>
             * <div class="tei-supplied teia-reason__illegible">le</div>
             */
            var m_teiButtons = {
                'code': {'name': 'Code', 'class_name': 'tei-div teia-type__code', 'color': 0x800000, 'image': 'code2.gif', 'block': 1}, 
                'book': {'name': 'Book', 'class_name': 'tei-div teia-type__book', 'color': 0x800000, 'image': 'book4.gif', 'block': 1}, 
                'chap': {'name': 'Chapter', 'class_name': 'tei-div teia-type__chapter', 'color': 0x800000, 'image': 'chapter3.gif', 'block': 1}, 
                'prol': {'name': 'Prologue', 'class_name': 'tei-div teia-type__prologue', 'color': 0x800000, 'image': 'prologue2.gif', 'block': 1},
                'div': {'name': 'Division', 'class_name': 'tei-div inline', 'color': 0x800000, 'image': 'division2.gif'},  
                'ttl': {'name': 'Title', 'class_name': 'tei-head', 'color': 0x008000, 'block': 0, 'image': 'title2.gif'}, 
                'rub': {'name': 'Rubric', 'class_name': 'tei-head', 'color': 0x008000, 'block': 0, 'image': 'rubric4.gif'}, 
                'fgn': {'name': 'Foreign', 'class_name': 'tei-foreign', 'color': 0x008000, 'image': 'txt-foreign.png'}, 
                'add': {'name': 'Added', 'class_name': 'tei-add', 'color': 0x008000, 'image': 'txt-add.gif'}, 
                'del': {'name': 'Deleted', 'class_name': 'tei-del', 'color': 0x008000, 'image': 'txt-del.gif'},
                'gap': {'name': 'Gap', 'class_name': 'tei-gap', 'color': 0x008000, 'image': 'txt-gap.gif', 'empty': '[Gap]', 'custom_command': 1},
                'sup': {'name': 'Supplied', 'class_name': 'tei-supplied', 'color': 0x008000, 'image': 'txt-supplied.gif'},
                'pb': {'name': 'PageBreak', 'class_name': 'tei-pb', 'color': 0x808080, 'image': 'pagebreak.gif', 'empty': '[PB]', 'custom_command': 1, 'display_name': 'Page break'},
                'link': {'name': 'Link', 'class_name': 'tei-link', 'color': 0x000080, 'image': 'link3.gif', 'custom_command': 1, 'display_name': 'Reference to another text'},
                'app': {'name': 'Apparatus', 'class_name': 'tei-app', 'color': 0x008000, 'image': 'apparatus.gif', 'custom_command': 1, 'empty': '[A]', 'display_name': 'Critical apparatus'}
            };
            
            for (btnid in m_teiButtons) {
                m_teiButtons[btnid].id = btnid;
            }
            
            // load custom css file
            ed.onInit.add(function() {
                if (ed.settings.content_css !== false) {
                    ed.dom.loadCSS(url + "/css/buttons.css");
                    ed.dom.loadCSS(url + "/css/custom.css");
                }
            });
            
            function divSelection(ed, div_class_name, remove_double_space, user_transform) {
                // properties:
                //    # remove all existing mark-up inside the selection
                //    # remove spans with same class in the editor
                //    # remove spans with same class overlapping this element

                // save selection
                if (ed.selection.isCollapsed()) return;
                
                var bm = ed.selection.getBookmark();
                
                var sel_cont = ed.selection.getContent();

                if (remove_double_space !== null && remove_double_space) {
                    sel_cont = sel_cont.replace(/(&nbsp;| |\xA0)+/g, ' ');
                }
                // Now <p>&nbsp;</p> -> <p> </p>
                // And we must reverse this process otherwise the empty lines won't appear
                sel_cont = sel_cont.replace(/<p> <\/p>/g, '<p>&nbsp;</p>');
                
                // removeAllSpans(ed, div_class_name);
                
                // remove all the elements in the current selection
                sel_cont = sel_cont.replace(/<\/?span[^>]*\>/g, '');
                sel_cont = sel_cont.replace(/<\/?div[^>]*\>/g, '');
                
                if (user_transform !== null) sel_cont = user_transform(sel_cont);
                
                ed.selection.setContent('<div class="'+div_class_name+'">' + sel_cont + '</div>');
                
                // restore selection
                // ed.selection.moveToBookmark(bm);                
            }

            function spanSelection(ed, span_class_name, unique) {
                // properties:
                //    # remove all existing mark-up inside the selection
                //    # remove spans with same class in the editor
                //    # remove spans with same class overlapping this element
                if (ed.selection.isCollapsed()) return;

                if (unique === null) unique = false;
            
                unmarkWithinAndThroughSelection();
                
                if (unique) removeAllSpans(ed, span_class_name);
                var sel_cont = ed.selection.getContent();                
                ed.selection.setContent('<span class="'+span_class_name+'">' + sel_cont + '</span>');                
            }
            
            function removeAllSpans(ed, span_class_name) {
                ed.dom.remove(ed.dom.select('span.'+span_class_name), true);
            }

            // ---

            function unmark(span_only) {
                if (span_only === null) span_only = false;
                for (var node = ed.selection.getNode(); node !== null; node = node.parentNode) {
                    if (node.attributes && node.attributes.getNamedItem("class") && node.attributes.getNamedItem("class").value.match(/^tei-/)) {
                        if (span_only && node.tagName != 'SPAN') {
                            break;
                        }
                        // found an element with cch class
                        // remove all the children with cch class
                        // $(node).find('[class|=cch]').each(function(){ed.dom.remove(this,true)});
                        $(node).find('[class|=tei]').each(function(){ed.dom.remove(this,true);});
                        // remove the element
                        ed.dom.remove(node, true);
                        break;
                    }
                }            
            }

            function unmarkWithinAndThroughSelection() {
                var bm = ed.selection.getBookmark();
                
                ed.selection.collapse();
                unmark(true);
                ed.selection.moveToBookmark(bm);                
                bm = ed.selection.getBookmark();
                
                ed.selection.collapse(true);
                unmark(true);                                                
                ed.selection.moveToBookmark(bm);                
                bm = ed.selection.getBookmark();

                // remove all the elements in the current selection
                var sel_cont = ed.selection.getContent();
                sel_cont = sel_cont.replace(/<[^>]*>/g, '');
                ed.selection.setContent(sel_cont);
                ed.selection.moveToBookmark(bm);
            }
            
            function clear_surrounding_readings() {
                // st 
                // <span class="tei-app teia-side__start">{</span>
                // critical apparatus
                // <span class="tei-app teia-side__end">
                //        <span class="tei-readings">[["reading1","W1","W4"]]</span>
                //        }
                // </span> 1
                
                // find the next teia-side__start and the next teia-side__end
                // can we use the dom to do this?? no systematic and simple way to find the readings elements from where we are
                // we need to parse the document as a string rather than a dom tree.
                // 
                
                // 
                // [fds{afs] fdsaf } fsdkfkads
            }

            // UNMARK
            
            // remove the first parent element with a class="tei-X" around the selection
            ed.addCommand('mceCCHUnmark', function() {
                unmark(true);
            });
            ed.addButton('CCHunmark', {
                title : 'cch.unmark',
                cmd : 'mceCCHUnmark',
                image : url + '/img/eraser2.gif'
            });

            // remove the first parent element with a class="tei-X" around the selection
            ed.addCommand('mceCCHClear', function() {
                clear();
            });
            ed.addButton('CCHclear', {
                title : 'Clear mark-up',
                cmd : 'mceCCHClear',
                image : url + '/img/eraser2.gif'
            });
            
            // ----------------------
            //         TEI BUTTONS
            // ----------------------
            
            // SPECIAL COMMANDS
            
            ed.addCommand('mceCCHDivNumber', function(ui, params) {
                ed.windowManager.open({
                    file : url + '/div_number.htm',
                    width : 320,
                    height : 150,
                    inline : 1
                }, {
                    plugin_url : url, // Plugin absolute URL
                    // Custom arguments
                    params : params,
                });
            });

            ed.addCommand('mceTEIGap', function(ui, params) {
                // <gap extent="1" unit="essay" reason="sampling"/>
                // 'reason' is not currently used
                
                if (!ed.selection.isCollapsed()) return;

                var fields = {reason: '', unit: 'character', extent: '1'};
                
                // read existing readings around the cursor
                var to_update = null;
                var node = ed.selection.getNode();
                if (node !== null && node.nodeType === 1 && $(node).hasClass('cch-gap')) {
                    to_update = $(node);
                    var classes = $(node).attr('class');
                    fields.extent = get_value_from_classes(classes, 'extent', '');
                    fields.reason = get_value_from_classes(classes, 'reason', '');
                    fields.unit = get_value_from_classes(classes, 'unit', 'character');
                }
                
                // open the popup, pass the table of MSS and the existing readings 
                ed.windowManager.open({
                    file : url + '/gap.htm',
                    width : 300,
                    height : 150,
                    inline : 1
                }, {
                    plugin_url : url, // Plugin absolute URL
                    fields: fields,
                    
                    // Custom arguments
                    params : params,
                    // Callback where we update the XHTML
                    callback: function(fields) {
                        // insert the two elements
                        var new_classes = 'cch-gap tei-gap teia-unit__' + encodeURI(fields.unit) + ' teia-extent__' + encodeURI(fields.extent);
                        if (to_update) {
                            to_update.attr('class', new_classes);
                        } else {
                            ed.selection.setContent('<span class="' + new_classes + '">[Gap]</span>');
                        }
                    }
                });
            });

            ed.addCommand('mceTEIPageBreak', function(ui, params) {
                // <gap extent="1" unit="essay" reason="sampling"/>
                // 'reason' is not currently used
                
                if (!ed.selection.isCollapsed()) return;

                var fields = {witid: '', loc: ''};
                
                // read existing readings around the cursor
                var to_update = null;
                var node = ed.selection.getNode();
                if (node !== null && node.nodeType === 1 && $(node).hasClass('cch-pb')) {
                    to_update = $(node);
                    var classes = $(node).attr('class');
                    fields.witid = get_value_from_classes(classes, 'witid', '');
                    fields.loc = get_value_from_classes(classes, 'loc', '');
                }
                
                // open the popup, pass the table of MSS and the existing readings 
                ed.windowManager.open({
                    file : url + '/page_break.htm',
                    width : 300,
                    height : 160,
                    inline : 1
                }, {
                    plugin_url : url, // Plugin absolute URL
                    fields: fields,
                    witnesses: g_page_break_witnesses,
                    
                    // Custom arguments
                    params : params,
                    // Callback where we update the XHTML
                    callback: function(fields) {
                        // insert the two elements
                        var new_classes = 'cch-pb tei-pb teia-witid__' + encodeURI(fields.witid) + ' teia-loc__' + encodeURI(fields.loc);
                        if (to_update) {
                            to_update.attr('class', new_classes);
                        } else {
                            ed.selection.setContent('<span class="' + new_classes + '">[PB]</span>');
                        }
                    }
                });
            });

            
            ed.addCommand('mceTEIApparatus', function(ui, params) {
                var readings = '';
                // TODO: remove space from the selection.
                // TODO: exclude silly cases: CA on empty selection AND not inside CA
                
                // read existing readings around the cursor
                var to_update = null;
                var node = ed.selection.getNode();
                if (node !== null && node.nodeType === 1 && $(node).hasClass('cch-app')) {
                    //to_update = $(node).children('span[class=tei-readings]');
                    to_update = $(node);
                    //readings = to_update.html();
                    var classes = $(node).attr('class');
                    readings = classes.replace(/^.*teia-readings__(\S*).*$/gi, '$1');
                    if (readings.length == classes.length) {
                        readings = '';
                    } else {
                        readings = decodeURI(readings);
                    }
                }
                
                if ((readings == '') && ed.selection.getContent({format : 'text'})) {
                    readings = $.toJSON([ed.selection.getContent({format : 'text'}), []]);                    
                }
                
                if (readings != '') {
                    var win = {handle: null};
                    // open the popup, pass the table of MSS and the existing readings 
                    ed.windowManager.open({
                        file : url + '/crit_app.htm',
                        width : 620,
                        height : 250,
                        inline : 1
                    }, {
                        plugin_url : url, // Plugin absolute URL
                        // Custom arguments
                        params : params,
                        table: $('#ca-table-div').html(),
                        readings: readings,
                        // Callback where we update the XHTML
                        callback: function(readings) {
                            // insert the two elements
                            var new_classes = 'cch-app tei-app teia-readings__' + encodeURI(readings);
                            if (to_update) {
                                to_update.attr('class', new_classes);
                            } else {
                                var sel_cont = ed.selection.getContent();
                                ed.selection.setContent(sel_cont+'<span class="' + new_classes + '">' + m_teiButtons['app'].empty + '</span>');
                            }
                        }
                    });
                }

            });

            ed.addCommand('mceTEILink', function(ui, params) {
                var info = {textid: 0, text_typeid: 0, rel: '', from: '0.0.0.0.0', to: '0.0.0.0.0'};
                // TODO: remove space from the selection.
                // TODO: exclude silly cases: CA on empty selection AND not inside CA
                
                // read existing readings around the cursor
                var to_update = null;
                // use current link or the current selection if none are defined we leave
                var node = ed.selection.getNode();
                var selection = ed.selection.getContent();
                if (node !== null && node.nodeType === 1 && $(node).hasClass('cch-link')) {
                    //to_update = $(node).children('span[class=tei-readings]');
                    to_update = $(node);
                    //readings = to_update.html();
                    var classes = $(node).attr('class');
                    //range = classes.replace(/^.*teia-range__(\S*).*$/gi, '$1');
                    info.textid = get_value_from_classes(classes, 'textid', '0');
                    info.text_typeid = get_value_from_classes(classes, 'text_typeid', '0');
                    info.rel = get_value_from_classes(classes, 'rel', '0');
                    info.from = get_value_from_classes(classes, 'from', '');
                    info.to = get_value_from_classes(classes, 'to', '');
                    // if (info.range.length) info.range = decodeURI(info.range);
                    selection = to_update.html();
                }
                
                if (selection.length) {
                    var win = {handle: null};
                    // open the popup, pass the table of MSS and the existing readings 
                    ed.windowManager.open({
                        file : url + '/link.htm',
                        width : 620,
                        height : 300,
                        inline : 1
                    }, {
                        plugin_url : url, // Plugin absolute URL
                        // Custom arguments
                        params : params,
                        witnesses: g_witnesses_list,
                        versions: g_versions_list,
                        info: info,
                        // Callback where we update the XHTML
                        callback: function(info) {
                            // insert the two elements
                            var new_classes = 'cch-link tei-link teia-text_typeid__' + info.text_typeid + ' teia-textid__' + info.textid + ' teia-from__' + info.from + ' teia-to__' + info.to + ' teia-rel__' + info.rel;
                            if (to_update) {
                                to_update.attr('class', new_classes);
                            } else {
                                ed.selection.setContent('<span class="' + new_classes + '">' + selection + '</span>');
                            }
                        }
                    });
                }

            });

            function get_value_from_classes(classes, field_name, default_value) {
                var ret = classes.replace(new RegExp('^.*teia-' + field_name + '__(\\S*).*$', 'gi'), '$1');
                return (ret.length == classes.length) ? default_value : decodeURI(ret); 
            }
                        
            // NORMAL STUFF

            function getButtonInfoFromNode(node) {
                var ret = null;
                if (node.nodeType == 1) {
                    var cl = node.getAttribute('class');
                    if (cl) {
                        var btnid = cl.replace(/^cch-([^\s]+).*/, '$1');
                        if (btnid) {
                            ret = m_teiButtons[btnid];
                        }
                    }
                }
                return ret;
            }

            function clear(anode) {
                var node = anode ? anode : ed.selection.getNode();
                if (node !== null && node.nodeType === 1 && node.id !== 'tinymce') {
                    if (node.parentNode.id == 'tinymce') {
                        // we are about to remove a top level element
                        // convert it into a <p> instead
                        $(node).replaceWith($('<p>'+node.innerHTML+'</p>'));
                    } else {
                        if (node.tagName.toUpperCase() == 'P') {
                            // leave p's alone, look at the parent instead
                            clear(node.parentNode);
                        } else {
                            var btnInfo = getButtonInfoFromNode(node);
                            keep_children = !(btnInfo && btnInfo.empty);
                            ed.dom.remove(node, keep_children);
                        }
                    }
                } 
            }
            
            function getUniqueid() {
                return 'i'+((new Date()).getTime()).toString(16) + (Math.floor(Math.random()*1000)).toString(16);            
            }
            
            function teiButton(btnid) {
                // save selection
                buttonInfo = m_teiButtons[btnid]; 
                if (ed.selection.isCollapsed() != (buttonInfo.empty ? true: false)) return;
                
                //var bm = ed.selection.getBookmark();
                
                var sel_cont = ed.selection.getContent();

                // remove spaces on each side of the selection. It will then be moved outside the selection (see spaces[])
                l = sel_cont.length;
                spaces = ['', ''];
                sel_cont = sel_cont.replace(/\s+$/, '');
                if (l > sel_cont.length) spaces[1] = ' ';

                l = sel_cont.length;
                sel_cont = sel_cont.replace(/^\s+/, '');
                if (l > sel_cont.length) spaces[0] = ' ';

                if (buttonInfo.empty) sel_cont = buttonInfo.empty;
                
                tag = buttonInfo.block ? 'div' : 'span';
                // todo: what if the selection contains ps already?
                // what if it contains a mix of ps and raw text?
                if (buttonInfo.block) sel_cont = '<p>' + sel_cont + '</p>'; 
                ed.selection.setContent(spaces[0]+'<'+tag+' class="'+'cch-'+btnid+' '+buttonInfo['class_name']+'" id='+getUniqueid()+'>' + sel_cont + '</'+tag+'>'+spaces[1]);
                
                // restore selection
                // ed.selection.moveToBookmark(bm);                
            }

            function registerButton(btnid) {
                buttonInfo = m_teiButtons[btnid];
                var name = buttonInfo.name;
                var namelc = name.toLowerCase();
                if (!buttonInfo.custom_command) {
                    ed.addCommand('mceTEI'+name, function() { teiButton(btnid); });
                }
                var image = 'qmark.gif';
                var display_name = buttonInfo.display_name ? buttonInfo.display_name : name;
                if (buttonInfo.image !== null) image = buttonInfo.image;
                ed.addButton('TEI'+namelc, {
                    // title : 'cch.'+namelc,
                    title : display_name,
                    cmd : 'mceTEI'+name,
                    image : url + '/img/'+image
                });
            }

            for (btnid in m_teiButtons) {
                registerButton(btnid);
            }

            // BILIOGRAPHY BUTTONS
            
            ed.addCommand('mceCCHAuthor', function() { spanSelection(ed, 'tei-author'); });
            ed.addCommand('mceCCHEditor', function() { spanSelection(ed, 'tei-editor'); });
            ed.addCommand('mceCCHTitleArticle', function() { spanSelection(ed, 'tei-title teia-level__a', true); });
            ed.addCommand('mceCCHTitleMonograph', function() { spanSelection(ed, 'tei-title teia-level__m', true); });
            ed.addCommand('mceCCHDate', function() { spanSelection(ed, 'tei-date', true); });

            // Register the command and button for each control
            for (i = 0; i < buttons.length; i++) {
                var name = buttons[i].name;
                var namelc = name.toLowerCase(); 
                ed.addButton('CCH'+namelc, {
                    title : 'cch.'+namelc,
                    cmd : 'mceCCH'+name,
                    image : url + '/img/'+namelc+'.gif'
                });
            }
            
            // Highlight and enable buttons depending on the current selection
            ed.onNodeChange.add(function(ed, cm, n) {
                var inherited_classes = '|';
                for (var node = n; node !== null; node = node.parentNode) {
                    inherited_classes += ed.dom.getAttrib(node, 'class')+'|';
                }
                
                var has_selection = !ed.selection.isCollapsed();
                for (i = 0; i < buttons.length; i++) {
                    var name = buttons[i].name;
                    var namelc = name.toLowerCase(); 
                    b = cm.get('CCH'+namelc);
                    if (b) {
                        b.setDisabled(!has_selection);
                        b.setState('Selected', inherited_classes.indexOf(buttons[i].class_name) != -1);
                    }
                }
                
                cm.setDisabled('CCHunmark', !ed.selection.isCollapsed());
            });
            
        },
        
        /**
         * Creates control instances based in the incoming name. This method is normally not
         * needed since the addButton method of the tinymce.Editor class is a more easy way of adding buttons
         * but you sometimes need to create more complex controls like listboxes, split buttons etc then this
         * method can be used to create those.
         *
         * @param {String} n Name of the control to create.
         * @param {tinymce.ControlManager} cm Control manager to use inorder to create new control.
         * @return {tinymce.ui.Control} New control instance or null if no control was created.
         */
        createControl : function(n, cm) {
            return null;
        },

        /**
         * Returns information about the plugin as a name/value array.
         * The current keys are longname, author, authorurl, infourl and version.
         *
         * @return {Object} Name/value array containing information about the plugin.
         */
        getInfo : function() {
            return {
                longname : 'CCH plugin',
                author : 'Geoffroy Noel',
                authorurl : 'http://www.kcl.ac.uk/schools/humanities/depts/cch',
                infourl : 'http://www.kcl.ac.uk/schools/humanities/depts/cch',
                version : "1.0"
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('cch', tinymce.plugins.CCHPlugin);
})();
