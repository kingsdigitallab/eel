/**
 * Text Viewer
 *
 * Description:
 *
 * Requires:
 *      jquery
 *
 * Authors:
 *      Geoffroy Noel
 *
 * Coding conventions:
 *      * variables prefixed with jq_ are jQuery elements.
 *      * variables prefixed with jqs_ are jQuery selectors (or elements).
 * Todo:
 *      * deal with ajax erros
 *
 * Version:
 *      $Id$
 *
 */

/**
 * ----------------------------------
 *              TextViewer
 * ----------------------------------
 */
function TextViewer() {

    this.panels = [];
    this.maxBottom = $(document).height();
    // Initialise this with the key of the text types
    // which will be used to feed the content of the tooltips.
    // The 'anchor' field is an anchor key.
    var jq_tooltip = $('<div id="tooltip"></div>');
    $('body').append(jq_tooltip);
    var jq_user_comments_box = $('#user-comments-box');
    //dm(jq_tooltip);
    this.annotators = {
                        'commentary':   new Annotator(jq_tooltip, 'co', 'commentary', this),
                        'apparatus':    new Annotator(jq_tooltip, 'ca', 'apparatus', this),
                        'user-comments':new AnnotatorComments($('#user-comments-box'), 'uc', 'user-comments', this),
                    };
    // On/off switches which modify the behaviour of the viewer.
    // The key of the switches can be anything you like.
    // If a key matches the key of an annotation source, it will
    // be used to toggle annotation visibility.
    this.switches = {
                        'sync':         false,
                        'commentary':   false,
                        'user-comments':false,
                        'apparatus':    true,
                        'chapter':      true,
                    };

    /*
    this.bindMainControls = function(jqs_permalink) {
        this.jq_permalink = $(jqs_permalink);
        //  event binding
        this.jq_permalink.focus(function() { $(this).select(); });
    }
    */

    this.getSwitch = function(name) {
        return this.switches[name];
    }

    // If called without second argument the switch is left
    // unchanged but the events attached to it are triggered.
    this.setSwitch = function(name, value) {
        if (value != null) this.switches[name] = value;

        if (name == 'chapter') {
            for (i in this.panels) this.panels[i].refreshChapterVisibility();
        }

        this.annotateTexts(name, this.switches[name]);

        return this.switches[name];
    }

    this.toggleSwitch = function(name) {
        return this.setSwitch(name, !this.switches[name]);
    }

    this.onResize = function() {
        for (i in this.panels) this.panels[i].onResize()
    }

    this.bindNewPanel = function(jqs_textType, jqs_textBox, jqs_navChapter, jqs_navPage) {
        this.panels.push(new TextPanel(this, this.panels.length, jqs_textType, jqs_textBox, jqs_navChapter, jqs_navPage));
    }

    this.updatePermalink = function () {
        var hash = '';
        for (i in this.panels) {
            if (i > 0) hash += '/';
            hash += this.panels[i].getPermalink();
        }
        //location.hash = hash;
        history.replaceState(undefined, undefined, '#'+hash)
    }

    this.ready = function() {
        // events binding
        var self = this;
        $(window).bind('resize', function() { self.onResize(); } );
        $(window).bind('scroll', function() { self.onResize(); } );
        for (i in this.panels) this.panels[i].ready();
    }

    this.synchronisePanels = function(referencePanel) {
        // TODO: opt: sync only when the location actually changes
        // not each time we scroll.
        if (!this.getSwitch('sync')) return;
        var locationId = referencePanel.getLocationId();
        var pageNumber = referencePanel.getPageNumber();
        for (i in this.panels) {
            if (this.panels[i] != referencePanel) {
                if (!this.panels[i].syncToLocationId(locationId)) {
                    this.panels[i].syncToPage(pageNumber);
                }
            }
        }
    }

    this.setLowerBoundaryElement = function(jqs_element) {
        this.maxBottom = $(jqs_element).offset().top;
    }

    this.getMaxBottom = function() {
        return this.maxBottom;
    }

    // all types of annotations to one panel
    this.annotateText = function(jq_text, panelIndex) {
        for (var annotatorKey in this.annotators) {
            this.annotators[annotatorKey].annotateText(jq_text, !this.getSwitch(annotatorKey), panelIndex);
        }
    }

    // one type of annotation to all panels
    this.annotateTexts = function(annotatorKey, show) {
        if (this.annotators[annotatorKey]) {
            for (i in this.panels) {
                this.annotators[annotatorKey].annotateText(this.panels[i].textBox, !show, i);
            }
        }
    }

    this.getWitnessid = function() {
        var ret = 0;
        for (i in this.panels) {
            if (this.panels[i].doc_info.witnessid) {
                if (ret) {
                    // more than one witnessid, we can't choose
                    ret = '';
                    break;
                } else {
                    ret = this.panels[i].doc_info.witnessid;
                }
            }
        }
        return ret;
    }

}

/**
 * ----------------------------------
 *              TextPanel
 * ----------------------------------
 */
function TextPanel(viewer, panelIndex, jqs_textType, jqs_textBox, jqs_navChapter, jqs_navPage) {

    this.textType = $(jqs_textType);
    this.textBox = $(jqs_textBox);
    this.navChapter = $(jqs_navChapter);
    this.navPage = $(jqs_navPage);
    this.viewer = viewer;
    this.panelIndex = panelIndex;
    this.beingSynced = false;
    this.locationId = '';
    this.doc_info = {'witnessid': 0, 'chaperisation': 0, 'pagination': 0};
    // if true the permalink will include a reference to
    // the current location in the text
    this.deepPermalink = true;

    this.getSpace = function() {
        return getSpace(this.textBox.parent());
    }

    this.refreshChapterVisibility = function() {
        // this might be slow if there ar a lot of chapters on the page
        // in that can faster techniques might be used:
        // http://www.learningjquery.com/2010/05/now-you-see-me-showhide-performance
        this.textBox.find('.anchor-label-c').toggle(this.viewer.getSwitch('chapter'));

    }

    this.syncToLocationId = function(locationId) {
        //this.dm('sync to location = ' + locationId);
        this.beingSynced = true;
        return this.setLocationId(locationId);
    }

    this.syncToPage = function(pageNumber) {
        //this.dm('sync to page = ' + pageNumber);
        this.beingSynced = true;
        this.scrollToPage(pageNumber);
    }

    this.setLocationId = function(locationId) {
        return this.scrollTextBoxToElement($('#a-'+this.panelIndex+'-'+locationId));
    }

    this.getLocationId = function() {
        //var ret = this.navChapter.val();
        var ret = this.locationId;
        ret = ret.replace(/^a-\d+-/, '');
        return ret;
    }

    this.getPageNumber = function() {
        return this.navPage.val().replace(/\s/g, '');
    }

    this.getPermalink = function() {
        var ret = this.textType.val();
        if (this.deepPermalink) {
            var pos = this.navChapter.val();
            if (pos) ret = ret + '-' + pos.replace(/\s/g, '');
        }
        return ret;
    }

    this.onResize = function() {
        var margin = 20;
        var minHeight = 100;
        var maxHeight = this.viewer.getMaxBottom() - this.textBox.offset().top - margin;
        var panelHeight = $(window).height() - margin - (this.textBox.offset().top - $("html").scrollTop());
        if (panelHeight > maxHeight) panelHeight = maxHeight;
        if (panelHeight < minHeight) panelHeight = minHeight;
        panelHeight = parseInt(panelHeight) + 'px';
        this.textBox.css('height', panelHeight);

        this.onChangeVisibleContent();
    }

    this.onChangeTextType = function() {
        // request the text
        var content = call_django('load_doc', {'doc_key': this.textType.val(), 'panel': this.panelIndex});

        // copy the doc info
        this.doc_info = content.doc_info;
        //this.dm(this.doc_info);

        // display the content in the text-box
        this.textBox.html(content.doc);

        this.applyJQStyles();

        this.refreshChapterVisibility();

        this.annotateText();

        this.onChangeVisibleContent();

        if (!this.deepPermalink) this.viewer.updatePermalink();
    }

    this.annotateText = function() {
        this.viewer.annotateText(this.textBox, this.panelIndex);
    }

    this.applyJQStyles = function() {
        // supplied elements will appear on the line above.
        $('.cch-add').each(function (){
            var w = $(this).width();
            $(this).attr('style', 'position:relative; top:-1em; margin-right:-'+w+'px;'+'left:-'+(Math.ceil(w/2))+'px;');
        });
    }

    this.onChangeVisibleContent = function() {
        // this is called each time the portion of the text visible in this panel has changed.
        // load visible images
        this.getAllVisibleElements(this.textBox, "div.lazy-image", this.loadLazyImage);

        // update the location in the navigation boxes
        var element = this.getFirstVisibleElement('.anchor-c');
        this.navChapter.val(element ? get_location_shorthand_from_id(element.attr('id')) : '');
        this.locationId = element ? element.attr('id') : '';

        // TODO: move this into a function
        // TODO: the condition should be resolved by the viewer class depending on the
        // doc_info in both panels.
        var pageLocation = '';
        var witnessid = this._getWitnessid();
        if (this.doc_info.pagination && witnessid) {
            var element = this.getFirstVisibleElement('.anchor-p-'+witnessid);
            if (element && element.length) {
                pageLocation = element.attr('id').replace(/^.*_/, '');
                //this.dm(pageLocation);
            }
        }
        this.navPage.val(pageLocation);

        if (this.deepPermalink) this.viewer.updatePermalink();

        //this.dm('onChangeVisibleContent ' + this.locationId);

        // bubble up event to enable synchronisation of the text location
        if (!this.beingSynced) this.viewer.synchronisePanels(this);
        this.beingSynced = false;
    }

    this._getWitnessid = function() {
        return this.doc_info.witnessid || this.viewer.getWitnessid();
    }

    this.loadLazyImage = function(jq_element) {
        // TODO: optimisation: don't do all this work if there are no images in the text
        var img_src = jq_element.children("span").text();
        //jq_element.replaceWith('<img class="'+jq_element.attr("class")+'" src="'+img_src+'" width="'+jq_element.width()+'" height="'+jq_element.height()+'" />');
        //img_src = '';
        var jq_anchor = $('<a href="#"><img class="' + jq_element.attr("class") + '" src="' + img_src + '" height="' + jq_element.height() + '"/></a>');
        jq_element.replaceWith(jq_anchor);

        // on click event => load in zoomifying tool
        jq_anchor.click(function() {
            var img_src = $(this).children('img').attr('src');
            if (img_src) {
                // reload the zoomifier iframe
                // img_src = img_src.replace(/(.*)\brft_id=(.+?\.jp2\b)(.*)/, '$2');
                img_src = img_src.replace(/\.jp2.*/, '.jp2');
                $('#image-viewer-iframe').attr('src', '?zoom=1&src='+img_src);

                // pop it up in a fancy box
                $.fancybox({
                    'href': '#image-viewer',
                });
            }
            return false;
        });
    }

    this.getFirstVisibleElement = function(jq_selector, windowHeight) {
        // get_first_visible_element($('.viewer-text-box'), 'p')
        var ret = null;
        if (windowHeight == null) windowHeight = 40;
        var windowTop = this.textBox.offset().top;
        var windowBottom = windowTop + windowHeight;
        var elements = this.textBox.find(jq_selector).each(function() {
                                var top = $(this).offset().top;
                                if (top <= windowBottom) ret = $(this);
                                return (top < windowTop);
                            }
                        );
        return ret;
    }

    this.getAllVisibleElements = function(jq_viewer, jqs_elements, fct) {
        var ret = [];
        var viewer_top = jq_viewer.offset().top;
        var viewer_bottom = viewer_top + jq_viewer.height();
        // true iff all the element encountered so far are completely above the viewer
        var above = true;
        var elements = jq_viewer.find(jqs_elements).each(function() {
                                var jq_element = $(this);
                                above = above && ((jq_element.offset().top + jq_element.height()) <= viewer_top);
                                if (!above) {
                                    if (jq_element.offset().top >= viewer_bottom) return false;
                                    if (fct != null) fct(jq_element);
                                    ret.push(jq_element);
                                }
                                return true;
                            }
                        );
        return ret;
    }

    this.scrollToPage = function(pageNumber) {
        var ret = false;
        var jq_element = this.textBox.find('#a-'+this.panelIndex+'-p-'+this._getWitnessid()+'_'+pageNumber);
        if (jq_element.length) {
            //this.dm('found! '+ids[i]);
            ret = this.scrollTextBoxToElement(jq_element);
        }
        return ret;
    }

    this.scrollToShorthand = function(shorthand) {
        var ret = false;
        // get possible ids from shorthand
        //this.dm('shorthand = '+shorthand);
        var ids = get_location_id_variants(get_location_id_from_shorthand(shorthand, this.panelIndex), this.panelIndex);
        for (var i in ids) {
            //this.dm('try '+ids[i]);
            var jq_element = this.textBox.find('#'+ids[i]);
            if (jq_element.length) {
                //this.dm('found! '+ids[i]);
                this.scrollTextBoxToElement(jq_element);
                ret = true;
                break;
            }
        }
        return ret;
    }

    // returns true iff jq_element is not empty/null.
    this.scrollTextBoxToElement = function(jq_element) {
        var ret = false;
        if (jq_element.offset()) {
            var before = this.textBox.scrollTop();
            this.textBox.scrollTop(jq_element.offset().top - this.textBox.offset().top + this.textBox.scrollTop());
            if (this.textBox.scrollTop() == before)
                // Didn't move, so no JS event will be triggered.
                // So the next time an event is triggered it should not be ignored.
                this.beingSynced = false;
            ret = true;
        } else {
            //this.dm('not found');
        }
        return ret;
    }

    this.bindOnScroll = function(unbind) {
        var self = this;
        if (this.onScroll == null) {
            this.onScroll = function(event_info) {
                self.onChangeVisibleContent($(event_info.target));
            };
        }
        if (unbind) {
            this.textBox.unbind('scroll', this.onScroll);
        } else {
            this.textBox.bind('scroll', this.onScroll);
        }
    }

    this.ready = function() {
        // events binding
        var self = this;
        this.textType.change(function() { self.onChangeTextType(); });
        this.bindOnScroll();
        this.navChapter.keydown(function(event_info) {
                if (event_info.keyCode == "13") {
                    if (!self.scrollToShorthand(self.navChapter.val())) {
                    }
                }
            }
        );
        this.navPage.keydown(function(event_info) {
                if (event_info.keyCode == "13") {
                    if (!self.scrollToPage(self.navPage.val())) {
                    }
                }
            }
        );

        // initial resize
        this.onResize();
        // initial loading of the text
        this.onChangeTextType();
    }

    this.dm = function(message) {
        dm('' + this.panelIndex + ' - ' + message);
    }

}

/**
 * ----------------------------------
 *              Annotator
 * ----------------------------------
 */

function Annotator(jqs_container, anchorKey, textType) {
    this.jq_annotations = null;
    this.anchorKey = anchorKey;
    this.textType = textType;
    this.jq_container = $(jqs_container);

    this.setAnnotations = function(jqs_annotations) {
        this.jq_annotations = $(jqs_annotations);
    }

    this.loadAnnotations = function() {
        if (this.jq_annotations == null) {
            this.jq_annotations = call_django('load_doc', {'doc_key': this.textType, 'panel': 2});
            if (this.jq_annotations != null) {
                this.jq_annotations = $('<div>' + this.jq_annotations.doc + '</div>');
            }
        }
    }

    /**
     * Parse the annotated text and add a class to the anchors
     * which are found in the annotation text.
     */
    this._tagExistingAnchors = function(jq_text, panelIndex) {
    }

    this.annotateText = function(jq_text, clearAnnotation, panelIndex) {
        var jq_anchors = jq_text.find('.anchor-label-'+this.anchorKey);
        if (jq_anchors.length == 0) return;
        clearAnnotation = (clearAnnotation == true ? true : false);
        if (!clearAnnotation) {
            if (!jq_anchors[0].annotated) {
                var self = this;
                //dm('bind');
                jq_anchors.bind(this._getAnchorEvents(), function(event) {self._displayAnnotation(event, $(this))} );
            }
            jq_anchors[0].annotated = true;
        }
        jq_anchors.toggle(!clearAnnotation);
        this._tagExistingAnchors(jq_text, panelIndex);
    }

    this._getAnchorEvents = function() {
        return 'mouseenter mouseleave';
    }

    this._displayAnnotation = function(event, jq_anchor) {
        if (event.type == 'mouseenter' || event.type == 'click') {
            var jq_content = this._getAnnotation(jq_anchor.attr('id'));
            if (this._generateContent(jq_anchor, jq_content))
                this._showContainer(jq_anchor);
        } else {
            this.jq_container.hide();
        }
    }

    this._getAnnotation = function(annotationId) {
        var ret = null;
        this.loadAnnotations();
        if (this.jq_annotations != null) {
            ret = this.jq_annotations.find('#'+annotationId.replace(/^(a-)\d+(.*)$/, '$12$2'));
        }
        return ret;
    }

    this._generateContent = function(jq_anchor, jq_content) {
        if (jq_content.length != 1) return false;
        this.jq_container.html(jq_content.html());
        return true;
    }

    this._showContainer = function(jq_anchor) {
        //dm('show');
        this.jq_container.css({
            'top': (jq_anchor.offset().top + jq_anchor.height() + 2)+'px',
            'left': (jq_anchor.offset().left + jq_anchor.width() + 2)+'px',
           });
        this.jq_container.show();
    }

}

/**
 * ----------------------------------
 *          Annotator Comments
 * ----------------------------------
 */

function AnnotatorComments(jqs_container, anchorKey, textType, text_viewer) {
    this.jq_annotations = null;
    this.anchorKey = anchorKey;
    this.textType = textType;
    this.jq_container = $(jqs_container);
    this.expanded = false;
    this.space = null;
    this.text_viewer = text_viewer;
    this.nonpanel_height = 0;

    // prepare the the comment box and wire it up with JS events
    var self = this;
    this.jq_container.remove().appendTo('body');
    this.jq_container.find('.user-comments-box-close,.cb-close').click( function() {self.jq_container.hide(); } );
    this.jq_container.find('.user-comments-box-submit').click( function() {self.postComment();} );
    this.jq_container.find('.user-comments-box-tabs li').click( function() {self.onClickTab(this);} );
    this.jq_container.find('#user-comments-field-comment').keyup( function() { self.refreshPostButtonVisibility();} );
    this.jq_container.find('#user-comments-field-comment').change( function() { self.refreshPostButtonVisibility();} );
    this.jq_container.find('.cb-resize').click( function() { self.onClickExpand(this); } );

    this.onClickExpand = function(expand_icon) {
        this.expandBox(!this.expanded);
    }

    this.expandBox = function(expand) {
        if (expand == null) expand = true;
        if (this.nonpanel_height == 0) {
            this.nonpanel_height = this.jq_container.height() - this.jq_container.find('.panel').height();
        }
        if (this.expanded != expand) {
            this.expanded = expand;
            if (this.expanded) {
                // save dimensions and position
                this.space = getSpace(this.jq_container);
                // expand the box
                setSpace(this.jq_container, this.text_viewer.panels[1 - this.getPanelIndex()].getSpace());
            } else {
                // shrink the box
                setSpace(this.jq_container, this.space);
            }
            this.jq_container.find('.panel').height(this.jq_container.height() - this.nonpanel_height);
            this.jq_container.find('.cb-resize').toggleClass('maximized', this.expanded);
        }
    }

    this.getPanelIndex = function() {
        return parseInt(this.jq_anchor.attr('id').replace(/^a-(\d+)-.*/, '$1'))
    }

    this.onClickTab = function(tab) {
        var panels = this.jq_container.find('.panel > div');
        this.jq_container.find('.user-comments-box-tabs li').each( function(index) {
            $(this).toggleClass('tab-selected', tab == this);
            $(panels[index]).toggle(tab == this);
        });

        this.refreshPostButtonVisibility();
    }

    this.postComment = function() {
        $('#spinner-uc').show();
        $('#ajax-message-uc').hide();
        var doc_key = this.text_viewer.panels[this.getPanelIndex()].textType.val();
        var content = call_django(
                                    'post_comment',
                                    {
                                        'doc_key': doc_key,
                                        'panel': this.getPanelIndex(),
                                        'refid': this.jq_anchor.attr('id').replace(/.*uc-/i, ''),
                                        'comment': $('#user-comments-field-comment').val(),
                                        'private': $('#user-comments-field-private').attr('checked') ? 1 : 0
                                    },
                                    true,
                                    function(jqXHR, textStatus) {
                                        $('#spinner-uc').hide();
                                        if (textStatus == 'success') {
                                            $('#ajax-message-uc').hide();
                                            $('#ajax-message-uc').removeClass('error');
                                        } else {
                                            $('#ajax-message-uc').show();
                                            $('#ajax-message-uc').html('Connection failed. Please try again later.');
                                            $('#ajax-message-uc').addClass('error');
                                        }
                                    }
        );

        // copy the doc info
        if (content && !content.error) {
            // clear the comment box.
            this.jq_container.find('#user-comments-field-comment').val('');
            this.refreshPostButtonVisibility();
            this.setAnnotations('<div>' + content.doc + '</div>');
            this.onClickTab($('#user-comments-tab-all')[0]);
            this.jq_anchor.addClass('exists');
            this.jq_anchor.click();

            $('#ajax-message-uc').show();
            $('#ajax-message-uc').html('Your comment was submitted.');
            $('#user-comments-box .panel').scrollTop(100000);
        }
    }

    this.refreshPostButtonVisibility = function() {
        $('#ajax-message-uc').hide();
        $('#ajax-message-uc').removeClass('error');
        // only show the button if the 'Post a comment' tab is open AND the comment textarea is not empty
        this.jq_container.find('.user-comments-box-submit').toggle($('#user-comments-tab-post').hasClass('tab-selected') && ($('#user-comments-field-comment').val().search(/\S/) > -1 ) );
    }

    this.jq_container.find('.user-comments-box-tabs li:first').click();

}

AnnotatorComments.prototype = new Annotator();

AnnotatorComments.prototype._getAnchorEvents = function() {
    return 'click';
}

AnnotatorComments.prototype._generateContent = function(jq_anchor, jq_content) {
    // restore default space
    this.expandBox(false);

    $('#ajax-message-uc').hide();
    $('#ajax-message-uc').removeClass('error');
    this.jq_anchor = jq_anchor;
    $('#user-comments-box-all').html(jq_content.html() ? jq_content.html() : '<p>No comments yet.</p>');
    $('#user-comments-box-my').html(jq_content.html() ? jq_content.html() : '<p>No comments yet.</p>');

    if ((userid == null) || (userid == 0) || (userid == '0')) {
        $('#user-comments-box-my').html('<p>You need to <a class="int" href="/user/login?r=/laws/texts/ecf2/view/">log in</a> first before seeing your comments.</p>');
        $('#user-comments-box-form').html('<p>You need to <a class="int" href="/user/login?r=/laws/texts/ecf2/view/">log in</a> first before posting a comments.</p>');
    }

    this.jq_anchor = jq_anchor;

    return true;
}

/**
 * Parse the annotated text and add a class to the anchors
 * which are found in the annotation text.
 */
AnnotatorComments.prototype._tagExistingAnchors = function(jq_text, panelIndex) {
    this.loadAnnotations();
    var className = 'exists';
    this.jq_annotations.find('.anchor-'+this.anchorKey).each(
        function() {
            if (!this.id) return;
            var id = this.id.replace(/^(a-)\d+(.*)$/, '#$1'+panelIndex+'$2');
            jq_text.find(id).addClass(className);
        }
    );
}



/*
var annotator = new Annotator('#tooltip', 'co', 'commentary');
annotator.setAnnotations('<div><div  id="a-2-co-1">c I</div><div id="a-2-co-2">c  II</div></div>');
annotator.annotateText($('#demo1'), false);
*/

/**
 * ----------------------------------
 *              Utilities
 * ----------------------------------
 */
function getSpace(jq_element) {
    return {'width': jq_element.width(), 'height': jq_element.height(), 'offset': jq_element.offset()};
}

function setSpace(jq_element, space) {
    if (space && space.width) {
        jq_element.width(space.width);
        jq_element.height(space.height);
        jq_element.offset(space.offset);
    }
}

function call_django(action, adata, post, complete) {
    var ret = null;
    if (adata == null) adata = {};
    adata['action'] = action;
    $.ajax({
        async: false,
        type: post ? "POST" : "GET",
        data: adata,
        //url: ".",
        success: function(data) {
            if (data != null && typeof data == "string" && data.length > 2) {
                ret = $.parseJSON(data.substring(1, data.length - 1));
            }
        },
        complete: complete,
     });
     return ret;
}

var rarr = new Array("M",  "CM", "D", "CD", "CCC", "CC", "C", "XC", "L", "XL", "XXX", "XX", "X", "IX", "V", "IV", "III", "II", "I");
           var narr = new Array(1000,900,500,400,300,200,100,90,50,40,30,20,10,9,5,4,3,2,1);
           var warr = new Array("CMCM",  "CMD",  "CMCD", "CMC", "DD", "DCD", "CDCD", "CDC", "CCCC", "XCXC",  "XCL", "XCXL", "XCX", "LL", "LXL", "XLXL", "XLX", "XXXX", "IXIX",  "IXV", "IXIV", "IXI", "IVIV", "IVI", "IIII");
           var carr= new Array("MDCCC", "MCD",  "MIII", "M",   "M",  "CM",  "DCCC", "D",   "CD",   "CLXXX", "CXL", "CIII", "C",   "C",  "XC",  "LXXX", "L",   "XL",   "XVIII", "XIV", "XIII", "X",   "VIII", "V",   "IV");
function get_arabic_from_roman(rom)
{
    var ret = 0;
    var roman = rom.replace(/ /g, "");
    roman = roman.toUpperCase();
    var roman2 = roman;
    roman = roman.replace(/[^IVXLCDM]/g, "");
    if (roman != roman2) return 0;
    if (roman.length == 0) return 0;

    var position = 0;
    var pp = -1;
    while(position < roman.length)
    {
        var p = getnextletter(roman, position);
        if ((pp != 0) && ( narr[pp] < narr[p])) return 0;
        if (p < 0) return 0;
        position += rarr[p].length;
        ret += narr[p];
        pp = p;
    }

    return ret;
}
function getnextletter(roman, position)
{
   for (i=0; i<warr.length; i++)
   {
      if ( roman.indexOf(warr[i], position) == position ) return -1;
   }
   for (i=0; i<rarr.length; i++)
   {
      if ( roman.indexOf(rarr[i], position) == position) return i;
   }
   return -1;
}
function get_roman_from_arabic(arabic)
{
    var narr=new Array("1000","900","500","400","100","90","50","40","10","9","5","4","1");
    var rarr=new Array("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I");
    var num = parseInt(arabic);
    if(num > 3999999 || num < 1) return '';
    var ret = '';
    var chk = num;
    while (chk > 0 )
    {
        var i;
        for (i=0; i < narr.length; i++)
        {
            if(chk >= narr[i] )
            {
                ret += rarr[i];
                chk -= narr[i];
                break;
            }
        }
    }
    return ret;
}

function isinteger(s)
{
    var i;
    s = s.toString();
    for (i = 0; i < s.length; i++)
    {
        var c = s.charAt(i);
        if (isNaN(c)) return false;
    }
    return true;
}

function get_location_shorthand_from_id(id) {
    var ret = '';
    // a-0-c-2_3_c_4_5
    // "code 2, III.4.5"
    // a-0-c-2_3_p_4_5
    // "code 2, III.prol 4.5"

    // remove prefix
    id = id.replace(/^a-\d+-/, '');
    var parts = id.split('-');
    var isPrologue = false;
    var lastIsPrologue = false;
    if (parts[0] == 'c') {
        var divs = parts[1].split('_');
        var i = 0;
        for (i = 0; i < divs.length; i++) {
            var div = divs[i];
            if ((i == 0) && (div != '0') && (div != '1')) {
                ret = ret + 'code '+div;
            }
            if ((i == 1) && (div != '0') && (div != '1')) {
                if (ret) ret = ret + ', ';
                ret = ret + get_roman_from_arabic(div);
            }
            if (i == 2) {
                isPrologue = (div == 'p');
                if (isPrologue) {
                    if (ret) ret = ret + '.';
                    ret = ret + 'prol. '
                    lastIsPrologue = true;
                }
            }
            if (i > 2) {
                if (!(i == 3 && isPrologue) && (div != '0')) {
                    if (((i == 5) && isPrologue) || ((i == 5) && !isPrologue)) {
                        div = String.fromCharCode(96 + parseInt(div));
                    } else {
                        if (ret && !lastIsPrologue) ret = ret + '.';
                    }
                    ret = ret + div;
                }
            }
        }
    }

    return ret;
}

function get_location_id_from_shorthand(shorthand, panelIndex) {
    var ret = '';

    // Clean
    shorthand = shorthand.toLowerCase().replace(/^\s*(.*?)\s*$/,'$1');

    // extract the code
    var rest = '';
    var parts = [];
    parts = shorthand.split(',');
    if (parts.length < 3) {
        if (parts.length == 2) {
            // code label, the rest
            // todo, extract as label not as 'code [number]'
            //ret = ret + parts[0];
            rest = parts[1].replace(/^\s*(.*?)\s*$/,'$1');
            ret = parts[0].replace(/code (\d+)/, '$1');
            if (ret == parts[0]) ret = '0';
        } else {
            // just the code label on its own?
            // TODO: look up the string in the list of available labels
            ret = parts[0].replace(/code (\d+)/, '$1');
            if (ret == parts[0]) {
                ret = '0';
                rest = parts[0];
            }
        }
    }
    // extract the rest
    if (rest) {
        // prol 1 => prol.1
        rest = rest.replace(/\s+/g,'.');
        rest = rest.replace(/\.+/g,'.');
        // 10.1a => 10.1.a
        rest = rest.replace(/(\d)([a-z])$/, '$1.$2');
        parts = rest.split('.');
        // IV.prol 3a -> {iv, prol, 3a}
        // IV.1.3a -> {iv, 1, 3a}
        // extract the book
        var book = get_arabic_from_roman(parts[0]);
        if (book) parts = parts.slice(1);
        ret = ret + '_' + book;
        // extract the chapter/prologue
        if (parts.length) {
            // prologue?
            var isPrologue = (parts[0] == 'prol');
            ret = ret + (isPrologue ? '_p' : '_c');
            if (isPrologue) parts = parts.slice(1);
            // chapter/prologue number
            if (parts.length) {
                if (isPrologue) ret = ret + '_1';
                // relative depth of the level where a letter is expected
                var numbersCount = isPrologue ? 1 : 2;
                while (parts.length) {
                    if (parts[0].match(/[a-z]/)) {
                        // e.g. a or prol a
                        // if we find a letter here, it implies an intermediate division 0.
                        while (numbersCount-- > 0) ret = ret + '_0';
                        ret = ret + '_' + (parts[0].charCodeAt(0) - 96);
                        // nothing after a letter
                        break;
                    } else {
                        // e.g. 3 or prol 3
                        ret = ret + '_' + parts[0];
                        parts = parts.slice(1);
                    }
                    numbersCount--;
                }
            } else {
                ret = ret + '_1';
            }
        }
    }

    return 'a-'+panelIndex+'-c-'+ret;
}

function test_location_translation() {
    var testCases = [
                     'prol.1',
                     'prol. 1',
                     'prol 1',
                     'prol',
                     'prol 1a',
//                   '3',
//                   '3c',
//                   '3.2',
//                   '3.2d',
//                   'iv.3',
//                   'IV.3.2',
                     'IV.prol 3',
//                   'IV.prol 3a',
//                   'IV.prol a',
//                   'Code 4, IV.3.2',
//                   'code 4, IV.3',
//                   'code 4, IV',
//                   'Code 0, I.1',
//                   'Code 1, I.1',
//                   'Code 4',
//                   'IV',
                     // phase 2
                     /*
                     'Code name',
                     'Code name, IV',
                     'Code name',
                     'Code name, IV',
                     */
                     ];

    var i;
    for (i in testCases) {
        var shorthand = testCases[i];
        //dm(shorthand);
        var id = get_location_id_from_shorthand(shorthand);
        //dm('---> '+id);
        var shorthand2 = get_location_shorthand_from_id(id);
        //dm('---> '+shorthand2);
        var id2 = get_location_id_from_shorthand(shorthand2);
        //dm('---> '+id2);
        if (shorthand2.toLowerCase() != shorthand.toLowerCase()) {
            //dm('---> ERROR: shorthands are different.');
        }
        if (id2.toLowerCase() != id.toLowerCase()) {
            //dm('---> ERROR: ids are different.');
        }
    }
}

function dm(message) {
    if (window.console && window.console.log) console.log(message);
}

function get_location_id_variants(ids, panelIndex, position) {
    if (position == null) position = 6;
    // a-0-c-1_0_c_15_2
    if (ids == null) ids = '';
    if (typeof(ids) == typeof('a')) ids = [ids];
    if (ids.length == 0) ids = ['a-'+panelIndex+'-c-0_0'];
    var i = 0;
    var c = '';
    for (i = ids.length - 1; i >= 0; i--) {
        c = ids[i].substr(position, 1);
        c = (c == '1') ? '0' : (c == '0') ? '1' : '';
        if (c != '') ids.push(ids[i].substr(0, position) + c + ids[i].substr(position + 1));
    }
    if (position == 6) ids = get_location_id_variants(ids, panelIndex, 8);

    return ids;
}
