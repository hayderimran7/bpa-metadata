var BPAM = (function() {
    'use strict';

    return {
        map_init_list: function(map, options) {
            $("#sitelist tbody tr").each(function(index, el) {
                var get = function(cls) { return $(el).find("td." + cls).text(); };
                var marker = L.marker([get("lat"), get("lng")], {
                    title: get("name")
                });
                var href = $(el).find("td.name a").attr("href");
                var content = $("<div class='site-popup-table'>Loading...</div>");
                marker.addTo(map);
                marker.bindPopup(content.wrap("<div/>").parent()
                                 .prepend("<h3>" + get("name") + "</h3>")[0]);
                marker.on("popupopen", function(ev) {
                    content.load(href + " table#collectionsite", function() {
                        // after loading content, update popup so it gets the
                        // right size and so map pans to make entire popup visible
                        ev.popup.update();
                    });
                });
            });

            $(window).resize(function() {
                var targets = $("#site_map, #sitelist-container");
                var footer = $(".version");
                var unknown_pad = 12;

                // bootstrap limit for .col-md
                var stacked = $(window).width() < 980;

                targets.each(function(index, el) {
                    var height = stacked ? "" : $(window).height() - $(el).offset().top - footer.outerHeight() - unknown_pad;
                    $(el).height(height);
                });

                map.invalidateSize();
            }).resize();
        },
        map_init_detail: function(map, options) {
            var latlng = L.latLng(window.collectionsite.lat, window.collectionsite.lon);
            L.marker(latlng).addTo(map);
            map.panTo(latlng);
        }
    };
})();
