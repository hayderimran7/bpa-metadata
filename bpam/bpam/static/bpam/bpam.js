"use strict";

var loadingText = 'Loading...';

$(document).ready(function () {
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
});

var set_ckanapi_error = function () {
    console.log("error contacting the CKAN API.")
    $('#error-bar').removeClass('hide').html('<p>An error occurred while attempting to contact the metadata server. Please <a href="javascript:history.go(0);">reload the page.</a> If the error persists, please <a href="http://www.bioplatforms.com/contact/">contact us</a>.</p>');
};

var get_sample = function (package_id, callback) {
    var api_base = bpam_config.ckan_base + 'proxy/';
    var uri = api_base + 'api/3/action/package_show?id=' + package_id;
    $.getJSON(uri).done(function (results) {
        callback(results.result);
    }).fail(function () {
        set_ckanapi_error();
    });
};

var get_project_data = function (data_type, callback) {
    // grab the packages and resources for the project - which should all
    // have CKAN type ``data_type``. calls ``callback`` with the result
    var api_base = bpam_config.ckan_base + 'proxy/';
    var package_search = api_base + 'api/3/action/package_search?q=type:' + data_type + "&rows=1000";
    var resource_search = api_base + 'api/3/action/resource_search?query=resource_type:' + data_type + "&rows=1000";
    $.getJSON(package_search).done(function (package_results) {
        $.getJSON(resource_search).done(function (resource_results) {
            var package_by_id = {};
            $.each(package_results.result.results, function (idx, package_obj) {
                package_by_id[package_obj.id] = package_obj;
            });
            var resources_by_id = {};
            $.each(resource_results.result.results, function (idx, resource_obj) {
                var package_id = resource_obj.package_id;
                if (!(package_id in resources_by_id)) {
                    resources_by_id[package_id] = [];
                }
                resources_by_id[package_id].push(resource_obj);
            });
            var package_info = [];
            $.each(package_by_id, function (id, package_obj) {
                var p = $.extend({}, package_obj);
                p.resources = resources_by_id[id];
                package_info.push(p);
            });
            var resource_info = [];
            $.each(resource_results.result.results, function (idx, resource) {
                var r = $.extend({}, resource);
                r.package = package_by_id[resource.package_id];
                resource_info.push(r);
            });
            callback(package_info, resource_info);
        }).fail(function () {
            set_ckanapi_error();
        });
    }).fail(function () {
        set_ckanapi_error();
    });
};

// TODO remove this function if not needed - started using Ajax from DataTable
var get_resources_data = function (org_name, package_type, callback) {
    var resource_search = bpam_config.ckan_base + 'resources/' + org_name + '/' + package_type;
    $.getJSON(resource_search).done(function (resource_results) {
        callback(resource_results.data);
    }).fail(function () {
        set_ckanapi_error();
    });
};

var get_packages_count = function (org_name, callback) {
    var packages_count = bpam_config.ckan_base + 'packages_count/' + org_name;
    $.getJSON(packages_count).done(function (result) {
        callback(result.data);
    }).fail(function () {
        set_ckanapi_error();
    });
};

var get_resources_count = function (org_name, callback) {
    var resource_count = bpam_config.ckan_base + 'resources_count/' + org_name;
    $.getJSON(resource_count).done(function (resource_results) {
        callback(resource_results.data);
    }).fail(function () {
        set_ckanapi_error();
    });
};

var get_resources_count_by_amplicon = function (callback) {
    var resource_count = bpam_config.ckan_base + 'resources_count_by_amplicon';
    $.getJSON(resource_count).done(function (resource_results) {
        callback(resource_results.data);
    }).fail(function () {
        set_ckanapi_error();
    });
};

var wheat_pathogen_samples_setup = function () {
    var setup_table = function (package_info, resource_info) {
        var config = {
            colReorder: true,
            stateSave: true,
            data: package_info,
            processing: true,
            pageLength: 100,
            buttons: [
                'colvis', 'copy', 'csv', 'excel', 'print'
            ],
            columns: [
                {
                    'data': 'bpa_id',
                    'render': function (data, type, row) {
                        var url = bpam_config.bpam_base + 'wheat_pathogens/sample/' + data + '/';
                        return '<a href="' + url + '">' + data + '</a>';
                    }
                },
                { 'data': 'sample_id' },
                { 'data': 'official_variety_name' },
                { 'data': 'kingdom' },
                { 'data': 'phylum' },
                { 'data': 'species' },
                { 'data': 'original_source_host_species' },
                { 'data': 'collection_location' },
                { 'data': 'wheat_pathogenicity' },
                { 'data': 'contact_scientist' },
                { 'data': 'dna_source' },
                { 'data': 'dna_extraction_protocol' }
            ],
            fixedHeader: true
        };
        var ft = $('.apitable').DataTable(config);
        ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
        $('.apitable').addClass('table-striped table-bordered table-condensed');
    };
    $(document).ready(function () {
        get_project_data('wheat-pathogens', setup_table);
    });
};

var marine_microbes_samples_setup = function () {
    var setup_table = function (resources) {
        var resource_search = bpam_config.ckan_base + 'packages/bpa-marine-microbes';
        var config = {
            colReorder: true,
            stateSave: true,
            // data: resources,
            ajax: {
                url: resource_search,
                cache: true,
                dataSrc: 'data'
            },
            processing: true,
            pageLength: 100,
            buttons: [
                'colvis', 'copy', 'csv', 'excel', 'print'
            ], columns: [
                {
                    'data': 'id',
                    'defaultContent': '',
                    'render': function (data, type, row) {
                        var url = bpam_config.bpam_base + 'marine_microbes/sample/' + data + '/';
                        return '<a href="' + url + '">' + data + '</a>';
                    }
                },
                { 'data': 'bpa_id' , 'defaultContent': ''},
                { 'data': 'sample_type' , 'defaultContent': ''},
                { 'data': 'sample_site', 'defaultContent': '' },
                { 'data': 'date_sampled', 'defaultContent': '' },
                { 'data': 'depth', 'defaultContent': '' }
            ],
            fixedHeader: true
        };
        var ft = $('.apitable').DataTable(config);
        ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
        $('.apitable').addClass('table-striped table-bordered table-condensed');
    };
    $(document).ready(function () {
        setup_table();
    });
};

var marine_microbes_metagenomics_setup = function () {
    var setup_table = function (resources) {
        var resource_search = bpam_config.ckan_base + 'resources/bpa-marine-microbes/mm-metagenomics';
        var config = {
            colReorder: true,
            stateSave: true,
            // data: resources,
            ajax: {
                url: resource_search,
                cache: true,
                dataSrc: 'data'
            },
            processing: true,
            pageLength: 100,
            buttons: [
                'colvis', 'copy', 'csv', 'excel', 'print'
            ], columns: [
                {
                    'data': 'package.id',
                    'defaultContent': '',
                    'render': function (data, type, row) {
                        var url = bpam_config.bpam_base + 'marine_microbes/sample/' + data + '/';
                        return '<a href="' + url + '">' + data + '</a>';
                    }
                },
                { 'data': 'package.bpa_id' , 'defaultContent': ''},
                { 'data': 'package.sample_type' , 'defaultContent': ''},
                { 'data': 'vendor', 'defaultContent': '' },
                { 'data': 'index', 'defaultContent': '' },
                {
                    'data': 'url',
                    'defaultContent': '',
                    'render': function (data, type, row) {
                        return '<a href="' + row.url + '"><span class="glyphicon glyphicon-download"></span> Download</a>';
                    }
                },
                {
                    'data': 'md5',
                    'defaultContent': '',
                    'render': function (data, type, row) {
                        return '<pre>' + data + '</pre>';
                    }
                }
            ],
            fixedHeader: true
        };
        var ft = $('.apitable').DataTable(config);
        ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
        $('.apitable').addClass('table-striped table-bordered table-condensed');
    };
    $(document).ready(function () {
        setup_table();
    });
};

var marine_microbes_amplicon_setup = function (amplicon) {
    var setup_table = function (resources) {
        var resource_search = bpam_config.ckan_base + 'resources/bpa-marine-microbes/mm-genomics-amplicon';
        if (amplicon !== 'all') {
            resource_search += '?amplicon=' + amplicon;
        }
        var config = {
            colReorder: true,
            stateSave: true,
            // data: resources,
            ajax: {
                url: resource_search,
                cache: true,
                dataSrc: 'data'
            },
            processing: true,
            pageLength: 100,
            buttons: [
                'colvis', 'copy', 'csv', 'excel', 'print'
            ], columns: [
                {
                    'data': 'package.id',
                    'defaultContent': '',
                    'render': function (data, type, row) {
                        var url = bpam_config.bpam_base + 'marine_microbes/sample/' + data + '/';
                        return '<a href="' + url + '">' + data + '</a>';
                    }
                },
                { 'data': 'package.bpa_id' , 'defaultContent': ''},
                { 'data': 'package.sra', 'defaultContent': ''},
                { 'data': 'facility', 'defaultContent': ''},
                { 'data': 'amplicon', 'defaultContent': ''},
                { 'data': 'index', 'defaultContent': ''},
                { 'data': 'pcr1_10' , 'defaultContent': ''},
                { 'data': 'pcr1_100' , 'defaultContent': ''},
                { 'data': 'neat_pcr' , 'defaultContent': ''},
                { 'data': 'package.dilution_used' , 'defaultContent': ''},
                { 'data': 'package.analysis_software_version' , 'defaultContent': ''},
                { 'data': 'read' , 'defaultContent': ''}
            ],
            fixedHeader: true
        };
        var ft = $('.apitable').DataTable(config);
        ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
        $('.apitable').addClass('table-striped table-bordered table-condensed');
    };
    $(document).ready(function () {
        setup_table();
    });
};


var wheat_pathogen_sequencefiles_setup = function () {
    var setup_table = function (package_info, resource_info) {
        var config = {
            colReorder: true,
            stateSave: true,
            data: resource_info,
            processing: true,
            pageLength: 100,
            buttons: [
                'colvis', 'copy', 'csv', 'excel', 'print'
            ], columns: [
                {
                    'data': 'package.bpa_id',
                    'render': function (data, type, row) {
                        var url = bpam_config.bpam_base + 'wheat_pathogens/sample/' + data + '/';
                        return '<a href="' + url + '">' + data + '</a>';
                    }
                },
                { 'data': 'package.official_variety_name' },
                { 'data': 'package.sample_id' },
                { 'data': 'package.species' },
                { 'data': 'run_protocol_library_type' },
                { 'data': 'run_protocol_base_pairs' },
                { 'data': 'run_protocol' },
                { 'data': 'sequencer' },
                { 'data': 'package.library_id' },
                { 'data': 'package.index' },
                { 'data': 'run_number' },
                { 'data': 'flowcell' },
                { 'data': 'run_lane_number' },
                {
                    'data': 'filename',
                    'render': function (data, type, row) {
                        return '<a href="' + row.url + '"><span class="glyphicon glyphicon-download"></span>' + data + '</a>';
                    }
                },
                {
                    'data': 'md5',
                    'render': function (data, type, row) {
                        return '<pre>' + data + '</pre>';
                    }
                },
                { 'data': 'file_size' }
            ],
            fixedHeader: true
        };
        var ft = $('.apitable').DataTable(config);
        ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
        $('.apitable').addClass('table-striped table-bordered table-condensed');
    };
    $(document).ready(function () {
        get_project_data('wheat-pathogens', setup_table);
    });
};

var set_counts = function (data_type) {
    get_project_data(data_type, function (package_info, resource_info) {
        $('#package_count').text(package_info.length);
        $('#resource_count').text(resource_info.length);
    });
};

var sample_id_from_location = function () {
    var sample_id = window.location.pathname.replace(/\/$/, '').split('/')[3];
    /*
    if (!sample_id.match(/^[\d\.]+$/)) {
        return;
    }
    */
    return sample_id;
};

var set_sample = function () {
    var sample_id = sample_id_from_location();
    if (!sample_id) {
        return;
    }
    get_sample(sample_id, function (sample_obj) {
        $(".sample_id").text(sample_obj.sample_id);
        $(".sample_organism").text(sample_obj.species);
        $(".sample_label").text(sample_obj.label);
        $(".sample_dna_source").text(sample_obj.dna_source);
        $(".sample_official_variety_name").text(sample_obj.official_variety_name);
        $(".sample_wheat_pathogenicity").text(sample_obj.wheat_pathogenicity);
        $(".sample_original_source_host_species").text(sample_obj.original_source_host_species);
        $(".sample_requested_sequence_coverage").text(sample_obj.requested_sequence_coverage);
        $(".sample_collection_location").text(sample_obj.collection_location);
        $(".sample_protocol_reference").text(sample_obj.protocol_reference);
        $(".sample_date_sequenced").text(sample_obj.date_sequenced);
        $(".sample_comments_by_facility").text(sample_obj.comments_by_facility);
    });
};

var set_mm_sample = function () {
    var sample_id = sample_id_from_location();
    if (!sample_id) {
        return;
    }
    get_sample(sample_id, function (sample_obj) {
        $(".bpa_id").text(sample_obj.bpa_id);
        $(".sample_id").text(sample_obj.id);
        $(".sample_type").text(sample_obj.type);
        $(".site").text(sample_obj.sample_site);
        $(".sample_depth").text(sample_obj.depth);
        $(".collection_date").text(sample_obj.date_sampled);
    });
};

var set_sample_resources = function () {
    var sample_id = sample_id_from_location();
    if (!sample_id) {
        return;
    }
    var setup_table = function (sample_obj) {
        var config = {
            colReorder: true,
            stateSave: true,
            data: sample_obj.resources,
            processing: true,
            pageLength: 100,
            buttons: [
                'colvis', 'copy', 'csv', 'excel', 'print'
            ],
            columns: [
                {
                    'data': 'name',
                    'render': function (data, type, row) {
                        return '<a href="' + row.url + '">' + data + '</a>';
                    }
                },
                { 'data': 'md5' }
            ],
            fixedHeader: true
        };
        var ft = $('#api-sequence-list').DataTable(config);
        ft.buttons().container().appendTo($('.bootstrap_buttons'), ft.table().container());
        $('#api-sequence-list').addClass('table-striped table-bordered table-condensed');
    };
    get_sample(sample_id, function (sample_obj) {
        $(".resource_count").text(sample_obj.resources.length);
        var urls = _.map(sample_obj.resources, function (resource_obj) {
            return resource_obj.url;
        });
        setup_table(sample_obj);
        $(".download_links").text(urls.join("\n"));
    });
};

var landing_setup = function () {
    $('#marine_microbes_sample_count').text(loadingText);
    $('#wheat_pathogens_genome_sample_count').text(loadingText);

    var set_count = function (sel) {
        return function (package_info, resource_info) {
            $(sel).text(package_info.length);
        };
    };
    $(document).ready(function () {
        get_project_data('wheat-pathogens', set_count('#wheat_pathogens_genome_sample_count'));
        get_packages_count('bpa-marine-microbes', function(count) {
            $('#marine_microbes_sample_count').text(count);
        });
    });
};
