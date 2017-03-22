"use strict";

var CKAN = (function() {
    var exported = {};

    exported.get_packages_count = function(org_name, callback) {
        var packages_count = bpam_config.ckan_base + 'packages_count/' + org_name;
        $.getJSON(packages_count).done(function(result) {
            callback(result.data);
        }).fail(function() {
            set_ckanapi_error();
        })
    };

    exported.get_all_packages_count = _.partial(exported.get_packages_count, '');

    exported.get_sample = function(package_id, callback) {
        var uri = bpam_config.ckan_base + 'package_show/' + package_id;
        $.getJSON(uri).done(function(results) {
            callback(results.data);
        }).fail(function() {
            set_ckanapi_error();
        });
    };

    exported.get_resources_count = function(org_name, callback) {
        var resource_count = bpam_config.ckan_base + 'resources_count/' + org_name;
        $.getJSON(resource_count).done(function(resource_results) {
            callback(resource_results.data);
        }).fail(function() {
            set_ckanapi_error();
        });
    };

    exported.get_resources_count_by_amplicon = function(callback) {
        var resource_count = bpam_config.ckan_base + 'resources_count_by_amplicon';
        $.getJSON(resource_count).done(function(resource_results) {
            callback(resource_results.data);
        }).fail(function() {
            set_ckanapi_error();
        });
    };

    return exported;
})();