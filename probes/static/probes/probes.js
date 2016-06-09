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
    return false;
}
