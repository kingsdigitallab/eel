/*
 * From:
 * http://lucassmith.name/2009/05/test-if-a-font-is-installed-via-javascript.html
 */
function testFont(name) {
    name = name.replace(/['"<>]/g,'');

    var body  = document.body;
    test  = document.createElement('div');
    installed = false;
    template =
        '<b style="display:inline !important; width:auto !important; font:normal 10px/1 \'X\',sans-serif !important">ii</b>'+
        '<b style="display:inline !important; width:auto !important; font:normal 10px/1 \'X\',monospace !important">ii</b>';
    
    if (name) {
        test.innerHTML = template.replace(/X/g, name);
        test.style.cssText = 'position: absolute; visibility: hidden; display: block !important';
        body.insertBefore(test, body.firstChild);
        ab = test.getElementsByTagName('b');
        installed = ab[0].offsetWidth === ab[1].offsetWidth;
        body.removeChild(test);
    }

    return installed;
}
