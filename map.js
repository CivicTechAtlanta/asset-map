// images

var historicalMapLayer = L.imageOverlay('data/1949.png', 
  [[33.74123662962249, -84.39920425415039],[33.758035496175616,-84.37899112701415]],
  {opacity: 0.9});

var neighborhoodProfileLayer = L.imageOverlay('data/neighborhood-profile.png', 
  [[33.743383923408516, -84.40467596054077],[33.7700260223456,-84.36972141265869]],
  {opacity: 0.9});

// foursquare integration

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
  '&categoryId=CATEGORY_ID' +
  '&callback=?';

var governmentBuildingsLayer = L.layerGroup();
$.getJSON(API_ENDPOINT
  .replace('CLIENT_ID', CLIENT_ID)
  .replace('CLIENT_SECRET', CLIENT_SECRET)
  .replace('CATEGORY_ID', '4bf58dd8d48988d126941735'), function(result, status) {

    if (status !== 'success') return alert('Request to Foursquare failed');

    // transform venue result into map marker
    for (var i = 0; i < result.response.venues.length; i++) {
      var venue = result.response.venues[i];
      var latlng = L.latLng(venue.location.lat, venue.location.lng);
      var marker = L.marker(latlng, {
        icon: L.AwesomeMarkers.icon({
          icon: 'university',
          prefix: 'fa',
          markerColor: 'green'
        })
      })
      .bindPopup('<strong><a href="https://foursquare.com/v/' + venue.id + '" target="_blank">' + venue.name + '</a></strong><br>' + venue.categories[0]["name"])
      .addTo(governmentBuildingsLayer);
    }

  });

var entertainmentLayer = L.layerGroup();
$.getJSON(API_ENDPOINT
  .replace('CLIENT_ID', CLIENT_ID)
  .replace('CLIENT_SECRET', CLIENT_SECRET)
  .replace('CATEGORY_ID', '4bf58dd8d48988d1f1931735'), function(result, status) {

    if (status !== 'success') return alert('Request to Foursquare failed');

    // transform venue result into map marker
    for (var i = 0; i < result.response.venues.length; i++) {
      var venue = result.response.venues[i];
      var latlng = L.latLng(venue.location.lat, venue.location.lng);
      var marker = L.marker(latlng, {
        icon: L.AwesomeMarkers.icon({
          icon: 'birthday-cake',
          prefix: 'fa',
          markerColor: 'purple'
        })
      })
      .bindPopup('<strong><a href="https://foursquare.com/v/' + venue.id + '" target="_blank">' + venue.name + '</a></strong><br>' + venue.categories[0]["name"])
      .addTo(entertainmentLayer);
    }

  });

var residentialLayer = L.layerGroup();
$.getJSON(API_ENDPOINT
  .replace('CLIENT_ID', CLIENT_ID)
  .replace('CLIENT_SECRET', CLIENT_SECRET)
  .replace('CATEGORY_ID', '4d954b06a243a5684965b473'), function(result, status) {

    if (status !== 'success') return alert('Request to Foursquare failed');

    // transform venue result into map marker
    for (var i = 0; i < result.response.venues.length; i++) {
      var venue = result.response.venues[i];
      var latlng = L.latLng(venue.location.lat, venue.location.lng);
      var marker = L.marker(latlng, {
        icon: L.AwesomeMarkers.icon({
          icon: 'home',
          prefix: 'fa',
          markerColor: 'darkpurple'
        })
      })
      .bindPopup('<strong><a href="https://foursquare.com/v/' + venue.id + '" target="_blank">' + venue.name + '</a></strong><br>' + venue.categories[0]["name"])
      .addTo(residentialLayer);
    }

  });

var foodLayer = L.layerGroup();
$.getJSON(API_ENDPOINT
  .replace('CLIENT_ID', CLIENT_ID)
  .replace('CLIENT_SECRET', CLIENT_SECRET)
  .replace('CATEGORY_ID', '4d4b7105d754a06374d81259'), function(result, status) {

    if (status !== 'success') return alert('Request to Foursquare failed');

    // transform venue result into map marker
    for (var i = 0; i < result.response.venues.length; i++) {
      var venue = result.response.venues[i];
      var latlng = L.latLng(venue.location.lat, venue.location.lng);
      var marker = L.marker(latlng, {
        icon: L.AwesomeMarkers.icon({
          icon: 'cutlery',
          prefix: 'fa',
          markerColor: 'darkgreen'
        })
      })
      .bindPopup('<strong><a href="https://foursquare.com/v/' + venue.id + '" target="_blank">' + venue.name + '</a></strong><br>' + venue.categories[0]["name"])
      .addTo(foodLayer);
    }

  });


// shapefiles

var NSPLayer = L.shapefile('data/NSP.zip', {
  onEachFeature: function(feature, layer) {
    layer.bindPopup("");
  },
  style: {color: '#00ffff',
    opacity: 1,
    weight: 1},
});

var cityCouncilLayer = L.shapefile('data/city-council.zip', {
  onEachFeature: function(feature, layer) {
    layer.bindPopup("City council district: " + feature.properties.DISTRICT);
  },
  style: {color: '#0000ff',
    opacity: 1,
    weight: 2},
});

var TADLayer = L.shapefile('data/TAD.zip', {
  onEachFeature: function(feature, layer) {
    layer.bindPopup(feature.properties.TAD_NAME + " TAD");
  },
  style: {color: '#00B200',
    opacity: 1,
    weight: 4},
});

var zoningLayer = L.shapefile('data/zoning-base-updated.zip', {
  onEachFeature: function(feature, layer) {
    layer.bindPopup("Status: " + feature.properties.STATUS + "<br>Zoning: " + feature.properties.ZONING);
  },
  style: {color: '#ff0000',
    opacity: 1,
    weight: 3},
});

var parcelLayer = L.shapefile('data/SD_parcel2012/southDowntown_parcels2012.zip', {
  onEachFeature: function(feature, layer) {
    layer.bindPopup("Parcel ID: <a href='http://qpublic9.qpublic.net/ga_display_dw.php?county=ga_fulton&KEY=" + feature.properties.PARID + "' target='_blank'>" + feature.properties.PARID + "</a><br>" + feature.properties.LandUseSpe + "<br>" + feature.properties.SITUS);
  },
  style: {color: '#f07300',
    opacity: 1,
    weight: 1},
});

var censusBlocksLayer = L.shapefile('data/census-blocks.zip', {
  onEachFeature: function(feature, layer) {
    var popdens = (isNaN(feature.properties.popdens)) ? 0 : feature.properties.popdens;
    layer.bindPopup("Census Block " + feature.properties.GEOID10 + "<br>Population density: " + popdens + " people per km<sup>2</sup>");
  },
  style: function(feature) {
    var popdens = (isNaN(feature.properties.popdens)) ? 0 : feature.properties.popdens;
    return {
      fillOpacity: (popdens / 10000) + 0.1,
      weight: 1,
      opacity: 1,
      color: '#f8b50c'
    };
  }
});


// standard layers

var southDowntownLayer = L.geoJson(southDowntown, {
  onEachFeature: function(feature, layer) {
    layer.bindPopup(feature.properties.name);
  },
  style: {color: '#007df0',
    opacity: 1},
});

var MARTALayer = L.geoJson(marta, {
  onEachFeature: function(feature, layer) {layer.bindPopup(feature.properties.Description)},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: L.AwesomeMarkers.icon({
      icon: 'subway',
      prefix: 'fa',
      markerColor: 'orange'
    })
  });
  }
});

var historicalMarkersLayer = L.geoJson(historicalMarkers, {
  onEachFeature: function(feature, layer) {layer.bindPopup("<b>Historical Marker</b><br>" + feature.properties.name + "<br>" + feature.properties.cmt + "<br>" + feature.properties.desc + "<br><a href='" + feature.properties.link1_href + "'>Additional information on HMdb.org</a>")},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: L.AwesomeMarkers.icon({
      icon: 'flag',
      prefix: 'fa',
      markerColor: 'blue'
    })
  });
  }
});

var landmarksLayer = L.geoJson(landmarks, {
  onEachFeature: function(feature, layer) {
  layer.bindPopup(feature.properties.BUILDING_N + "<br>" + feature.properties.FIELD5)},
  style: {color: '#8e44ad',
    fillOpacity: 0.6,
    weight: 0},
});

var artLayer = L.geoJson(art, {
  onEachFeature: function(feature, layer) {
    layer.bindPopup("<a href='" + feature.properties.Website + "' target='_blank'>Title: " + feature.properties.Title + "</a><br>Artist: " + feature.properties.Artist)},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: L.AwesomeMarkers.icon({
      icon: 'paint-brush',
      prefix: 'fa',
      markerColor: 'red'
    })
  });
  }
});

var communityAssetsLayer = L.geoJson(communityAssets, {
  onEachFeature: function(feature, layer) {
    layer.bindPopup("<a href='" + feature.properties.Website + "' target='_blank'>" + feature.properties.Name + "</a><br>" + feature.properties.Category)},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: L.AwesomeMarkers.icon({
      icon: 'group',
      prefix: 'fa',
      markerColor: 'cadetblue'
    })
  });
  }
});

var vacantLayer = L.geoJson(vacant, {
  onEachFeature: function(feature, layer) {
    layer.bindPopup(feature.properties.CommonName + "<br>" + feature.properties.Category + "<br>" + feature.properties.SalePrice)},
  pointToLayer: function(feature, latlng) {
    return L.marker(latlng, {icon: L.AwesomeMarkers.icon({
      icon: 'circle-o',
      prefix: 'fa',
      markerColor: 'darkred'
    })
  });
  }
});

// colors: 'red', 'darkred', 'orange', 'green', 'darkgreen', 'blue', 'purple', 'darkpuple', 'cadetblue'


// map

var map = L.map('map', {
  attributionControl: false,
  center: new L.LatLng(33.75, -84.392), 
  zoom: 15,
  layers: [southDowntownLayer, MARTALayer, historicalMarkersLayer, landmarksLayer, artLayer, communityAssetsLayer, vacantLayer, parcelLayer, governmentBuildingsLayer, residentialLayer, foodLayer, censusBlocksLayer, zoningLayer]
});
L.control.attribution({position: 'bottomleft'}).addTo(map);

L.tileLayer('http://otile4.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
  attribution: 
  'Made at <a href="http://www.codeforamerica.org/events/codeacross-2015/">CodeAcross</a> for <a href="http://www.codeforatlanta.org/"><img src="images/code-for-atlanta.png" height=70></a>' +
  '<br>Tiles &copy; <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png" />',
  maxZoom: 18
}).addTo(map);

var overlayMaps = {
  "<i class='fa fa-cutlery' style='color:#728224'></i> Food <img src='images/foursquare-logomark.png' width='18' valign='bottom'>": foodLayer,
  "<i class='fa fa-home' style='color:#5B396B'></i> Residential Buildings <img src='images/foursquare-logomark.png' width='18' valign='bottom'>": residentialLayer,
  "<span style='color: #f8b50c;'>▌</span>Population Density": censusBlocksLayer,
  "<span style='color: #f07300;'>▌</span>Parcels": parcelLayer,
  "<span style='color: #ff0000;'>▌</span>Zoning": zoningLayer,
  "<span style='color: #00B200;'>▌</span>Tax Allocation Districts": TADLayer,
  "<span style='color: #00ffff;'>▌</span>Neighborhood Stabilization Program": NSPLayer,
  "<span style='color: #0000ff;'>▌</span>City Council Districts": cityCouncilLayer,
  "Neighborhood Profile": neighborhoodProfileLayer,
  "1949 Aerial Survey": historicalMapLayer,
  "<i class='fa fa-circle-o' style='color:#A13336'></i> Available Properties": vacantLayer,
  "<i class='fa fa-group' style='color:#436877'></i> Community Assets": communityAssetsLayer,
  "<i class='fa fa-paint-brush' style='color:#D43E2A'></i> Public Art": artLayer,
  "<i class='fa fa-subway' style='color:#F49630'></i> MARTA Train Stations": MARTALayer,
  "<i class='fa fa-flag' style='color:#38AADD'></i> Historical Markers": historicalMarkersLayer,
  "<span style='color: #8e44ad;'>▌</span>Landmarks": landmarksLayer,
  "<i class='fa fa-university' style='color:#72AF26'></i> Government Buildings <img src='images/foursquare-logomark.png' width='18' valign='bottom'>": governmentBuildingsLayer
};

L.control.layers(null, overlayMaps, {
  collapsed: false
}).addTo(map);

