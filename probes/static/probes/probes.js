var probes_tabs_expanded_cookie_name = 'probes_tabs_expanded';

function create_cookie(name, value, days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days * 24 * 60 * 60 * 1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name + "=" + value + expires + "; path=/";
}

function read_cookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1, c.length);
		if (c.indexOf(nameEQ) == 0) {
		    return c.substring(nameEQ.length, c.length);
		}
	}
	return null;
}

function erase_cookie(name) {
	create_cookie(name, "", -1);
}

function are_tabs_scrollable() {
    return $('.probe-tab-container').hasClass('scrollable-tabs');
}

function enable_disable_tab_scroll_buttons() {
    if(!are_tabs_scrollable()) return;

    var $leftButton = $('a.scroll-action.action-left');
    var $rightButton = $('a.scroll-action.action-right');
    var $probeTabs = $('.nav-tabs.probe-tabs');

    var scrollValue = $probeTabs.scrollLeft() / ($probeTabs[0].scrollWidth - $probeTabs.width());

    $leftButton.toggleClass('disabled', (isNaN(scrollValue) || scrollValue == 0));
    $rightButton.toggleClass('disabled', (isNaN(scrollValue) || scrollValue == 1));
}

function get_tab_scroll_amount() {
    return $('.probe-tab-container').width() / 3;
}

function scroll_tabs_left() {
    $('.probe-tabs').animate(
        { scrollLeft: '-=' + get_tab_scroll_amount() },
        { always: enable_disable_tab_scroll_buttons }
    );
    $('a.scroll-action').blur();
    return false;
}

function scroll_tabs_right() {
    $('.probe-tabs').animate(
        { scrollLeft: '+=' + get_tab_scroll_amount() },
        { always: enable_disable_tab_scroll_buttons }
    );
    $('a.scroll-action').blur();
    return false;
}

function toggle_scrollable_probe_tabs() {
    if(are_tabs_scrollable()) {
        $('.probe-tab-container').removeClass('scrollable-tabs');
        $('#probe-tab-style-toggle').html('&#8863; Collapse');
    } else {
        $('.probe-tab-container').addClass('scrollable-tabs');
        $('#probe-tab-style-toggle').html('&#8862; Expand');
        enable_disable_tab_scroll_buttons();
    }
    create_cookie(probes_tabs_expanded_cookie_name, are_tabs_scrollable() ? 0 : 1);
    return false;
}
