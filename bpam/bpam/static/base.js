jQuery(document).ready(function($) {
    var catalog_path = $("#bpa-catalog-base").val();
    // wire up search
    $('#submit-form').submit(function(ev) {
        ev.preventDefault();
        var url = catalog_path + '/search/' + encodeURIComponent($("#search-input").val());
        window.location.href = url;
    });
});


jQuery(document).ready(function($) {
    'use strict';

    var form = $("#sample-search");

    var query_fields = [{
        name: "Sample ID",
        field: "sample_id",
        type: "text",
        regexp: "([0-9]+.?)*"
    }, {
        name: "Date sampled",
        field: "date",
        type: "date"
    }, {
        name: "Depth",
        field: "depth",
        type: "number",
        units: "m"
    }, {
        name: "Horizon",
        field: "horizon",
        type: "text"
    }, {
        name: "Description",
        field: "desc",
        type: "text"
    }, {
        name: "Current land use",
        field: "land_use",
        type: "text"
    }, {
        // 7 taxonomic ranks
        name: "Kingdom",
        field: "kingdom",
        type: "select",
        options: ["Bacteria", "Protozoa", "Chromista", "Plantae", "Fungi", "Animalia"]
    }, {
        name: "Phylum",
        field: "phylum",
        type: "combo"
    }, {
        name: "Class",
        field: "class",
        type: "combo"
    }, {
        name: "Order",
        field: "order",
        type: "combo"
    }, {
        name: "Family",
        field: "family",
        type: "combo"
    }, {
        name: "Genus",
        field: "genus",
        type: "combo"
    }, {
        name: "Species",
        field: "species",
        type: "combo"
    }];
    var field_map = _.indexBy(query_fields, "field");

    var values = {};

    var make_row = function() {
        var row = $("<div class='row' />");
        var select = $("<select class='form-control' class='query-field'><option /></select>");
        _.each(query_fields, function(field) {
            select.append($("<option/>").attr("value", field.field).text(field.name));
        });
        row.append(select.wrap("<div class='col-xs-2'/>").parent());
        var value_col = $("<div class='col-xs-6'/>");
        row.append(value_col);
        var close = $('<button type="button" class="close" aria-hidden="true">&times;</button>');
        row.append(close.wrap('<div class="col-xs-1" />').parent());

        close.on("click", function(ev) {
            ev.preventDefault();
            row.remove();
        });

        var make_value_field = function(field) {
            var div = $('<div/>');

            var rangediv = function(min, max) {
                var col = '<div class="col-xs-5"/>';
                var dash = $('<div class="col-xs-2 text-center">—</div>');
                return $("<div class='row' />")
                    .append(min.wrap(col).parent())
                    .append(dash)
                    .append(max.wrap(col).parent());
            }

            if (field.type === "text" || !field.type) {
                var input = $('<input type="text" class="form-control" class="query-value">')
                    .attr("placeholder", field.name || null)
                    .on("change", function(ev) {
                        values[field.field] = $(this).val();
                    });
                div.append(input);
            } else if (field.type === "number") {
                var min = $('<input type="number" class="form-control" placeholder="min">');
                var max = $('<input type="number" class="form-control" placeholder="max">');
                div.append(rangediv(min, max).on("change", "input", function() {
                    values[field.field] = { min: min.val(), max: max.val() };
                }));
            } else if (field.type === "date") {
                var min = $('<input type="date" class="form-control" placeholder="min">');
                var max = $('<input type="date" class="form-control" placeholder="max">');
                div.append(rangediv(min, max).on("change", "input", function() {
                    values[field.field] = { min: min.val(), max: max.val() };
                }));
            } else if (field.type === "select") {
                var input = $('<select class="form-control">').on("change", function(ev) {
                    values[field.field] = $(this).val();
                });
                _.forEach(field.options, function(opt) {
                    input.append($("<option/>").val(opt).text(opt));
                });
                div.append(input);
            } else if (field.type === "combo") {
                var input = $('<input type="text" class="form-control query-value">')
                    .attr("placeholder", field.name || null);
                div.append(input);

                var opts = new Bloodhound({
                    name: field.field,
                    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
                    queryTokenizer: Bloodhound.tokenizers.whitespace,
                    remote: window.auto_complete_url + field.field + "?q=%QUERY"
                });

                opts.initialize();

                window.setTimeout(function() {
                    input.typeahead({
                        hint: true,
                        highlight: true,
                        minLength: 1
                    }, {
                        name: field.field,
                        displayKey: "name",
                        source: opts.ttAdapter()
                    }).focus().on("change", function(ev) {
                        values[field.field] = $(this).val();
                    });
                }, 1);

            }

            return div;
        };

        select.on("change", function(ev) {
            var field = field_map[$(this).val()];
            var newstuff = make_value_field(field);
            var oldstuff = value_col.empty();
            value_col.append(newstuff.children());
            value_col.find("input, select").filter(":visible").first().focus();
        });

        return row;
    };

    var insert_row = function(fixed) {
        var row = make_row();
        form.children().last().before(row);

        if (fixed) {
            row.find("option:first, button.close").remove();
            row.find("select").triggerHandler("change");
        }

        return row;
    };

    form.children("div").not(":last").remove();
    insert_row(true);

    form.on("change", "select.field", function(ev) {
        update_sensitive();

        var placeholders = form.find(".query-value").filter(function() {
            return $(this).val() === "";
        });

        if (placeholders.length === 0) {
            form.append(make_row());
        }
    });

    form.on("click", ".add-row", function(ev) {
        insert_row();
    });

    var update_sensitive = function() {
        var active = true;
        form.find("button[type='submit']")
            .toggleClass("disabled", !active)
            .attr("disabled", active ? null : "disabled");
    };
});
