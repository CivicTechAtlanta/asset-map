// foursquare integration

var govtIcon = L.AwesomeMarkers.icon({
  icon: 'university',
  prefix: 'fa',
  markerColor: 'green'
});

var config = {
  apiKey: 'EJAXVB3GXRY550WSHRBEVAHYKIKGHW0YXHQIVJVMMF3OLQID',
  authUrl: 'https://foursquare.com/',
  apiUrl: 'https://api.foursquare.com/'
};

var CLIENT_ID = 'EJAXVB3GXRY550WSHRBEVAHYKIKGHW0YXHQIVJVMMF3OLQID'
var CLIENT_SECRET = 'OPOIMXAYAEIDLPH1E1GB2HDF4UKJVATA25R2LJVCFQX4GOZK'

var API_ENDPOINT = 'https://api.foursquare.com/v2/venues/search' +
  '?client_id=CLIENT_ID' + 
  '&client_secret=CLIENT_SECRET' +
  '&v=20130815' +
  '&ll=33.74986,-84.39223' + 
  '&radius=889' +
  '&limit=50' +
  '&intent=browse' +
  // '&query=coffee' +
  '&categoryId=4bf58dd8d48988d126941735' +
  '&callback=?';

var foursquarePlaces = L.layerGroup().addTo(map);

$.getJSON(API_ENDPOINT
  .replace('CLIENT_ID', CLIENT_ID)
  .replace('CLIENT_SECRET', CLIENT_SECRET), function(result, status) {

    if (status !== 'success') return alert('Request to Foursquare failed');

    // transform venue result into map marker
    for (var i = 0; i < result.response.venues.length; i++) {
      var venue = result.response.venues[i];
      var latlng = L.latLng(venue.location.lat, venue.location.lng);
      var marker = L.marker(latlng, {
        icon: govtIcon
      })
      .bindPopup('<strong><a href="https://foursquare.com/v/' + venue.id + '" target="_blank">' + venue.name + '</a></strong>')
      .addTo(foursquarePlaces);
    }

  });


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
  "<i class='fa fa-subway' style='color:#D43E2A'></i> MARTA Train Stations": MARTALayer,
  "<i class='fa fa-subway' style='color:#38AADD'></i> Historical Markers": historicalMarkersLayer,
  "<span style='color: #8e44ad;'>▌</span>Landmarks": landmarksLayer,
  "<i class='fa fa-university' style='color:#72AF26'></i> Government Buildings <img src='images/foursquare-logomark.png' width='18' valign='bottom'>": foursquarePlaces
};

L.control.layers(null, overlayMaps, {
  collapsed: false
}).addTo(map);

