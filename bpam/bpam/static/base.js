jQuery(document).ready(function($) {
    var catalog_path = $("#bpa-catalog-base").val();
    // wire up search
    $('#submit-form').submit(function(ev) {
        ev.preventDefault();
        var url = catalog_path + '/search/' + encodeURIComponent($("#search-input").val());
        window.location.href = url;
    });
});
