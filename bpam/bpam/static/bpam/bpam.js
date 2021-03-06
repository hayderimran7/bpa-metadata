"use strict";

var loadingText = 'Loading...';

var set_ckanapi_error = function() {
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
    var match = window.location.pathname.match(/([^\/]+)\/sample\/([^\/]+\/)?([^\/]+\/)?([^\/]+)\/?$/);
    if (match == null || match.length < 2) {
        return;
    }
    var project = _.defaultTo(match[1], '');
    var resource_type = _.chain(match[2]).defaultTo('').trimEnd('/').value();
    var status = _.chain(match[3]).defaultTo('').trimEnd('/').value();
    var id = match[4];
    return [id, project, resource_type, status];
}

// TODO clean this up!
// get the samples from the sample_detail page!

var project_from_location = function() {
  return sample_data_from_location()[1];
}

var sample_id_from_location = function() {
  return sample_data_from_location()[0];
}

var resource_type_from_location = function() {
  return sample_data_from_location()[2];
}

var sample_status_from_location = function() {
  return sample_data_from_location()[3];
}

var set_sample = function(callback) {
    var sample_id = sample_id_from_location();
    var project = project_from_location();
    var resource_type = resource_type_from_location();
    var status = sample_status_from_location();
    if (!sample_id) {
        return;
    }
    CKAN.get_sample_of_type(sample_id, project, resource_type, status, callback);
};

// Can be made more general later if needed
var createProjectOverviewTree = function(config) {
  var alwaysSelectable = function(node) {
    return true;
  };
  var parentNonSelectable = function (node) {
        var isTopLevel = function(node) { return node.parents && node.parents.length == 1; }
        return !isTopLevel(node);
  };

  var tree = $('#tree').jstree({
    'core' : {
      'data': function(obj, callback) {
        $.ajax({ 'url': config.url }).done(function(resp) {
            var data = resp.data;
            callback.call(this, config.nodeCreator(data));
        });
      }
    },
    'conditionalselect' : config.parentNonSelectable ? parentNonSelectable : alwaysSelectable,
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

  // open all on load
  tree.on('loaded.jstree', function() {
    tree.jstree('open_all');
  });
};

/*
Sets up all the ccgtables to use datatables.net.
This is used in legacy apps that haven't been moved to CKAN yet, should be removed when we port
all the apps to CKAN.
*/
var setup_all_ccg_tables = function() {
    var ccg_full_setup = {
        colReorder: true,
        stateSave: true,
        processing: true,
        pageLength: 100,
        buttons: [
            'colvis', 'copy', 'csv', 'excel', 'print'
        ],
        fixedHeader: true
    };
    var ft = $('.ccgtable').DataTable(ccg_full_setup);
    ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
    $('.ccgtable').addClass('table-striped table-bordered table-condensed');

    var ccg_slim_setup = {
        colReorder: true,
        stateSave: true,
        paging: false,
        pageLength: 100
    };
    var slimtable = $('.ccgslimtable').DataTable(ccg_slim_setup);
    $('.ccgslimtable').addClass('table-striped table-bordered table-condensed');
}

$(document).ready(function () {
		setup_all_ccg_tables();
});
