import React, { useEffect, useRef } from 'react';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: icon,
  shadowUrl: iconShadow
});

const MapComponent = ({ latitude, longitude }) => {
  const mapRef = useRef(null);

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map('map').setView([latitude, longitude], 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(mapRef.current);
    } else {
      mapRef.current.setView([latitude, longitude]);
    }

    // Clear previous marker and add new one
    if (mapRef.current && mapRef.current.marker) {
      mapRef.current.removeLayer(mapRef.current.marker);
    }
    mapRef.current.marker = L.marker([latitude, longitude]).addTo(mapRef.current);

  }, [latitude, longitude]);

  return <div id="map" style={{ height: '400px' }} />;
};

export default MapComponent;
