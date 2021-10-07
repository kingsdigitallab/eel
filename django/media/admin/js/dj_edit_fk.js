/* Adds an edit icon next to each foreign key field */
$(function(){
    $("select ~ a.add-another").each(function(){
        $(this).after("&nbsp;\x3Ca class='changelink' href='#'\x3E\x3C/a\x3E");
        $(this).next().click(function(){
            var value = $(this).parent().children('select:first').attr('value');
            var link = ($(this).prev().attr('href')+'../'+value+'/');
            var win = window.open(link + '?_popup=1', link, 'height=600,width=1000,resizable=yes,scrollbars=yes');
            win.focus();
            return false;
        });
    });

    // this is for one to many inlines
    $("span.delete").each(function(){
        var inputFK = $(this).parent().nextAll('input').filter(function(index){return ($(this).attr("id").match(/-id$/) );}).eq(0);
        if (inputFK != null) {
            var recId = inputFK.val();
            var recTable = inputFK.attr('name').match(/^(.*)_set-/);
            if (recTable != null) {
            	recTable = recTable[1];
            	$(this).before("&nbsp;\x3Ca class='changelink' href='#'\x3E\x3C/a\x3E");
                var link = '../../'+recTable+'/'+recId+'/';
                $(this).prev().click(function(){
	                var win = window.open(link + '?_popup=1', link, 'height=600,width=1000,resizable=yes,scrollbars=yes');
    	            win.focus();
    	            return false;
                });
            }
        }
    });
});
/* -------------------------------------------- */
