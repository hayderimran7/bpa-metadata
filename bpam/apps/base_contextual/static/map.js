var BPAM = (function() {
  'use strict';

  return {
    map_init_list: function(map, options) {
      var positions = window.positions;
      for (var i = 0; i < positions.length; i++) {
        var latlng = L.latLng(positions[i]);
        L.marker(latlng).addTo(map);
      }
    },
    map_init_detail: function(map, options) {
      var latlng = L.latLng(window.collectionsite.lat, window.collectionsite.lon);
      L.marker(latlng).addTo(map);
      map.panTo(latlng);
    }
  };
})();
