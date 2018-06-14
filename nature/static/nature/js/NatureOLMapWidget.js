/**
 * @file This is a modified version of OLMapWidget.js provided by Django
 * to support the needs of feature geometry editing.
 *
 * List of modifications:
 * - Set map projection to EPSG:3879
 * - Add custom base maps (WMTS)
 * - Scale bar
 * - Coordinates at mouse
 */

var GeometryTypeControl = function(opt_options) {
    'use strict';
    // Map control to switch type when geometry type is unknown
    var options = opt_options || {};

    var element = document.createElement('div');
    element.className = 'switch-type type-' + options.type + ' ol-control ol-unselectable';
    if (options.active) {
        element.className += " type-active";
    }
    element.title = options.title;

    var self = this;
    var switchType = function(e) {
        e.preventDefault();
        if (options.widget.currentGeometryType !== self) {
            options.widget.map.removeInteraction(options.widget.interactions.draw);
            options.widget.interactions.draw = new ol.interaction.Draw({
                features: options.widget.featureCollection,
                type: options.type
            });
            options.widget.map.addInteraction(options.widget.interactions.draw);
            var className = options.widget.currentGeometryType.element.className.replace(/ type-active/g, '');
            options.widget.currentGeometryType.element.className = className;
            options.widget.currentGeometryType = self;
            element.className += " type-active";
        }
    };

    element.addEventListener('click', switchType, false);
    element.addEventListener('touchstart', switchType, false);

    ol.control.Control.call(this, {
        element: element
    });
};
ol.inherits(GeometryTypeControl, ol.control.Control);

(function() {
    'use strict';
    var jsonFormat = new ol.format.GeoJSON();

    function MapWidget(options) {
        this.map = null;
        this.interactions = {draw: null, modify: null};
        this.typeChoices = false;
        this.ready = false;

        // WMTS layers and options
        this.wmtsLayerNames = [
            'avoindata:Ortoilmakuva',
            'avoindata:Opaskartta_PKS',
            'avoindata:Kiinteistokartan_maastotiedot',
            'avoindata:Kiinteistokartta',
            'avoindata:Kantakartan_maastotiedot',
            'avoindata:Kantakartta',
            'avoindata:Opaskartta_Helsinki'
        ];
        this.wmtsLayerImageFormat = {
            'avoindata:Ortoilmakuva': 'image/jpeg'
        };
        this.wmtsOptions = {
            url: 'https://kartta.hel.fi/ws/geoserver/avoindata/gwc/service/wmts',
            matrixSet: 'ETRS-GK25',
            tileSize: [256, 256],
            extent: [25440000, 6630000, 25571072, 6761072],
            origin: [25440000, 6761072],
            resolutions: [256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625],
            matrixIds: [
                'ETRS-GK25:0', 'ETRS-GK25:1', 'ETRS-GK25:2',
                'ETRS-GK25:3', 'ETRS-GK25:4', 'ETRS-GK25:5',
                'ETRS-GK25:6', 'ETRS-GK25:7', 'ETRS-GK25:8',
                'ETRS-GK25:9', 'ETRS-GK25:10', 'ETRS-GK25:11',
                'ETRS-GK25:12'
            ]
        };

        // Default options
        this.options = {
            default_y: 0,
            default_x: 0,
            default_zoom: 12,
            is_collection: options.geom_name.indexOf('Multi') > -1 || options.geom_name.indexOf('Collection') > -1
        };

        // Altering using user-provided options
        for (var property in options) {
            if (options.hasOwnProperty(property)) {
                this.options[property] = options[property];
            }
        }
        if (!options.base_layer) {
            this.options.base_layer = new ol.layer.Tile({source: new ol.source.OSM()});
        }

        this.map = this.createMap();
        this.featureCollection = new ol.Collection();
        this.featureOverlay = new ol.layer.Vector({
            map: this.map,
            source: new ol.source.Vector({
                features: this.featureCollection,
                useSpatialIndex: false // improve performance
            }),
            updateWhileAnimating: true, // optional, for instant visual feedback
            updateWhileInteracting: true // optional, for instant visual feedback
        });

        // Populate and set handlers for the feature container
        var self = this;
        this.featureCollection.on('add', function(event) {
            var feature = event.element;
            feature.on('change', function() {
                self.serializeFeatures();
            });
            if (self.ready) {
                self.serializeFeatures();
                if (!self.options.is_collection) {
                    self.disableDrawing(); // Only allow one feature at a time
                }
            }
        });

        var initial_value = document.getElementById(this.options.id).value;
        if (initial_value) {
            var features = jsonFormat.readFeatures('{"type": "Feature", "geometry": ' + initial_value + '}');
            var extent = ol.extent.createEmpty();
            features.forEach(function(feature) {
                this.featureOverlay.getSource().addFeature(feature);
                ol.extent.extend(extent, feature.getGeometry().getExtent());
            }, this);
            // Center/zoom the map
            this.map.getView().fit(extent, {maxZoom: this.options.default_zoom});
        } else {
            this.map.getView().setCenter(this.defaultCenter());
        }
        this.createInteractions();
        if (initial_value && !this.options.is_collection) {
            this.disableDrawing();
        }
        this.ready = true;
    }

    MapWidget.prototype.createMap = function() {
        var projection = new ol.proj.Projection({
            code: 'EPSG:3879',
            extent: [21531406.93, 4503686.78, 25664437.76, 9371843.41],
            units: 'm'
        });
        ol.proj.addProjection(projection);

        var baseLayerGroup = this.getBaseLayerGroup();
        var map = new ol.Map({
            target: this.options.map_id,
            layers: [baseLayerGroup],
            view: new ol.View({
                projection: projection,
                zoom: this.options.default_zoom,
                extent: projection.getExtent()
            })
        });

        // Add layer switcher
        var layerSwitcher = new ol.control.LayerSwitcher({
            tipLabel: 'Layers'
        });
        map.addControl(layerSwitcher);


        // Add mouse position coordiantes
        var mousePositionControl = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(4),
            projection: 'EPSG:3879',
            className: 'nature-mouse-position'
        });
        map.addControl(mousePositionControl);

        // Add scale line
        var scaleLineControl = new ol.control.ScaleLine({
            units: 'metric',
        });
        map.addControl(scaleLineControl);

        return map;
    };

    MapWidget.prototype.getBaseLayerGroup = function() {
        var baseLayers = [];
        for (var i=0; i<this.wmtsLayerNames.length; i++) {
            var layerName = this.wmtsLayerNames[i];
            var layer = new ol.layer.Tile({
                type: 'base',
                title: layerName,
                source: new ol.source.WMTS({
                    url: 'https://kartta.hel.fi/ws/geoserver/avoindata/gwc/service/wmts',
                    layer: layerName,
                    format: this.wmtsLayerImageFormat[layerName] || 'image/png',
                    matrixSet: this.wmtsOptions.matrixSet,
                    tileGrid: new ol.tilegrid.WMTS({
                        tileSize: this.wmtsOptions.tileSize,
                        extent: this.wmtsOptions.extent,
                        origin: this.wmtsOptions.origin,
                        resolutions: this.wmtsOptions.resolutions,
                        matrixIds: this.wmtsOptions.matrixIds
                    }),
                    wrapX: true
                })
            });
            baseLayers.push(layer);
        }
        return new ol.layer.Group({
            title: 'Base maps',
            layers: baseLayers
        });
    };

    MapWidget.prototype.createInteractions = function() {
        // Initialize the modify interaction
        this.interactions.modify = new ol.interaction.Modify({
            features: this.featureCollection,
            deleteCondition: function(event) {
                return ol.events.condition.shiftKeyOnly(event) &&
                    ol.events.condition.singleClick(event);
            }
        });

        // Initialize the draw interaction
        var geomType = this.options.geom_name;
        if (geomType === "Unknown" || geomType === "GeometryCollection") {
            // Default to Point, but create icons to switch type
            geomType = "Point";
            this.currentGeometryType = new GeometryTypeControl({
                widget: this,
                type: "Point",
                active: true,
                title: "Piste"
            });
            this.map.addControl(this.currentGeometryType);
            this.map.addControl(new GeometryTypeControl({
                widget: this,
                type: "LineString",
                active: false,
                title: "Viiva"
            }));
            this.map.addControl(new GeometryTypeControl({
                widget: this,
                type: "Polygon",
                active: false,
                title: "Monikulmio"
            }));
            this.typeChoices = true;
        }
        this.interactions.draw = new ol.interaction.Draw({
            features: this.featureCollection,
            type: geomType
        });

        this.map.addInteraction(this.interactions.draw);
        this.map.addInteraction(this.interactions.modify);
    };

    MapWidget.prototype.defaultCenter = function() {
        var center = [this.options.default_x, this.options.default_y];
        return center;
    };

    MapWidget.prototype.enableDrawing = function() {
        this.interactions.draw.setActive(true);
        if (this.typeChoices) {
            // Show geometry type icons
            var divs = document.getElementsByClassName("switch-type");
            for (var i = 0; i !== divs.length; i++) {
                divs[i].style.visibility = "visible";
            }
        }
    };

    MapWidget.prototype.disableDrawing = function() {
        if (this.interactions.draw) {
            this.interactions.draw.setActive(false);
            if (this.typeChoices) {
                // Hide geometry type icons
                var divs = document.getElementsByClassName("switch-type");
                for (var i = 0; i !== divs.length; i++) {
                    divs[i].style.visibility = "hidden";
                }
            }
        }
    };

    MapWidget.prototype.clearFeatures = function() {
        this.featureCollection.clear();
        // Empty textarea widget
        document.getElementById(this.options.id).value = '';
        this.enableDrawing();
    };

    MapWidget.prototype.serializeFeatures = function() {
        // Three use cases: GeometryCollection, multigeometries, and single geometry
        var geometry = null;
        var features = this.featureOverlay.getSource().getFeatures();
        if (this.options.is_collection) {
            if (this.options.geom_name === "GeometryCollection") {
                var geometries = [];
                for (var i = 0; i < features.length; i++) {
                    geometries.push(features[i].getGeometry());
                }
                geometry = new ol.geom.GeometryCollection(geometries);
            } else {
                geometry = features[0].getGeometry().clone();
                for (var j = 1; j < features.length; j++) {
                    switch(geometry.getType()) {
                        case "MultiPoint":
                            geometry.appendPoint(features[j].getGeometry().getPoint(0));
                            break;
                        case "MultiLineString":
                            geometry.appendLineString(features[j].getGeometry().getLineString(0));
                            break;
                        case "MultiPolygon":
                            geometry.appendPolygon(features[j].getGeometry().getPolygon(0));
                    }
                }
            }
        } else {
            if (features[0]) {
                geometry = features[0].getGeometry();
            }
        }
        document.getElementById(this.options.id).value = jsonFormat.writeGeometry(geometry);
    };

    window.MapWidget = MapWidget;
})();
