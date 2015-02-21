
// map

L.control.attribution({position: 'bottomleft'}).addTo(map);

L.tileLayer('http://otile4.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
  attribution: 'Tiles &copy; <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png" /><br>' +
  'Made at <a href="http://www.codeforamerica.org/events/codeacross-2015/">CodeAcross</a> for <a href="http://www.codeforatlanta.org/"><img src="images/code-for-atlanta.png" height=70></a>',
  maxZoom: 18
}).addTo(map);

var southDowntownLayer = L.geoJson(southDowntown, {
  onEachFeature: function(feature, layer) {
    layer.bindPopup(feature.properties.name);
  },
  style: {color: '#007df0',
    opacity: 1},
}).addTo(map);

var trainIcon = L.AwesomeMarkers.icon({
  icon: 'subway',
  prefix: 'fa',
  markerColor: 'red'
});

var MARTALayer = L.geoJson(marta, {
  onEachFeature: function(feature, layer) {layer.bindPopup(feature.properties.Description)},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: trainIcon});
  }
}).addTo(map);

var markerIcon = L.AwesomeMarkers.icon({
  icon: 'flag',
  prefix: 'fa',
  markerColor: 'blue'
});

var historicalMarkersLayer = L.geoJson(historicalMarkers, {
  onEachFeature: function(feature, layer) {layer.bindPopup("<b>Historical Marker</b><br>" + feature.properties.name + "<br>" + feature.properties.cmt + "<br>" + feature.properties.desc + "<br><a href='" + feature.properties.link1_href + "'>Additional information on HMdb.org</a>")},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: markerIcon});
  }
}).addTo(map);

function onEachLandmark(feature, layer) {
  layer.bindPopup(feature.properties.BUILDING_N + "<br>" + feature.properties.FIELD5);
};

var landmarksLayer = L.geoJson(landmarks, {
  onEachFeature: onEachLandmark,
  style: {color: '#8e44ad',
    fillOpacity: 0.6,
    weight: 0},
}).addTo(map);

var overlayMaps = {
  "MARTA Train Stations": MARTALayer,
  "Historical Markers": historicalMarkersLayer,
  "<span style='color: #8e44ad;'>▌</span>Landmarks": landmarksLayer
};

L.control.layers(null, overlayMaps, {
  collapsed: false
}).addTo(map);

