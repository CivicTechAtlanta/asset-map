var target = document.getElementById('map');
var spinner = new Spinner().spin(target);

// extend L.Map so popups don't close automatically (so they can all be open on load)
L.Map = L.Map.extend({
    openPopup: function(popup) {
        // this.closePopup(); 
        this._popup = popup;
        return this.addLayer(popup).fire('popupopen', {
            popup: this._popup
        });
    }
});

var southDowntownLayer = L.geoJson(southDowntown, {
  onEachFeature: function(feature, layer) {
    layer.bindPopup(feature.properties.name);
  },
  style: {color: '#007df0',
    opacity: 1},
});

// instagram integration

var CLIENT_ID = '426ca0b85f5243a99098fc6ea703d53b';

// var API_ENDPOINT = 'https://api.instagram.com/v1/media/search' +
//   '?client_id=CLIENT_ID' + 
//   '&lat=33.74986&lng=-84.39223' +
//   '&distance=889' +
//   '&callback=?';

var API_ENDPOINT = 'https://api.instagram.com/v1/tags/weloveatl/media/recent' +
  '?client_id=CLIENT_ID';

var instagramLayer = L.layerGroup();

var nextEndpoint = null;

var notInSouthDowntown = [
  "Atlanta, Georgia",
  "Edgewood Ave",
  "Peachtree Center (MARTA station)",
  "Jungle",
  "Atlanta,Ga" // a lot of these seem to actually be downtown
];

// change background color of spinner

function queryInstagram(next_url, geoItems, callback) {

  var nextURL = next_url ? next_url : API_ENDPOINT;
  nextURL += '&callback=?';

  $.getJSON(nextURL
  .replace('CLIENT_ID', CLIENT_ID), function(result, status) {

    if (status !== 'success') return alert('Request to Instagram failed');

    // only add items to map if they are inside the south downtown polygon
    for (var i = 0; i < result.data.length; i++) {

      var item = result.data[i];

      if (item.location) {
        // check if they are from a location not really in south downtown
        if ($.inArray(item.location.name, notInSouthDowntown) >= 0) {
          console.log("excluding: ", item.link);
          break;
        };

        var inPolygon = leafletPip.pointInLayer([item.location.longitude, item.location.latitude], southDowntownLayer);

        if (inPolygon.length) {
          console.log(item);
          geoItems.push(item);
        };
      };

    }

    if (geoItems.length >= 5) {
      callback(geoItems, result.pagination.next_url);
    } else {
      queryInstagram(result.pagination.next_url, geoItems, callback);
    };

  });
}

function getPhotosAndAddToMap(next_url) {
  // start spinner
  spinner.spin(target);
  document.getElementById("refresh").style.display = 'none';

  queryInstagram(next_url, [], function (geoItems, next_url) {

    // add photos to map
    for (var i = 0; i < geoItems.length; i++) {
      var media = geoItems[i];
      var popupContents = '<a href="' + media.link + '" target="_blank"><img src="' + media.images.thumbnail.url + '" width = "' + media.images.thumbnail.width + '"></a>';
      if (media.type === "video") {
        popupContents = '<video width="150" height="150" controls="controls"><source src="' + media.videos.low_bandwidth.url + '" type="video/mp4"></video><br><a href="' + media.link + '" target="_blank">Link</a>';
      }
      var latlng = L.latLng(media.location.latitude, media.location.longitude);
      var marker = L.marker(latlng, {
        icon: L.AwesomeMarkers.icon({
          icon: 'instagram',
          prefix: 'fa',
          markerColor: 'cadetblue'
        })
      })
      .bindPopup(popupContents)
      .addTo(instagramLayer)
      .togglePopup();
    };
    nextEndpoint = next_url;
    // end spinner
    spinner.stop();
    document.getElementById("refresh").style.display = 'block';
    // show button to add more
    // button runs getPhotosAndAddToMap(nextEndpoint)
  });
};

getPhotosAndAddToMap(null);

// colors: 'red', 'darkred', 'orange', 'green', 'darkgreen', 'blue', 'purple', 'darkpuple', 'cadetblue'


// map

var map = L.map('map', {
  attributionControl: false,
  center: new L.LatLng(33.75, -84.392), 
  zoom: 15,
  layers: [instagramLayer, southDowntownLayer]
});
L.control.attribution({position: 'bottomleft'}).addTo(map);

L.tileLayer('http://otile4.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
  attribution: 
  'Made at <a href="http://www.codeforamerica.org/events/codeacross-2015/">CodeAcross</a> for <a href="http://www.codeforatlanta.org/"><img src="images/code-for-atlanta.png" height=70></a>' +
  '<br>Tiles &copy; <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png" />',
  maxZoom: 18
}).addTo(map);

var overlayMaps = {
  "<i class='fa fa-instagram' style='color:#426776'></i> Instagram": instagramLayer
};

L.control.layers(null, overlayMaps, {
  collapsed: false
}).addTo(map);

