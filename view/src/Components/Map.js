import { Map } from '@esri/react-arcgis';

import './Map.css';

const MapVis = () => {
  return <Map
        class="full-screen-map"
        mapProperties={{ basemap: 'satellite' }}
    />
}

export default MapVis;
