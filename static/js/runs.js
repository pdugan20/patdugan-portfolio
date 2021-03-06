function loadGPXFileIntoGoogleMap(map, filename, map_info) {
    $.ajax({url: filename,
        dataType: "xml",
        success: function(data) {
          var parser = new GPXParser(data, map);
          parser.setTrackColour("#4B2E83");
          parser.setTrackWidth(5);
          parser.setTrackInfo(map_info);
          parser.setMinTrackPointDelta(0.001);
          // parser.centerAndZoom(data);
          parser.addTrackpointsToMap();
          parser.addRoutepointsToMap();
          parser.addWaypointsToMap();
        }
    });
}

var map;
function initMap() {
    if($("#map1").length != 0) {
        map1 = new google.maps.Map(document.getElementById('map1'), {
            center: new google.maps.LatLng(38.093231, -122.577528),
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
            disableDefaultUI: true,
            zoomControl: true,
        });
        loadGPXFileIntoGoogleMap(map1, "https://www.patdugan.me/runs/ragnar_01.gpx", "Ragnar Leg 9 - 6.01 miles through Novato, CA");
    }

    if($("#map2").length != 0) {
        map2 = new google.maps.Map(document.getElementById('map2'), {
            center: new google.maps.LatLng(38.487234, -122.775706),
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
            disableDefaultUI: true,
            zoomControl: true,
        });
        loadGPXFileIntoGoogleMap(map2, "https://www.patdugan.me/runs/ragnar_02.gpx", "Ragnar Leg 22 - 5.33 miles through Fulton, CA");
    }

    if($("#map3").length != 0) {
        map3 = new google.maps.Map(document.getElementById('map3'), {
            center: new google.maps.LatLng(38.295826, -122.477501),
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
            disableDefaultUI: true,
            zoomControl: true,
        });
        loadGPXFileIntoGoogleMap(map3, "https://www.patdugan.me/runs/ragnar_03.gpx", "Ragnar Leg 33 - 4.12 miles through Sonoma, CA");
    }

    if($("#map4").length != 0) {
        map4 = new google.maps.Map(document.getElementById('map4'), {
            center: new google.maps.LatLng(37.811838, -122.3032713),
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
            disableDefaultUI: true,
            zoomControl: true,
        });
        loadGPXFileIntoGoogleMap(map4, "https://www.patdugan.me/runs/oakland_marathon_01.gpx", "Oakland Marathon - 26.22 miles through Oakland, CA");
    }

    if($("#map5").length != 0) {
        map5 = new google.maps.Map(document.getElementById('map5'), {
            center: new google.maps.LatLng(37.837112, -122.506691),
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.TERRAIN,
            disableDefaultUI: true,
            zoomControl: true,
        });
        loadGPXFileIntoGoogleMap(map5, "https://www.patdugan.me/runs/north_face_endurance_01.gpx", "North Face Endurance Marathon - 26.29 miles through the Marin Headlands");
    }
}
