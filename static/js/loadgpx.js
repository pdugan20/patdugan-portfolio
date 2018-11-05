function GPXParser(xmlDoc, map, map_info) {
    this.xmlDoc = xmlDoc;
    this.map = map;
    this.trackcolour = "#4B2E83";
    this.trackwidth = 5;
    this.mintrackpointdelta = 0.0001
    this.map_info = ''
}

// Set the colour of the track line segements.
GPXParser.prototype.setTrackColour = function(colour) {
    this.trackcolour = colour;
}

// Set the width of the track line segements
GPXParser.prototype.setTrackWidth = function(width) {
    this.trackwidth = width;
}

// Set the infowindow of the track line segements
GPXParser.prototype.setTrackInfo = function(map_info) {
    this.map_info = map_info;
}

// Set the minimum distance between trackpoints.
// Used to cull unneeded trackpoints from map.
GPXParser.prototype.setMinTrackPointDelta = function(delta) {
    this.mintrackpointdelta = delta;
}

GPXParser.prototype.translateName = function(name) {
    if(name == "wpt") {
        return "Waypoint";
    }
    else if(name == "trkpt") {
        return "Track Point";
    }
    else if(name == "rtept") {
        return "Route Point";
    }
}

GPXParser.prototype.createMarker = function(point) {
    var lon = parseFloat(point.getAttribute("lon"));
    var lat = parseFloat(point.getAttribute("lat"));
    var html = "";

    var pointElements = point.getElementsByTagName("html");
    if(pointElements.length > 0) {
        for(i = 0; i < pointElements.item(0).childNodes.length; i++) {
            html += pointElements.item(0).childNodes[i].nodeValue;
        }
    }
    else {
        // Create the html if it does not exist in the point.
        html = "<b>" + this.translateName(point.nodeName) + "</b><br>";
        var attributes = point.attributes;
        var attrlen = attributes.length;
        for(i = 0; i < attrlen; i++) {
            html += attributes.item(i).name + " = " +
                    attributes.item(i).nodeValue + "<br>";
        }

        if(point.hasChildNodes) {
            var children = point.childNodes;
            var childrenlen = children.length;
            for(i = 0; i < childrenlen; i++) {
                // Ignore empty nodes
                if(children[i].nodeType != 1) continue;
                if(children[i].firstChild == null) continue;
                html += children[i].nodeName + " = " +
                        children[i].firstChild.nodeValue + "<br>";
            }
        }
    }

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat,lon),
        map: this.map
    });

    var infowindow = new google.maps.InfoWindow({
        content: html,
        size: new google.maps.Size(50,50)
    });

    google.maps.event.addListener(marker, "click", function() {
        infowindow.open(this.map, marker);
    });
}

GPXParser.prototype.addTrackSegmentToMap = function(trackSegment, colour,
        width, map_info) {
    var trackpoints = trackSegment.getElementsByTagName("trkpt");
    if(trackpoints.length == 0) {
        return;
    }

    var pointarray = [];

    // process first point
    var lastlon = parseFloat(trackpoints[0].getAttribute("lon"));
    var lastlat = parseFloat(trackpoints[0].getAttribute("lat"));
    var latlng = new google.maps.LatLng(lastlat,lastlon);
    pointarray.push(latlng);

    for(var i = 1; i < trackpoints.length; i++) {
        var lon = parseFloat(trackpoints[i].getAttribute("lon"));
        var lat = parseFloat(trackpoints[i].getAttribute("lat"));

        // Verify that this is far enough away from the last point to be used.
        var latdiff = lat - lastlat;
        var londiff = lon - lastlon;
        if(Math.sqrt(latdiff*latdiff + londiff*londiff)
                > this.mintrackpointdelta) {
            lastlon = lon;
            lastlat = lat;
            latlng = new google.maps.LatLng(lat,lon);
            pointarray.push(latlng);
        }

    }

    var polyline = new google.maps.Polyline({
        path: pointarray,
        strokeColor: colour,
        strokeWeight: width,
        map: this.map
    });

    var infowindow = new google.maps.InfoWindow();

    google.maps.event.addListener(polyline, 'click', function(event) {
        infowindow.setContent(map_info);
        infowindow.setPosition(event.latLng);
        infowindow.open(this.map);
    });

}

GPXParser.prototype.addTrackToMap = function(track, colour, width, map_info) {
    var segments = track.getElementsByTagName("trkseg");
    for(var i = 0; i < segments.length; i++) {
        var segmentlatlngbounds = this.addTrackSegmentToMap(segments[i], colour,
                width, map_info);
    }
}

GPXParser.prototype.addRouteToMap = function(route, colour, width) {
    var routepoints = route.getElementsByTagName("rtept");
    if(routepoints.length == 0) {
        return;
    }

    var pointarray = [];

    // process first point
    var lastlon = parseFloat(routepoints[0].getAttribute("lon"));
    var lastlat = parseFloat(routepoints[0].getAttribute("lat"));
    var latlng = new google.maps.LatLng(lastlat,lastlon);
    pointarray.push(latlng);

    for(var i = 1; i < routepoints.length; i++) {
        var lon = parseFloat(routepoints[i].getAttribute("lon"));
        var lat = parseFloat(routepoints[i].getAttribute("lat"));

        // Verify that this is far enough away from the last point to be used.
        var latdiff = lat - lastlat;
        var londiff = lon - lastlon;
        if(Math.sqrt(latdiff*latdiff + londiff*londiff)
                > this.mintrackpointdelta) {
            lastlon = lon;
            lastlat = lat;
            latlng = new google.maps.LatLng(lat,lon);
            pointarray.push(latlng);
        }

    }

    var polyline = new google.maps.Polyline({
        path: pointarray,
        strokeColor: colour,
        strokeWeight: width,
        map: this.map
    });
}

GPXParser.prototype.centerAndZoom = function(trackSegment) {

    var pointlist = new Array("trkpt", "rtept", "wpt");
    var minlat = 0;
    var maxlat = 0;
    var minlon = 0;
    var maxlon = 0;

    for(var pointtype = 0; pointtype < pointlist.length; pointtype++) {

        // Center the map and zoom on the given segment.
        var trackpoints = trackSegment.getElementsByTagName(
                pointlist[pointtype]);

        // If the min and max are uninitialized then initialize them.
        if((trackpoints.length > 0) && (minlat == maxlat) && (minlat == 0)) {
            minlat = parseFloat(trackpoints[0].getAttribute("lat"));
            maxlat = parseFloat(trackpoints[0].getAttribute("lat"));
            minlon = parseFloat(trackpoints[0].getAttribute("lon"));
            maxlon = parseFloat(trackpoints[0].getAttribute("lon"));
        }

        for(var i = 0; i < trackpoints.length; i++) {
            var lon = parseFloat(trackpoints[i].getAttribute("lon"));
            var lat = parseFloat(trackpoints[i].getAttribute("lat"));

            if(lon < minlon) minlon = lon;
            if(lon > maxlon) maxlon = lon;
            if(lat < minlat) minlat = lat;
            if(lat > maxlat) maxlat = lat;
        }
    }

    if((minlat == maxlat) && (minlat == 0)) {
        this.map.setCenter(new google.maps.LatLng(49.327667, -122.942333), 14);
        return;
    }

    // Center around the middle of the points
    var centerlon = (maxlon + minlon) / 2;
    var centerlat = (maxlat + minlat) / 2;

    var bounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(minlat, minlon),
            new google.maps.LatLng(maxlat, maxlon));
    this.map.setCenter(new google.maps.LatLng(centerlat, centerlon));
    this.map.fitBounds(bounds);
}

GPXParser.prototype.centerAndZoomToLatLngBounds = function(latlngboundsarray) {
    var boundingbox = new google.maps.LatLngBounds();
    for(var i = 0; i < latlngboundsarray.length; i++) {
        if(!latlngboundsarray[i].isEmpty()) {
            boundingbox.extend(latlngboundsarray[i].getSouthWest());
            boundingbox.extend(latlngboundsarray[i].getNorthEast());
        }
    }

    var centerlat = (boundingbox.getNorthEast().lat() +
            boundingbox.getSouthWest().lat()) / 2;
    var centerlng = (boundingbox.getNorthEast().lng() +
            boundingbox.getSouthWest().lng()) / 2;
    this.map.setCenter(new google.maps.LatLng(centerlat, centerlng),
            this.map.getBoundsZoomLevel(boundingbox));
}

GPXParser.prototype.addTrackpointsToMap = function() {
    var tracks = this.xmlDoc.documentElement.getElementsByTagName("trk");
    for(var i = 0; i < tracks.length; i++) {
        this.addTrackToMap(tracks[i], this.trackcolour, this.trackwidth, this.map_info);
    }
}

GPXParser.prototype.addWaypointsToMap = function() {
    var waypoints = this.xmlDoc.documentElement.getElementsByTagName("wpt");
    for(var i = 0; i < waypoints.length; i++) {
        this.createMarker(waypoints[i]);
    }
}

GPXParser.prototype.addRoutepointsToMap = function() {
    var routes = this.xmlDoc.documentElement.getElementsByTagName("rte");
    for(var i = 0; i < routes.length; i++) {
        this.addRouteToMap(routes[i], this.trackcolour, this.trackwidth);
    }
}
