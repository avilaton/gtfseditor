var transit = transit || {};

transit.geolocation = (function () {
    var watchId;
    if (typeof(navigator.geolocation)==='object') {
        watchId = navigator.geolocation.watchPosition(
            transit.maps.showUserLocation,
            function (positionError) {
                console.log(positionError);
            },
            {enableHighAccuracy:true, maximumAge:30000, timeout:27000}
        );
    };
})();
