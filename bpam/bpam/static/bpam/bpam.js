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

var sample_data_from_location = function() {
    // sample id should be the last part of the URL following '.../sample/'
    var match = window.location.pathname.match(/sample\/([^\/]+\/)?([^\/]+\/)?([^\/]+)\/?$/);
    if (match == null || match.length < 2) {
        return;
    }
    var resource_type = _.chain(match[1]).defaultTo('').trimEnd('/').value();
    var status = _.chain(match[2]).defaultTo('').trimEnd('/').value();
    var id = match[3];
    return [id, resource_type, status];
}

var sample_id_from_location = function() {
  return sample_data_from_location()[0];
}

var resource_type_from_location = function() {
  return sample_data_from_location()[1];
}

var sample_status_from_location = function() {
  return sample_data_from_location()[2];
}

var set_sample = function(callback) {
    var sample_id = sample_id_from_location();
    var resource_type = resource_type_from_location();
    var status = sample_status_from_location();
    if (!sample_id) {
        return;
    }
    CKAN.get_sample_of_type(sample_id, resource_type, status, callback);
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
    'conditionalselect' : function (node) {
        var isTopLevel = function(node) { return node.parents.length == 1; }
        return !isTopLevel(node);
    },
    'plugins' : [ 'conditionalselect', 'state' ]
  });

  tree.on('select_node.jstree', function (e, data) {
    config.tableRecreator(data.node.original.url, data.node.original);

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
