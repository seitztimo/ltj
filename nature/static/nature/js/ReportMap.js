(function() {
    'use strict';

    function ReportMap(target, featureGeometry) {
        this.baseLayers = this.createBaseLayers();
        this.featureLayer = this.createFeatureLayer();
        this.map = this.createMap(target);
        this.addFeature(featureGeometry)
    }

    ReportMap.prototype.createBaseLayers = function() {
        var wmtsLayerNames = [
            'avoindata:Opaskartta_Helsinki',
            'avoindata:Kantakartta',
            'avoindata:Kantakartan_maastotiedot',
            'avoindata:Kiinteistokartta',
            'avoindata:Kiinteistokartan_maastotiedot',
            'avoindata:Opaskartta_PKS',
            'avoindata:Ortoilmakuva'
        ];
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
        var baseLayers = [];
        for (var i=0; i<wmtsLayerNames.length; i++) {
            var layerName = wmtsLayerNames[i];
            var layer = new ol.layer.Tile({
                title: layerName,
                visible: layerName === 'avoindata:Ortoilmakuva',
                source: new ol.source.WMTS({
                    attributions: wmtsOptions.attributions,
                    url: 'https://kartta.hel.fi/ws/geoserver/avoindata/gwc/service/wmts',
                    layer: layerName,
                    format: wmtsLayerImageFormat[layerName] || 'image/png',
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
            baseLayers.push(layer);
        }
        return baseLayers;
    };

    ReportMap.prototype.createFeatureLayer = function() {
        return new ol.layer.Vector({
            source: new ol.source.Vector()
        });
    };

    ReportMap.prototype.createControls = function() {
        var scaleLine = new ol.control.ScaleLine();
        var attribution = new ol.control.Attribution({collapsible: false});
        return [scaleLine, attribution];
    };

    ReportMap.prototype.createMap = function(target) {
        var projection = new ol.proj.Projection({
            code: 'EPSG:3879',
            extent: [21531406.93, 4503686.78, 25664437.76, 9371843.41],
            units: 'm',
            getPointResolution: function(r) {
                return r;
            }
        });

        var map = new ol.Map({
            target: target,
            layers: this.baseLayers.concat([this.featureLayer]),
            controls: this.createControls(),
            interactions: [],
            view: new ol.View({
                projection: projection,
                zoom: 12,
                extent: projection.getExtent()
            })
        });

        return map;
    };

    ReportMap.prototype.addFeature = function(featureGeometry) {
        var jsonFormat = new ol.format.GeoJSON();
        var feature = jsonFormat.readFeature('{"type": "Feature", "geometry": ' + featureGeometry + '}');
        this.featureLayer.getSource().addFeature(feature);
        this.map.getView().fit(feature.getGeometry(), {maxZoom: 15});
    };

    ReportMap.prototype.changeLayer = function(layerName) {
        this.baseLayers.forEach(function(layer) {
            layer.setVisible(layer.get('title') === layerName);
        });
    };

    window.ReportMap = ReportMap;
})();
