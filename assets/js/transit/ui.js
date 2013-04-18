define(["jquery",
        "transit/templates",
        "transit/api",
        "transit/maps",
        "transit/config"],
        function ($, templates, api, maps, config) {
    'use strict';

    var ui = {};

    function populateTracks() {
        var options = $('select#' + config.ui.tracksDiv);

        function fillValues(values) {

            options
                .empty()
                .append($('<option />').val('').text('Select an option'));
            $.each(values, function () {
                options.append($('<option />')
                    .val(this.filename)
                    .text(this.name));
            });
        };
        api.getTracks(fillValues.routes);

        return this;
    };
    function populateSelect(selectDiv, values) {
        var options = $('select#' + selectDiv);
        options
            .empty()
            .append($('<option />').val('none').text('Select an option'));
        $.each(values, function() {
            options.append($('<option />')
                .val(this.route_id)
                .text(this.route_id));
        });
    };

    function populateRoutes() {
        api.getRoutes(function (values) {
            populateSelect(config.ui.routesDiv, values.routes);
        });
        return this;
    };

    function populateTrips(route_id) {
        var options = $('select#' + config.ui.tripsDiv);
        function fillValues(values) {
            options
                .empty()
                .append($('<option />').val('none').text('Select an option'));
            $.each(values.trips, function() {
                options.append($('<option />')
                    .val(this.trip_id)
                    .text('Hacia ' + this.trip_headsign)
                    .attr('trip_id', this.trip_id));
            });
        };
        api.getTrips(route_id, fillValues);
        return this;
    };

    function setupTabs() {
        $('a[data-toggle="tab"]').on('shown', function (e) {
            if (e.target.hash == '#stopsTab') {
                maps.toggleLayer('bbox',true);
                maps.controls.selectStops.deactivate();
                maps.controls.selectMultiple.activate();
            } else if (e.target.hash == '#tripsTab') {
                maps.controls.selectMultiple.deactivate();
                maps.controls.selectStops.activate();
            };
        });
    };

    function setupButtons() {
        $('select#' + config.ui.routesDiv).change(function () {
            var route_id = $(this).find(':selected')[0].value;
            maps.update({route_id:route_id,shape_id:'',trip_id:''});
            populateTrips(route_id);
            renderServices(route_id);
            renderStopInfo(null);
        });
        
        $('select#' + config.ui.tripsDiv).change(function () {
            var selected = $(this).find(':selected')[0];
            var trip_id = $(selected).attr('trip_id');
            maps.update({shape_id:trip_id, trip_id:trip_id});
            renderStopInfo(null);
        });

        $('select#' + config.ui.tracksDiv).change(function () {
            var selected = $(this).find(':selected')[0];
            var track = $(selected).val();
            maps.update({track:track});
        });
        
        function saveStops() {
            var readStops = maps.readStops();
            // TODO trip_id <> shape_id in general
            api.saveStops(readStops.trip_id, 
                readStops.stops, 
                function(response){
                    maps.update();
                }
            );
        };
        

        $('#prevStop').click(maps.skipHandler(-1));
        $('#nextStop').click(maps.skipHandler(1));

        $('#editShape').toggle(
            function () {
                $(this).addClass('btn-primary');
                maps.controls.selectStops.deactivate();
                maps.controls.modifyShape.activate();
            },
            function () {
                $(this).removeClass('btn-primary');
                maps.controls.modifyShape.deactivate();
                maps.controls.selectStops.activate();
                var readShape = maps.readShape();
                api.saveShape(readShape.shape, function(response) {
                    console.log(response);
                });
            }
        );

        $('#revShape').click(function (e){
            var selected = $('#tripsSelect').find(':selected')[0],
                trip_id;
            trip_id = $(selected).val();
            e.preventDefault();
            api.revShape(trip_id, function(response) {
                maps.update();
            });
        });

        $('#sortStops').click(function (e){
            var selected = $('#tripsSelect').find(':selected')[0],
                trip_id;
            trip_id = $(selected).val();
            e.preventDefault();
            api.sortStops(trip_id, function(response) {
                maps.update();
            });
        });

        $('#offsetStops').click(function (e){
            var selected = $('#tripsSelect').find(':selected')[0],
                trip_id;
            trip_id = $(selected).val();
            e.preventDefault();
            api.offsetStops(trip_id, function(response) {
                maps.update();
            });
        });

        $('#editStops').toggle(
            function () {
                $(this).addClass('btn-primary');
                maps.controls.selectStops.deactivate();
                maps.controls.modifyStops.activate();
            }, 
            function () {
                $(this).removeClass('btn-primary');
                maps.controls.modifyStops.deactivate();
                maps.controls.selectStops.activate();
                saveStops();
            }
        );

        $('#drawStops').toggle(
            function () {
                $(this).addClass('btn-primary');
                maps.controls.selectStops.deactivate();
                maps.controls.drawStops.activate();
            },
            function () {
                $(this).removeClass('btn-primary');
                maps.controls.drawStops.deactivate();
                maps.controls.selectStops.activate();
                saveStops();
            }
        );
        
        $('#removeStop').click(function (e) {
            e.preventDefault();
            maps.destroySelected();
            saveStops();
        });

        $('#toggleTimepoint').click(function (e) {
            var tripsSelected = $('#tripsSelect').find(':selected')[0],
                spec = {};
            e.preventDefault();
            spec.trip_id = $(tripsSelected).val();
            spec.stop_id = maps.getSelectedStop()['fid'];
            api.toggleTimepoint(spec,function (result) {
                console.log(result);
            });
            maps.update();
        });

        $('#appendStop').click(function (e){
            e.preventDefault();
            maps.appendSelected();
            saveStops();
        });

        // buttons on the Stops tab
        $('#findStop').on('click', function (event){
            var stop_id = $('#stop_id').val();
            api.findStop(stop_id, function(response) {
                console.log(response);
                maps.utiles.setCenter({
                    lon: response.lon,
                    lat: response.lat,
                    zoom: 18
                });
            });
        });
        $("#stop_id").keyup(function(event){
            if(event.keyCode == 13){
                $("#findStop").click();
            }
        });

        $('#moveStops').toggle(
            function () {
                $(this).addClass('btn-primary');
                maps.controls.selectMultiple.deactivate();
                maps.controls.modifyBbox.activate();
            }, 
            function () {
                $(this).removeClass('btn-primary');
                maps.controls.modifyBbox.deactivate();
                maps.controls.selectMultiple.activate();
                //saveStops();
            }
        );

        
        return this;
    };

    function renderServices(route_id) {
        var fillSchedule = function (data) {
            var scheduleDiv = $('#schedule');
            scheduleDiv.empty();
            scheduleDiv.append(templates.schedule(data));
        };
        api.getServices(route_id, fillSchedule);
    };

    function renderStopsTable(trip_id) {
        var stopsTemplate = template.stopsTemplate;
        var stopsRenderer = function(data) {
            $('#'+transit.controlsModule.config.stopsDiv).empty().append(stopsTemplate(data));
            $('#'+transit.controlsModule.config.stopsDiv+' table tr').on('hover',function(e){
                console.log(e);
            });
        };
        api.getTripStops(trip_id,stopsRenderer);
    };

    function handleMerger(spec) {
        var merge;
        merge = JSON.stringify(spec.merge);
        api.mergeStops(spec.keep,merge,
            function (response) {
                console.log(response);
        });
    };

    function renderStopInfo(evt) {
        var selectedFeature;
        if (evt && (evt.type == 'featureselected')) {
            selectedFeature = evt.feature;
        } else {
            selectedFeature = null;
        };
        var stopInfoDiv = $('#stopData');
        stopInfoDiv.empty();
        if (selectedFeature) {
            stopInfoDiv.append(templates.stops(selectedFeature));
        };
    };
    
    function renderMultipleStops(evt) {
        var selected,
            multipleDiv;
        selected = maps.bboxGetSelected();
        multipleDiv = $('#multipleStops');
        multipleDiv.empty();
        if (selected.length == 1) {
            multipleDiv.append(stopTemplate(selected[0]));
        } else {
            multipleDiv.append(multipleTemplate({features:selected}));
        };
        $('#multipleStops table tr button').on('click',function(e){
            var merge = [],
                keep = e.currentTarget.id;

            for (var i = 0; i < selected.length; i++) {
                merge.push(selected[i]['fid']);
            };
            handleMerger({
                keep: keep,
                merge: merge
            });
            maps.update();
        });
    };

    function bindLayerControls() {
        $('#' + config.layersDiv + ' :checkbox').click(function() {
                var layerId = $(this)[0].value;
                if ($(this).is(':checked')) {
                    maps.map.getLayer(layerId).setVisibility(true);
                } else {
                    maps.map.getLayer(layerId).setVisibility(false);
                }
            }
        );
    };

    ui.init = function (spec) {

        if (spec.controls == 'editor') {
            //templates.multiple;
        }

        // populate selection controls
        //populateTracks();
        populateRoutes();

        // setup button actions
        setupButtons();
        setupTabs();
        //~ bindLayerControls();
        //

        maps.setEventHandlers({
            renderStopInfo:renderStopInfo,
            renderMultipleStops:renderMultipleStops
        });
    };
    
    return ui;
});
