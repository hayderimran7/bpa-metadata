jQuery(document).ready(function($) {
    // wire up search
    $('#submit-form').submit(function(ev) {
        ev.preventDefault();
        var url = '/search/' + encodeURIComponent($("#search-input").val());
        window.location.href = url;
    });
});
