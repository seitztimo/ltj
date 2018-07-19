/**
 * @file This is a modified version of OLMapWidget.js provided by Django
 * to support the needs of feature geometry editing.
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
            var isMultiGeometry = options.type.indexOf('Multi') > -1;
            options.widget.setIsDrawingMultiGeometry(isMultiGeometry);
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
        this.interactions = {draw: null, modify: null, select: null};
        this.typeChoices = false;
        this.ready = false;

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

        // feature popup
        this.featurePopup = new ol.Overlay({
            element: document.getElementById('popup'),
            autoPan: true,
            autoPanAnimation: {
                duration: 250
            }
        });

        this.map = this.createMap();
        this.featureCollection = new ol.Collection();

        var stroke = new ol.style.Stroke({
            color: [0, 0, 255, 1],
            width: 3
        });
        var fill = new ol.style.Fill({
            color: [0, 0, 255, 0.5]
        });
        this.featureOverlay = new ol.layer.Vector({
            map: this.map,
            source: new ol.source.Vector({
                features: this.featureCollection,
                useSpatialIndex: false // improve performance
            }),
            style: new ol.style.Style({
                stroke: stroke,
                fill: fill,
                image: new ol.style.Circle({
                    stroke: stroke,
                    fill: fill,
                    radius: 5
                })
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
                if (self.isDrawingMultiGeometry()) {
                    // Prevent switching geometry types but allow adding same type geometries
                    self.hideGeomTypeIcons();
                } else if (!self.options.is_collection) {
                    self.disableDrawing(); // Only allow one feature at a time
                }
            }
        });

        var initial_value = document.getElementById(this.options.id).value;
        var initialGeomType = '';
        if (initial_value) {
            var features = jsonFormat.readFeatures('{"type": "Feature", "geometry": ' + initial_value + '}');
            initialGeomType = features[0].getGeometry().getType();
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

        // Enable drawing if editing an existing multi-geometry feature
        if (initialGeomType.indexOf('Multi') > -1) {
            var controlElement = document.getElementsByClassName('type-' + initialGeomType)[0];
            controlElement.click();
        } else {
            this.setIsDrawingMultiGeometry(false);
        }

        this.ready = true;
    }

    MapWidget.prototype.isDrawingMultiGeometry = function() {
        return this._isDrawingMultiGeometry;
    };

    MapWidget.prototype.setIsDrawingMultiGeometry = function(isDrawingMultiGeometry) {
        return this._isDrawingMultiGeometry = isDrawingMultiGeometry;
    };

    MapWidget.prototype.createMap = function() {
        var projection = new ol.proj.Projection({
            code: 'EPSG:3879',
            extent: [21531406.93, 4503686.78, 25664437.76, 9371843.41],
            units: 'm',
            getPointResolution: function(r) {
                return r;
            }
        });
        ol.proj.addProjection(projection);

        var baseLayerGroup = this.getBaseLayerGroup();
        var overLayerGroup = this.getOverlayGroup();
        var map = new ol.Map({
            target: this.options.map_id,
            layers: [baseLayerGroup, overLayerGroup],
            overlays: [this.featurePopup],
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
        var scaleLineControl = new ol.control.ScaleLine();
        map.addControl(scaleLineControl);

        return map;
    };

    MapWidget.prototype.getBaseLayerGroup = function() {
        var wmtsLayers = [
            ['avoindata:Ortoilmakuva', 'Ortoilmakuva'],
            ['avoindata:Opaskartta_PKS', 'Opaskartta PKS'],
            ['avoindata:Kiinteistokartan_maastotiedot', 'Kiinteistokartan maastotiedot'],
            ['avoindata:Kiinteistokartta', 'Kiinteistokartta'],
            ['avoindata:Kantakartan_maastotiedot', 'Kantakartan maastotiedot'],
            ['avoindata:Kantakartta', 'Kantakartta'],
            ['avoindata:Opaskartta_Helsinki', 'Opaskartta Helsinki']
        ].sort(function(a, b) {
            // sort layer in reverse-alphabetic order, the layer order will
            // be reversed when adding to layer switcher
            if (a[1] > b[1]) {
                return -1;
            }
            if (a[1] < b[1]) {
                return 1;
            }
            return 0;
        });
        var wmtsLayerImageFormat = {
            'avoindata:Ortoilmakuva': 'image/jpeg'
        };
        var wmtsOptions = {
            attributions: ['Helsingin kaupungin avoimen datan WMTS-palvelu, CC BY 4.0'],
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

        var baseLayers = wmtsLayers.map(function(wmtsLayer) {
            return new ol.layer.Tile({
                type: 'base',
                title: wmtsLayer[1],
                visible: wmtsLayer[0] === 'avoindata:Opaskartta_Helsinki',
                source: new ol.source.WMTS({
                    attributions: wmtsOptions.attributions,
                    url: 'https://kartta.hel.fi/ws/geoserver/avoindata/gwc/service/wmts',
                    layer: wmtsLayer[0],
                    format: wmtsLayerImageFormat[wmtsLayer[0]] || 'image/png',
                    matrixSet: wmtsOptions.matrixSet,
                    tileGrid: new ol.tilegrid.WMTS({
                        tileSize: wmtsOptions.tileSize,
                        extent: wmtsOptions.extent,
                        origin: wmtsOptions.origin,
                        resolutions: wmtsOptions.resolutions,
                        matrixIds: wmtsOptions.matrixIds
                    }),
                    wrapX: true
                })
            });
        });

        return new ol.layer.Group({
            title: 'Basemaps',
            layers: baseLayers
        });
    };

    MapWidget.prototype.getOverlayGroup = function() {
        var featureWFSLayers = [
            ['rauh_luonnonsuojelualueet', 'Luonnonsuojelualueet'],
            ['rauh_natura', 'Natura-alueet'],
            ['rauh_suojellut_luontotyypit', 'Luonnonsuojelulain mukaiset suojellut luontotyypit'],
            ['rauh_luonnonmuistomerkit', 'Luonnonmuistomerkit'],
            ['suojellut_lajikohteet', 'Suojellut lajikohteet'],
            ['rauh_luonnonsuojeluohjelma', 'Luonnonsuojeluohjelman kohteet'],
            ['arvokkaat_kasvikohteet', 'Arvokkaat kasvillisuus- ja kasvistokohteet'],
            ['arvokkaat_lintukohteet', 'Linnustollisesti arvokkaat kohteet'],
            ['arvo_tarkeat_lepakkoalueet', 'Lepakkokohteet'],
            ['arvokkaat_geologiset', 'Arvokkaat geologiset kohteet'],
            ['arvo_tarkeat_matelija_ja_sammakkoelainkohteet', 'Matelija- ja sammakkoeläinkohteet'],
            ['arvo_kaapakohteet', 'Kääpäkohteet ja orvakkakohteet'],
            ['arvo_metsakohteet', 'Arvokkaat metsäkohteet'],
            ['arvo_liito_orava', 'Liito-oravan ydinalueet'],
            ['muu_perinnemaisemia', 'Perinnemaisemat'],
            ['vesi_lahteet', 'Lähteet'],
            ['vesi_purot_ja_lammet', 'Purot ja lammet'],
            ['vesi_purojen_ja_lampien_valuma_alueet', 'Purojen ja lampien valuma-alueet'],
            ['vesi_purojen_putkitetut_osuudet', 'Purojen putkitetut osuudet'],
            ['muu_elainhavaintoja', 'Eläinhavaintoja'],
            ['muut_luontokohteet', 'Muut luontokohteet'],
            ['vesi_vesikasvilinjat', 'Vesikasvilinjat'],
            ['vesi_vedenalainen_roskaantuminen', 'Vedenalaisen roskan kartoitus']
        ].sort(function(a, b) {
            // sort layer in reverse-alphabetic order, the layer order will
            // be reversed when adding to layer switcher
            if (a[1] > b[1]) {
                return -1;
            }
            if (a[1] < b[1]) {
                return 1;
            }
            return 0;
        });

        self = this;
        var layers = featureWFSLayers.map(function(wfsLayer, index) {
            var colors = self.getWFSColors(index, featureWFSLayers.length);
            var stroke = new ol.style.Stroke({
                color: colors.stroke
            });
            var fill = new ol.style.Fill({
                color: colors.fill
            });
            return new ol.layer.Vector({
                type: 'feature-wfs',
                title: wfsLayer[1],
                visible: false,
                source: new ol.source.Vector({
                    format: new ol.format.GeoJSON(),
                    url: function(extent) {
                        return self.getWFSUrl(wfsLayer[0], extent);
                    },
                    strategy: ol.loadingstrategy.bbox
                }),
                style: new ol.style.Style({
                    stroke: stroke,
                    fill: fill,
                    image: new ol.style.Circle({
                        stroke: stroke,
                        fill: fill,
                        radius: 5
                    })
                })
            });
        });

        return new ol.layer.Group({
            title: 'Overlays',
            layers: layers
        });
    };

    MapWidget.prototype.getWFSColors = function(layerIndex, layerCount) {
        var step = Math.floor(255 / layerCount);
        var offset = step * layerIndex;
        return {
            stroke: [255 - offset, offset, 255 - offset, 1],
            fill: [255 - offset, offset, 255 - offset, 0.1]
        }
    };

    MapWidget.prototype.getWFSUrl = function(typeName, extent) {
        return self.options.wfs_server_url +
            '?service=WFS&version=1.1.0&request=GetFeature' +
            '&typeName=' + typeName + '&outputFormat=application/json' +
            '&srsname=EPSG:3879&bbox=' + extent.join(',') + ',EPSG:3879';
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
            this.map.addControl(new GeometryTypeControl({
                widget: this,
                type: "MultiLineString",
                active: false,
                title: "multi-linestring"
            }));
            this.map.addControl(new GeometryTypeControl({
                widget: this,
                type: "MultiPolygon",
                active: false,
                title: "multi-polygon"
            }));
            this.typeChoices = true;
        }
        this.interactions.draw = new ol.interaction.Draw({
            features: this.featureCollection,
            type: geomType
        });

        // initialize select interaction
        this.interactions.select = new ol.interaction.Select({
            filter: function(feature, layer) {
                return layer && layer.get('type') === 'feature-wfs';
            }
        });
        var selectedFeatures = this.interactions.select.getFeatures();
        var self = this;
        selectedFeatures.on('add', function(event) {
            var feature = event.target.item(0);
            self.showFeaturePopup(feature);
        });
        selectedFeatures.on('remove', function() {
            self.closeFeaturePopup();
        });

        this.map.addInteraction(this.interactions.draw);
        this.map.addInteraction(this.interactions.modify);
        this.map.addInteraction(this.interactions.select)
    };

    MapWidget.prototype.showFeaturePopup = function(feature) {
        var extent = feature.getGeometry().getExtent();
        var center = [(extent[0] + extent[2]) / 2, (extent[1] + extent[3]) / 2];
        var content = document.getElementById('popup-content');
        content.innerHTML = this.getFeaturePopupHtml(feature);
        this.featurePopup.setPosition(center);
    };

    MapWidget.prototype.closeFeaturePopup = function() {
        this.featurePopup.setPosition(undefined);
    };

    MapWidget.prototype.getFeaturePopupHtml = function(feature) {
        var formLink = '<a target="_blank" href="/admin/nature/feature/' +
            feature.get('id') + '/change/">Muokkaa kohde</a>';
        var reportLink = '<a target="_blank" href="/ltj/feature-report/' + feature.get('id') + '/">Kohderaportti</a>';

        return '<p><b>' + feature.get('nimi') + '</b></p>' +
            '<p>' + formLink + '</p>' +
            '<p>' + reportLink + '</p>';
    };

    MapWidget.prototype.defaultCenter = function() {
        var center = [this.options.default_x, this.options.default_y];
        return center;
    };

    MapWidget.prototype.enableDrawing = function() {
        this.interactions.draw.setActive(true);
        this.showGeomTypeIcons();
    };

    MapWidget.prototype.showGeomTypeIcons = function() {
        if (this.typeChoices) {
            var divs = document.getElementsByClassName("switch-type");
            for (var i = 0; i !== divs.length; i++) {
                divs[i].style.visibility = "visible";
            }
        }
    };

    MapWidget.prototype.disableDrawing = function() {
        if (this.interactions.draw) {
            this.interactions.draw.setActive(false);
            this.hideGeomTypeIcons();
        }
    };

    MapWidget.prototype.hideGeomTypeIcons = function() {
        if (this.typeChoices) {
            var divs = document.getElementsByClassName("switch-type");
            for (var i = 0; i !== divs.length; i++) {
                divs[i].style.visibility = "hidden";
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
        if (this.options.is_collection || this.isDrawingMultiGeometry()) {
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
