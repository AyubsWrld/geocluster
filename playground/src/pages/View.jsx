import { useState, useEffect } from 'react';
import {
  APIProvider,
  Map,
  useMapsLibrary,
  useMap
} from '@vis.gl/react-google-maps';

function RouteMap() {
  const map = useMap();
  const routesLib = useMapsLibrary('routes');
  const [directionsService, setDirectionsService] = useState(null);
  const [directionsRenderer, setDirectionsRenderer] = useState(null);
  const [waypoints, setWaypoints] = useState([]);
  const [center, setCenter] = useState({ lat: 53.5444, lng: -113.4909 }); // Default to Edmonton coordinates
  
  useEffect(() => {
    fetch('../lib/driver_routes.json')
      .then(response => response.json())
      .then(data => {
        setWaypoints(data.driver_3.waypoints);
        // Set the center to the first waypoint if available
        if (data.driver_1.waypoints.length > 0) {
          const firstWaypoint = data.driver_1.waypoints[0].location; // Assuming location is a string
          const geocoder = new routesLib.Geocoder();

          // Geocode the first waypoint to get its coordinates
          geocoder.geocode({ address: firstWaypoint })
            .then(results => {
              if (results && results[0]) {
                setCenter({
                  lat: results[0].geometry.location.lat(),
                  lng: results[0].geometry.location.lng()
                });
              }
            })
            .catch(err => {
              console.error("Geocoding failed:", err);
            });
        }
      })
      .catch(err => {
        console.error("Failed to load routes:", err);
      });
  }, [routesLib]);

  useEffect(() => {
    if (!routesLib || !map || !waypoints.length) return;

    const directionsService = new routesLib.DirectionsService();
    const directionsRenderer = new routesLib.DirectionsRenderer({
      map: map
    });

    setDirectionsService(directionsService);
    setDirectionsRenderer(directionsRenderer);

    // Calculate route with the updated waypoints
    directionsService.route({
      origin: waypoints[0].location , 
      destination: waypoints[waypoints.length -1].location , 
      waypoints,
      travelMode: google.maps.TravelMode.DRIVING,
      optimizeWaypoints: true
    })
    .then(response => {
      directionsRenderer.setDirections(response);
    })
    .catch(err => {
      console.error("Direction service failed:", err);
    });

  }, [routesLib, map, waypoints]);
  // console.log(waypoints[0].location)
  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      <Map
        defaultCenter={center}
        defaultZoom={11}
        gestureHandling={'greedy'}
        disableDefaultUI={false}
        zoomControl={true}
        scrollwheel={true}
        draggable={true}
        keyboardShortcuts={true}
        mapTypeControl={true}
        streetViewControl={true}
        fullscreenControl={true}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}

function View() {
  return (
    <APIProvider apiKey={"AIzaSyAsUGZHvc6xQ64aI8XZ1Q_QKSPlrTwfVsg"} libraries={['routes']}>
      <RouteMap />
    </APIProvider>
  );
}

export default View;
