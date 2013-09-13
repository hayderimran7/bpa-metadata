jQuery(document).ready(function($) {
    var catalog_name = $("#bpa-metadata-catalog").val();
    // wire up search
    $('#submit-form').submit(function(ev) {
        ev.preventDefault();
        var url = '/' + encodeURIComponent(catalog_name) + '/search/' + encodeURIComponent($("#search-input").val());
        window.location.href = url;
    });
});
