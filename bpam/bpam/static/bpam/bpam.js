"use strict";

var loadingText = 'Loading...';

var set_ckanapi_error = function() {
    console.log("error contacting the CKAN API.")
    $('#error-bar').removeClass('hide').html('<p>An error occurred while attempting to contact the metadata server. Please <a href="javascript:history.go(0);">reload the page.</a> If the error persists, please <a href="http://www.bioplatforms.com/contact/">contact us</a>.</p>');
};

var setup_table = function(configure) {
  var config = configure();

  var ft = $('.apitable').DataTable(config);
  ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
  $('.apitable').addClass('table-striped table-bordered table-condensed');
};

var sample_id_from_location = function() {
    // sample id should be the last part of the URL following '.../sample/'
    var match = window.location.pathname.match(/sample\/([^\/]+)\/?$/);
    if (match == null || match.length < 2) {
        return;
    }

    return match[1];
};

var set_sample = function(callback) {
    var sample_id = sample_id_from_location();
    if (!sample_id) {
        return;
    }
    CKAN.get_sample(sample_id, callback);
};

// Can be made more general later if needed
var createProjectOverviewTree = function(config) {
  var tree = $('#tree').jstree({
    'core' : {
      'data': function(obj, callback) {
        $.ajax({ 'url': config.url }).done(function(resp) {
            var data = resp.data;
            callback.call(this, config.nodeCreator(data));
        });
      }
    },
    'plugins' : [ 'state' ]
  });

  tree.on('select_node.jstree', function (e, data) {
    config.tableRecreator(data.node.original.url);

    if (data.instance.is_parent(data.node)) {
        if (!data.instance.is_open(data.node) ) {
            data.instance.toggle_node(data.node);
        }
    }
  });

  $('#tree-toggle-btn').on('click', function() {
    if ( $('#tree-col').is(':hidden') ) {
      $('#content-col').removeClass('col-md-12');
      $('#content-col').addClass('col-md-10');
      $('#tree-col').show('slow');
      $('#tree-toggle-btn').html('Hide tree');
    } else {
      $('#tree-col').hide('slow', function() {
          $('#content-col').removeClass('col-md-10');
          $('#content-col').addClass('col-md-12');
          $('#tree-toggle-btn').html('Show tree');
      });
    }
  });
};
