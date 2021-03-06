$(document).ready(function () {
    var theSpinner = null;

    function stopSpinner() {
        if (theSpinner) {
            theSpinner.stop();
            theSpinner = null;
        }
    }

    function doSpin() {
        var opts = {
            lines: 15, // The number of lines to draw
            length: 14, // The length of each line
            width: 10, // The line thickness
            radius: 20, // The radius of the inner circle
            corners: 1, // Corner roundness (0..1)
            rotate: 60, // The rotation offset
            direction: 1, // 1: clockwise, -1: counterclockwise
            color: '#000', // #rgb or #rrggbb or array of colors
            speed: 2.2, // Rounds per second
            trail: 95, // Afterglow percentage
            shadow: true, // Whether to render a shadow
            hwaccel: false, // Whether to use hardware acceleration
            className: 'spinner', // The CSS class to assign to the spinner
            zIndex: 2e9, // The z-index (defaults to 2000000000)
            top: '50%', // Top position relative to parent
            left: '50%' // Left position relative to parent
        };
        var target = document.getElementById('spinner');

        if (!theSpinner) {
            theSpinner = new Spinner(opts).spin(target);
        }

    }

    // var standardisedVocabularyEndPointURL = "{% url 'base:lookup' None %}".replace("None", "");
    // var TAXONOMY_URL = "{% url 'base:taxonomy' None None %}".replace("/None/None", "");
    // var SEARCH_FORM_URL = "{% url 'base:search' %}";
    // var EXPORT_RESULTS_URL = "{% url 'base:searchexport' %}";
    var STATUS_OK = "success";
    var rangeFieldOptions = [
        {value: "lat", text: "Latitude"},
        {value: "lon", text: "Longitude"},
        {value: "depth", text: "Soil Depth"},
        {value: "elevation", text: "Elevation (m)"},
        {value: "texture", text: "Texture"},
        {value: "gravel", text: "Gravel (%) - ( >2.0 mm)"},
        {value: "course_sand", text: "Course Sand (%) (200-2000 µm)"},
        {value: "fine_sand", text: "Fine Sand (%) - (20-200 µm)"},
        {value: "sand", text: "Sand (%)"},
        {value: "silt", text: "Silt (%) (2-20 µm)"},
        {value: "clay", text: "Clay (%) (<2 µm)"},
        {value: "ammonium_nitrogen", text: "Ammonium Nitrogen (mg/Kg)"},
        {value: "nitrate_nitrogen", text: "Nitrate Nitrogen (mg/Kg)"},
        {value: "phosphorus_colwell", text: "Phosphorus Colwell (mg/Kg)"},
        {value: "potassium_colwell", text: "Potassium Colwell (mg/Kg)"},
        {value: "sulphur", text: "Sulphur (mg/Kg)"},
        {value: "organic_carbon", text: "Organic Carbon (%)"},
        {value: "conductivity", text: "Conductivity (dS/m)"},
        {value: "cacl2_ph", text: "pH Level (CaCl2) (pH)"},
        {value: "h20_ph", text: "pH Level (H2O) (pH)"},
        {value: "dtpa_copper", text: "DTPA Copper (mg/Kg)"},
        {value: "dtpa_iron", text: "DTPA Iron (mg/Kg)"},
        {value: "dtpa_manganese", text: "DTPA Manganese (mg/Kg)"},
        {value: "dtpa_zinc", text: "DTPA Zinc (mg/Kg)"},
        {value: "exc_aluminium", text: "Exc. Aluminium (meq/100g)"},
        {value: "exc_calcium", text: "Exc. Calcium (meq/100g)"},
        {value: "exc_magnesium", text: "Exc. Magnesium (meq/100g)"},
        {value: "exc_potassium", text: "Exc. Potassium (meq/100g)"},
        {value: "exc_sodium", text: "Exc. Sodium (meq/100g)"},
        {value: "boron_hot_cacl2", text: "Boron Hot CaCl2 (mg/Kg)"},
        {value: "total_nitrogen", text: "Total Nitrogen"},
        {value: "total_carbon", text: "Total Carbon"}
    ];

    var fieldFieldOptions = [
        {value: "sample_id", text: "Sample Id"},
        {value: "date_sampled", text: "Date sampled"},
        {value: "lat", text: "Latitude"},
        {value: "lon", text: "Longitude"},
        {value: "depth", text: "Soil Depth"},
        {value: "description", text: "Description"},
        {value: "current_land_use", text: "Current land-use"},
        {value: "general_ecological_zone", text: "General Ecological Zone"},
        {value: "vegetation_type", text: "Vegetation Type"},
        {value: "vegetation_total_cover", text: "Vegetation Total cover (%)"},
        {value: "vegetation_dominant_trees", text: "Vegetation Dom. Trees"},
        {value: "elevation", text: "Elevation (m)"},
        {value: "australian_soil_classification", text: "Australian Soil Classification"},
        {value: "fao_soil_type", text: "FAO soil classification"},
        {value: "immediate_previous_land_use", text: "Immediate Previous Land Use"},
        {value: "agrochemical_additions", text: "Agrochemical Additions"},
        {value: "tillage", text: "Tillage"},
        {value: "fire_history", text: "Fire History"},
        {value: "fire_intensity", text: "Fire Intensity"},
        {value: "environment_event", text: "Environment Events"},
        {value: "moisture", text: "Soil moisture (%)"},
        {value: "colour", text: "Soil Colour"},
        {value: "texture", text: "Texture"},
        {value: "gravel", text: "Gravel (%)"},
        {value: "course_sand", text: "Course Sand (%)"},
        {value: "fine_sand", text: "Fine Sand (%)"},
        {value: "sand", text: "Sand (%)"},
        {value: "silt", text: "Silt (%)"},
        {value: "clay", text: "Clay (%)"},
        {value: "ammonium_nitrogen", text: "Ammonium Nitrogen (mg/Kg)"},
        {value: "nitrate_nitrogen", text: "Nitrate Nitrogen (mg/Kg)"},
        {value: "phosphorus_colwell", text: "Phosphorus Colwell (mg/Kg)"},
        {value: "potassium_colwell", text: "Potassium Colwell (mg/Kg)"},
        {value: "sulphur", text: "Sulphur (mg/Kg)"},
        {value: "organic_carbon", text: "Organic Carbon (%)"},
        {value: "conductivity", text: "Conductivity (dS/m)"},
        {value: "cacl2_ph", text: "pH Level (CaCl2)"},
        {value: "h20_ph", text: "pH Level (H2O)"},
        {value: "dtpa_copper", text: "DTPA Copper (mg/Kg)"},
        {value: "dtpa_iron", text: "DTPA Iron (mg/Kg)"},
        {value: "dtpa_manganese", text: "DTPA Manganese (mg/Kg)"},
        {value: "dtpa_zinc", text: "DTPA Zinc (mg/Kg)"},
        {value: "exc_aluminium", text: "Exc. Aluminium (meq/100g)"},
        {value: "exc_calcium", text: "Exc. Calcium (meq/100g)"},
        {value: "exc_magnesium", text: "Exc. Magnesium (meq/100g)"},
        {value: "exc_potassium", text: "Exc. Potassium (meq/100g)"},
        {value: "exc_sodium", text: "Exc. Sodium (meq/100g)"},
        {value: "boron_hot_cacl2", text: "Boron Hot CaCl2 (mg/Kg)"},
        {value: "total_nitrogen", text: "Total Nitrogen"},
        {value: "total_carbon", text: "Total Carbon"}
    ];

    // helper functions
    function enabled(row, fieldId, bool) {
        var fieldSelector = "[id^='" + fieldId + "']"
        if (bool) {
            $(row).find(fieldSelector).prop("disabled", false);
            $(row).find(fieldSelector).show();
        }
        else {
            $(row).find(fieldSelector).prop("disabled", true);
            $(row).find(fieldSelector).hide();
        }
    }

    function isNumeric(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    }

    var activate = function (row, fieldId) {
        return enabled(row, fieldId, true);
    }

    var deactivate = function (row, fieldId) {
        return enabled(row, fieldId, false);
    }

    function isRangeSearch(row) {
        return $(row).find("[id^=range]").is(":checked");
    }

    function getSearchField(row) {
        return $(row).find("[id^=search_field]");
    }

    function validationErrorMessage(validationMessage) {
        if (validationMessage) {
            $("#validation span").text(validationMessage);
            $("#validation").show();
        }
        else {
            $("#validation").hide();
        }
    }

    function checkStandardised(row, callback) {
        var searchFieldSelect = getSearchField(row);
        var searchField = $(searchFieldSelect).val();
        var url = standardisedVocabularyEndPointURL + searchField;
        $.get(url, callback);
    }

    // utility extension to easily replace options in select - thanks S.O.
    (function ($, window) {
        $.fn.replaceOptions = function (options) {
            var self, $option;

            this.empty();
            self = this;

            $.each(options, function (index, option) {
                $('<option/>').val(option.value).text(option.text).appendTo(self);
            });
        };
    })(jQuery, window);

    function wireUpAllSamplesSearchCheckBox() {
        $("#enable_contextual_filters").click(function () {
            $("#contextual_filter_panel").toggle();

            if ($("#search_all").val() == "search_all") {
                $("#search_all").val("XXXX");
            } else if ($("#search_all").val() == "XXXX") {
                $("#search_all").val("search_all");
            }

        });
    }


    function updateStandardisedOptions(row, standardisedOptions) {
        if (standardisedOptions.length > 0) {
            deactivate(row, "search_value");
            activate(row, "search_standardised_value");
            $(row).find("[id^=search_standardised_value]").replaceOptions(standardisedOptions);
        }

        else {
            activate(row, "search_value");
            deactivate(row, "search_standardised_value");
        }

    }

    function hideOrShowInputs(newRow) {
        // show single field or range ( min and max ) inputs
        var search_field_select = $(newRow).find("[id^=search_field]");
        if (isRangeSearch(newRow)) {
            // change options to fields where a range search makes sense
            $(search_field_select).replaceOptions(rangeFieldOptions);
            // show the range search inputs and hide the single field input
            activate(newRow, "search_range_min");
            activate(newRow, "search_range_max");
            deactivate(newRow, "search_value");
            deactivate(newRow, "search_standardised_value");
        }

        else {
            $(search_field_select).replaceOptions(fieldFieldOptions);
            deactivate(newRow, "search_range_min");
            deactivate(newRow, "search_range_max");
            //$(newRow).find("[id^=search_range_min],[id^=search_range_max] ").hide();

            checkStandardised(newRow, function (standardisedOptions, status) {
                if (status == STATUS_OK) {
                    updateStandardisedOptions(newRow, standardisedOptions);
                }
                else {
                    // this should show the text box
                    updateStandardisedOptions(newRow, null);
                }
            });
        }
    }

    function wireUpSearchFieldSelect(newRow) {
        // if single field search type selected , make the search value field a drop down list for
        // for terms with a standardised vocabulary, otherwise make it a textbox
        if (!isRangeSearch(newRow)) {
            $(newRow).find("[id^=search_field]").change(function () {

                checkStandardised(newRow, function (standardisedOptions, status) {
                    if (status == STATUS_OK) {
                        updateStandardisedOptions(newRow, standardisedOptions);
                    }
                    else {
                        updateStandardisedOptions(newRow, null);
                    }
                });
            });
        }
        else {
            $(newRow).find("[id^=search_field]").unbind("change");
        }
    }

    function wireUpRadioButtons(newRow) {
        // Make the search type radio swap field options
        $(newRow).find("[name^=search_type]").unbind("change");
        $(newRow).find("[name^=search_type]").change(function () {
            hideOrShowInputs(newRow);
            wireUpSearchFieldSelect(newRow);
        });
    }

    function wireUpSearchButton() {
        $("#search_button").click(function () {
            doSearch();
        })
    }

    function incrementValue(value) {
        var pattern = /^(.*)(\d+)$/;
        var prefix = value.match(pattern)[1];
        var oldNumber = parseInt(value.match(pattern)[2]);
        var newNumber = oldNumber + 1;
        return prefix + newNumber;
    }

    function updateIds(newRow) {
        newRow.find("[id^='search_type']," +
                    "[id^='field']," +
                    "[id^='range']," +
                    "[id^='search_field']," +
                    "[id^='search_value']," +
                    "[id^='search_standardised_value']," +
                    "[id^='search_range_min']," +
                    "[id^='search_range_max']").each(
        function (i, val) {
            val.id = incrementValue(val.id);
            try {
                val.name = incrementValue(val.name);
            }
            catch (err) {
            }
            ;
        });
    }

    function addSearchTerm() {
        var lastRow = $("#search_terms > tbody > tr:last");
        var newRow = $(lastRow).clone();
        updateIds(newRow);
        wireUpRadioButtons(newRow);
        hideOrShowInputs(newRow);
        wireUpSearchFieldSelect(newRow);
        $(newRow).insertAfter(lastRow);
    }

    function removeSearchTerm() {
        var numRows = $("#search_terms tr").size() - 1;
        if (numRows > 1) {
            $("#search_terms > tbody > tr:last").remove();
        }

    }

    function getRangeMinValue(row) {
        return $(row).find("[id^='search_range_min']").val();
    }

    function getRangeMaxValue(row) {
        return $(row).find("[id^='search_range_max']").val();
    }

    function getFieldValue(row) {
        return $(row).find("[id^='search_value']").val();
    }

    function isNumericField(fieldName) {

        var NUMERIC_FIELDS = [
            'lat', 'lon', 'elevation', 'moisture', 'texture',
            'course_sand', 'fine_sand', 'sand', 'silt', 'clay',
            'ammonium_nitrogen', 'nitrate_nitrogen', 'phosphorus_colwell',
            'potassium_colwell', 'sulphur', 'organic_carbon', 'conductivity',
            'cacl2_ph', 'h20_ph', 'dtpa_copper', 'dtpa_iron',
            'dtpa_manganese', 'dtpa_zinc', 'exc_aluminium', 'exc_calcium',
            'exc_magnesium', 'exc_potassium', 'exc_sodium', 'boron_hot_cacl2',
            'total_nitrogen', 'total_carbon'];

            return NUMERIC_FIELDS.indexOf(fieldName) > -1;
    }

    function isIntegerField(fieldName) {
        var INTEGER_FIELDS = ['elevation']
        return INTEGER_FIELDS.indexOf(fieldName) > -1;
    }

    function isInteger(value) {
        var pattern = /^\s*\d+\s*$/;
        return value.match(pattern);
    }

    function isDateField(fieldName) {
        var DATE_FIELDS = ['date_sampled'];
        return DATE_FIELDS.indexOf(fieldName) > -1;
    }

    function correctDateFormat(value) {
        var pattern = /^\s*\d\d\d\d-\d\d-\d\d\s*$/;
        return value.match(pattern);
    }

    function validateSearchParameters() {
        var errors = [];
        $("#search_terms > tbody > tr").each(function (i, row) {
            var fieldName = getSearchField(row).find("option:selected").text();
            var fieldCode = getSearchField(row).val();
            if (isRangeSearch(row)) {
                var minValue = getRangeMinValue(row);
                var maxValue = getRangeMaxValue(row);
                if (!isNumeric(minValue)) {
                    var e = fieldName + " minimum value is not a number";
                    errors.push(e);
                }

                if (!isNumeric(maxValue)) {
                    var e = fieldName + " maximum value is not a number";
                    errors.push(e);
                }

                if (isIntegerField(fieldCode) & !isInteger(minValue)) {
                    var e = fieldName + " minimum value is not an integer";
                    errors.push(e);
                }

                if (isIntegerField(fieldCode) & !isInteger(maxValue)) {
                    var e = fieldName + " maximum value is not an integer";
                    errors.push(e);
                }
            }

            else {
                // non range search term
                var fieldValue = getFieldValue(row);
                if (isNumericField(fieldCode)) {
                    if (!isNumeric(fieldValue)) {
                        var e = fieldName + " is numeric but a non numeric value was entered";
                        errors.push(e);
                    }

                    if (isIntegerField(fieldCode) && !isInteger(fieldValue)) {
                        var e = fieldName + " value is not an integer";
                        errors.push(e);
                    }
                }

                if (isDateField(fieldCode) && !correctDateFormat(fieldValue)) {
                    var e = fieldName + " date format is YYYY-MM-DD";
                    errors.push(e);
                }
            }
        });

        if (errors.length > 0) {
            return "Errors found: " + errors.join(";");
        }
        else {
            return "";
        }

    }

    function doSearch() {
        $("#results > tbody > tr").remove();
        validationErrorMessage("");

        var validationErrors = validateSearchParameters();
        if (validationErrors) {
            validationErrorMessage(validationErrors);
            return;
        }

        doSpin();

        $.post(SEARCH_FORM_URL,
               $("#search_form").serialize(),
               displayResults);
    }

    function displayResults(results) {
        // clear table
        $("#results > tbody > tr").remove();

        if (typeof(results) == 'string') {
            // An error happened on the server
            var new_row = '<tr align="center"><td colspan="5"><div class="alert alert-danger">' + results + '</div></td></tr>';
            $("#results > tbody").append(new_row);
            stopSpinner();
            return;
        }

        function link(text, link, missingWord) {
            if (link) {
                if (text != 'Amplicon') {
                    return "<a href='" + link + "' target='_blank'>" + text + "</a>";
                }
                else {
                    var links = "";
                    for (var i = 0; i < link.length; i++) {
                        amplicon_data = link[i];
                        links += "<a href='" + amplicon_data.amplicon_link + "' target='_blank'>" + amplicon_data.amplicon_type + "</a>&nbsp;";
                    }

                    if (links == "") {
                        return missingWord;
                    }
                    else {
                        return links;
                    }
                }
            }
            else {
                return missingWord;
            }
        }

        function td(s) {
            return "<td>" + s + "</td>"
        }

        $(results).each(function (index, item) {
            var new_row = "<tr>" +
                td(link(item.bpa_id, item.sc, "")) +
                td(link(item.sc_display, item.sc, "<span class=\"glyphicon glyphicon-remove\"></span>")) +
                td(link("Chemical Analysis", item.ca, "<span class=\"glyphicon glyphicon-remove\"></span>")) +
                td(link("Amplicon", item.am, "<span class=\"glyphicon glyphicon-remove\"></span>")) +
                td(link("Metagenomics", item.mg, "<span class=\"glyphicon glyphicon-remove\"></span>"))
            "</tr>";

            $("#results > tbody").append(new_row);
        });


        if (results.length == 0) {
            var new_row = '<tr align="center"><td colspan="5"><span class="badge badge-important">No Results</span></td></tr>';
            $("#results > tbody").append(new_row);
        }

        // table sorter
        $("#results").trigger('update') 
        stopSpinner();
    }

    function wireUpClearTaxonomicFiltersButton() {
        $("#clear_taxonomic_filters").click(function () {
            //$("#kingdom option:first").attr('selected','selected').trigger("change");
            $("#kingdom option:first").prop('selected', 'selected').trigger("change");
        })
    }

    function makePopulater(sourceId, targetId) {
        return function () {
            doSpin();
            var sourceValue = $("#" + sourceId).val();
            var taxonomyURL = TAXONOMY_URL + "/" + sourceId + "/" + sourceValue;  // the 'parent' category

            $.get(taxonomyURL, function (childOptions, status) {
                $("#" + targetId).replaceOptions([
                    {value: "---", text: "---"}
                ].concat(childOptions));
                //$("#" + targetId + " option:first").attr('selected', 'selected').trigger("change");
                //$("#" + targetId).find('option:eq(0)').prop('selected', true).trigger("change");
                $('#' + targetId).selectedIndex = 0;
                $('#' + targetId).trigger("change")
                stopSpinner();
            });
        }
    }

    var populatePhylum = makePopulater("kingdom", "phylum");
    var populateClass = makePopulater("phylum", "otu_class");
    var populateOrder = makePopulater("otu_class", "order");
    var populateFamily = makePopulater("order", "family");
    var populateGenus = makePopulater("family", "genus");
    var populateSpecies = makePopulater("genus", "species");

    function wireUpTaxonomyDropDowns() {
        $("#kingdom").change(populatePhylum);
        $("#phylum").change(populateClass);
        $("#otu_class").change(populateOrder);
        $("#order").change(populateFamily);
        $("#family").change(populateGenus);
        $("#genus").change(populateSpecies);
    }

    function wireUpExportSearchResultsButton() {
        function getResultIds() {
            var ids = [];
            $("#results > tbody tr").each(function (i, value) {
                var id = $(value).find("td:first").text();
                ids.push(id);
            })
            return ids;
        }

        function getTaxonomicFilters() {
            var kingdom = $("#kingdom").val();
            var phylum = $("#phylum").val();
            var otu_class = $("#otu_class").val();
            var order = $("#order").val();
            var family = $("#family").val();
            var genus = $("#genus").val();
            var species = $("#species").val();

            return "&kingdom=" + kingdom +
                "&phylum=" + phylum +
                "&otu_class=" + otu_class +
                "&order=" + order +
                "&family=" + family +
                "&genus=" + genus +
                "&species=" + species
        }

        function constructExportQueryString(ids) {
            var s = ids.join(",");

            return "?ids=" + s + getTaxonomicFilters();
        }

        $("#export_button").click(function () {
            var ids = getResultIds();
            var querystring = constructExportQueryString(ids);
            window.open(EXPORT_RESULTS_URL + querystring);
        });
    }

    $("#add_search_term").click(addSearchTerm);
    $("#remove_search_term").click(removeSearchTerm);
    // initialise the handlers on the first row also ( not just dynamically added rows)
    var firstRow = $("#search_terms > tbody > tr:first");
    validationErrorMessage("");
    wireUpRadioButtons(firstRow);
    hideOrShowInputs(firstRow);
    wireUpSearchFieldSelect(firstRow);

    wireUpAllSamplesSearchCheckBox();

    wireUpSearchButton();
    wireUpTaxonomyDropDowns();
    wireUpClearTaxonomicFiltersButton();
    wireUpExportSearchResultsButton();
});
