var directions = new google.maps.DirectionsService();
var renderer = new google.maps.DirectionsRenderer({
  // suppressInfoWindows: true
});
var map, transitLayer;

function initialize() {
  var mapOptions = {
    zoom: 11,
    center: new google.maps.LatLng(-32.8897185,-68.8467144),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  map = new google.maps.Map(document.getElementById('map'), mapOptions);

  google.maps.event.addDomListener(document.getElementById('goBtn'), 'click',
    route);

  var inputFrom = document.getElementById('from');
  var autocompleteFrom = new google.maps.places.Autocomplete(inputFrom);
  autocompleteFrom.bindTo('bounds', map);

  var inputTo = document.getElementById('to');
  var autocompleteTo = new google.maps.places.Autocomplete(inputTo);
  autocompleteTo.bindTo('bounds', map);

  addDepart();
}

function addDepart() {
  var depart = document.getElementById('depart');
  for (var i = 0; i < 24; i++) {
    for (var j = 0; j < 60; j += 15) {
      var x = i < 10 ? '0' + i : i;
      var y = j < 10 ? '0' + j : j;
      depart.innerHTML += '<option>' + x + ':' + y + '</option>';
    }
  }
}

function route() {
  var departure = document.getElementById('depart').value;
  var bits = departure.split(':');
  var now = new Date();
  var tzOffset = (now.getTimezoneOffset() + 60) * 60 * 1000;
  var customInfoWindow = new google.maps.InfoWindow({
    maxWidth: 500,
    content: "test"
  });

  var time = new Date();
  time.setHours(bits[0]);
  time.setMinutes(bits[1]);

  var ms = time.getTime() - tzOffset;
  if (ms < now.getTime()) {
    ms += 24 * 60 * 60 * 1000;
  }

  var departureTime = new Date(ms);

  var request = {
    origin: document.getElementById('from').value,
    destination: document.getElementById('to').value,
    travelMode: google.maps.DirectionsTravelMode.TRANSIT,
    provideRouteAlternatives: true,
    transitOptions: {
      departureTime: departureTime
    }
  };

  var panel = document.getElementById('panel');
  panel.innerHTML = '';
  directions.route(request, function(response, status) {
    console.log(status, response)
    if (status == google.maps.DirectionsStatus.OK) {
      renderer.setDirections(response);
      renderer.setMap(map);
      renderer.setPanel(panel);
    } else {
      renderer.setMap(null);
      renderer.setPanel(null);
      panel.innerHTML = '<div><p>No se encontraron resultados</p></div>'
    }
  });

}

google.maps.event.addDomListener(window, 'load', initialize);