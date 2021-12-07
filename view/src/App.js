import { useEffect, useState, useRef } from 'react';
import axios from 'axios';

import logo from './logo.svg';
import './App.css';
import MapVis from './Components/Map.js';

import { loadModules , loadCss} from 'esri-loader';

function App() {
  const [points, setPoints] = useState([]);
  const [drawRoutes, setDrawRoutes] = useState(undefined);
  const form = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/compute_shortest_path', {
      start: {
        "latitude": points[0][0],
        "longitude": points[0][1]
      },
      end: {
        "latitude": points[1][0],
        "longitude": points[1][1]
      }
    }).then(res => {
      for(let i = 0; i < res.data.length; i++){
        drawRoutes(res.data[i], [points[0][0], points[0][1]], [points[1][0], points[1][1]], i);
      }
    });
  }


  useEffect( () => {
    if(!form){
      return;
    }
    loadCss("4.21");

    // configure esri-loader to use version 3.38
    // and the CSS for that version from the ArcGIS CDN
    const options = { version: '4.21', css: true };

    loadModules([
      "esri/config",
      "esri/Map",
      "esri/layers/FeatureLayer",
      "esri/layers/GraphicsLayer",
      "esri/views/SceneView",
      "esri/WebScene",
      "esri/layers/ElevationLayer",
      "esri/widgets/Sketch/SketchViewModel",
      "esri/Graphic",
      "esri/geometry/Polyline",
      "esri/layers/BaseElevationLayer",
      "esri/layers/support/LabelClass",
      "esri/Basemap",
      "esri/geometry/Point",
      "esri/layers/TileLayer",
      "esri/widgets/Search",
      "esri/rest/locator",
      "esri/widgets/Search/LayerSearchSource"], options)
      .then(([esriConfig, Map, FeatureLayer, GraphicsLayer, SceneView, WebScene, ElevationLayer, SketchViewModel, Graphic, Polyline, BaseElevationLayer, LabelClass, Basemap, Point, TileLayer, Search, locator, LayerSearchSource]) => {
        esriConfig.apiKey = 'AAPK4e870b84de1741d3933f19c0e4a079c62hgfr2QWI1X2cyUmJgaMTrOUp2cY79xTNnPZjdlltlZBfdAJnTXjRSZgqVeG6dq7';
        const places = [
          {
            "id": 1,
            "address": "650 N Pleasant St, Amherst, MA 01003",
            "longitude": -72.52587088060791,
            "latitude": 42.390934188741205,
            "label": "Integrative Learning Center"
          }
        ];
        const graphics = places.map(function (place) {
          return new Graphic({
            attributes: {
              ObjectId: place.id,
              address: place.address,
              label: place.label
            },
            geometry: new Point({
              longitude: place.longitude,
              latitude: place.latitude
            }),
            symbol: {
              type: "simple-marker",             // autocasts as new SimpleMarkerSymbol()
              color: [ 226, 119, 40 ],
              outline: {                         // autocasts as SimpleLineSymbol()
                color: [ 255, 255, 255 ],
                width: 2
              }
            },
            popupTemplate: {                     // autocasts as new PopupTemplate()
              title: "Places in Los Angeles",
              content: [{
                type: "fields",
                fieldInfos: [
                  {
                    fieldName: "label",
                    label: "Name",
                    visible: true
                  },
                  {
                    fieldName: "address",
                    label: "Address",
                    visible: true
                  }
                ]
              }]
            }
          });
        });
        const labelFeatureLayer = new FeatureLayer({
          source: graphics,
          renderer: {
            type: "simple",                    // autocasts as new SimpleRenderer()
            symbol: {                          // autocasts as new SimpleMarkerSymbol()
              type: "simple-marker",
              color: "#102A44",
              outline: {                       // autocasts as new SimpleLineSymbol()
                color: "#598DD8",
                width: 2
              }
            }
          },
          popupTemplate: {                     // autocasts as new PopupTemplate()
            title: "Places in Los Angeles",
            content: [{
              type: "fields",
              fieldInfos: [
                {
                  fieldName: "address",
                  label: "Address",
                  visible: true
                },
                {
                  fieldName: "label",
                  label: "Label",
                  visible: true
                }
              ]
            }]
          },
          objectIdField: "ObjectID",           // This must be defined when creating a layer from `Graphic` objects
          fields: [
            {
              name: "ObjectID",
              alias: "ObjectID",
              type: "oid"
            },
            {
              name: "address",
              alias: "address",
              type: "string"
            },
            {
              name: "label",
              alias: "label",
              type: "string"
            }
          ]
        });
        const sym = { // symbol used for polylines
          type: "simple-line", // autocasts as new SimpleMarkerSymbol()
          color: "#8A2BE2",
          width: "4",
          style: "dash"
        }
        const grL = new GraphicsLayer();

        /* EXAGGERATION LAYER */
        // this function takes the existing terrain and exaggerates the features
        const ExaggeratedElevationLayer = BaseElevationLayer.createSubclass({
          properties: {
            exaggeration: null
          },
          // The load() method is called when the layer is added to the map
          // prior to it being rendered in the view.
          load: function () {
            this._elevation = new ElevationLayer({
              url: "https://elevation3d.arcgis.com/arcgis/rest/services/WorldElevation3D/TopoBathy3D/ImageServer"
            });
            // wait for the elevation layer to load before resolving load()
            this.addResolvingPromise(this._elevation.load());
          },
          // Fetches the tile(s) visible in the view
          fetchTile: function (level, row, col, options) {
            // calls fetchTile() on the elevationlayer for the tiles
            // visible in the view
            return this._elevation.fetchTile(level, row, col, options).then(
              function (data) {
                var exaggeration = this.exaggeration;
                // `data` is an object that contains the
                // the width and the height of the tile in pixels,
                // and the values of each pixel
                for (var i = 0; i < data.values.length; i++) {
                  // Multiply the given pixel value
                  // by the exaggeration value
                  data.values[i] = data.values[i] * exaggeration;
                }
                return data;
              }.bind(this)
            );
          }
        });

        // define exaggeration

        const elevationLayer = new ExaggeratedElevationLayer({ exaggeration: 8 });

        //load base map
        const basemap = new Basemap({
          baseLayers: [
            new TileLayer({
              url: "https://wtb.maptiles.arcgis.com/arcgis/rest/services/World_Topo_Base/MapServer"
            })
          ]
        });

        //initialize elevation layer for terrain

        const map = new Map({
          ground: {
            layers: [ new ElevationLayer({
              url: "https://elevation3d.arcgis.com/arcgis/rest/services/WorldElevation3D/Terrain3D/ImageServer"
            }), elevationLayer]
          },
          basemap: basemap,
          showLabels: true
        });

        //Initialize view, camera

        const view = new SceneView({
          container: "viewDiv",
          map: map,
          qualityProfile: "high",
          camera: {
            position: [
              -72.525387,
              42.364154,
              1000
            ],
            heading: 0.51,
            tilt: 75
          }
        });

        const searchStart = new Search({
          view: view

        })
        const searchEnd = new Search({
          view: view
        })

        const serviceUrl = "http://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer";

        view.ui.add(searchStart, "top-right");
        view.ui.add(searchEnd, "top-right");

        /*

        Search functionality
        Gets latitude and longitude from results, extract gemoetry object, update corresponding point

        */

        searchStart.on('search-complete', function(result){
          if(result.results && result.results.length > 0 && result.results[0].results && result.results[0].results.length > 0){
            var geom = result.results[0].results[0].feature.geometry;
            let latitude = geom.latitude;
            let longitude = geom.longitude;
            setPoints(prev => {
              view.graphics.removeAll();
              grL.graphics.removeAll();
              return [[latitude, longitude]];
            });

            let geo = new Graphic(
              {
                geometry: new Point({
                  longitude: longitude,
                  latitude: latitude
                }),
                symbol: {
                  type: "simple-marker",             // autocasts as new SimpleMarkerSymbol()
                  color: [ 226, 119, 40 ],
                  outline: {                         // autocasts as SimpleLineSymbol()
                    color: [ 255, 255, 255 ],
                    width: 2
                  }
                }
              });
              view.graphics.add(geo);
            }
          });

          searchEnd.on('search-complete', function(result){
            if(result.results && result.results.length > 0 && result.results[0].results && result.results[0].results.length > 0){
              var geom = result.results[0].results[0].feature.geometry;

              let latitude = geom.latitude;
              let longitude = geom.longitude;
              setPoints(prev => {
                if(prev.length === 1){
                  return [...prev, [latitude, longitude]];
                }else{
                  view.graphics.removeAll();
                  grL.graphics.removeAll();
                  return [[], [latitude, longitude]];
                }
              });
              let geo = new Graphic(
                {
                  geometry: new Point({
                    longitude: longitude,
                    latitude: latitude
                  }),
                  symbol: {
                    type: "simple-marker",             // autocasts as new SimpleMarkerSymbol()
                    color: [ 226, 119, 40 ],
                    outline: {                         // autocasts as SimpleLineSymbol()
                      color: [ 255, 255, 255 ],
                      width: 2
                    }
                  }
                });
                view.graphics.add(geo);

              }
          });
          view.ui.add(searchStart, "top-right");
          view.ui.add(searchEnd, "top-right");


          /*

            Draw route implementation:
              Once user has selects points, bind form onsubmit, send request thru axios to backend
              Backend sends paths back, passed into below route.

          */

          const routeDrawer = (routes, start_point, end_point, ind) => {
            const symb = [{
              type: "simple-line",
              color: [234, 181, 67, 0.65], // Orange
              width: 4
            },
            {
              type: "simple-line",
              color: [88, 177, 159, 0.65], // Orange
              width: 4
            }, {
              type: "simple-line",
              color: [130, 88, 159, 0.65], // Orange
              width: 4
            }, {
              type: "simple-line",
              color: [24, 44, 97,0.65], // Orange
              width: 4
            }][ind];
            map.add(grL);
            let pths = [];
            routes = [[start_point[1], start_point[0]], ...routes, [end_point[1], end_point[0]]];
            for(let i = 0; i < routes.length; i++){
              pths.push(routes[i]);
            }
            const polyline = {
              type: "polyline",
              paths: pths
            }
            const polylineGraphic = new Graphic({
              geometry: polyline,
              symbol: symb
            });
            grL.add(polylineGraphic);

          }

          setDrawRoutes(()=>routeDrawer); //Expose draw routes since senstivie classes are defined within a useEffect

          const trails = new FeatureLayer({
            url: "https://services3.arcgis.com/GVgbJbqm8hXASVYi/arcgis/rest/services/Trails/FeatureServer/0",
            elevationInfo: {
              mode: "relative-to-ground",
              offset: 3
            },
            renderer: {
              type: "simple",
              symbol: {
                type: "line-3d",
                symbolLayers: [{
                  type: "line",
                  material: { color: "#FF5500" },
                  size: "2px"
                }]
              }
            }
          });

          const trailHeads = new FeatureLayer({
            url: "https://services3.arcgis.com/GVgbJbqm8hXASVYi/arcgis/rest/services/Trailheads/FeatureServer/0",
            elevationInfo: {
              mode: "relative-to-ground"
            },
            renderer: {
              type: "simple",
              symbol: {
                type: "point-3d",
                symbolLayers: [{
                  type: "icon",
                  resource: { primitive: "circle"},
                  material: { color: "#FF5500" },
                  outline: { color: "#FFFFFF", size: 1 },
                  size: "10px"
                }],
                verticalOffset: {
                  screenLength: 20,
                  maxWorldLength: 200,
                  minWorldLength: 20
                },
                callout: {
                  type: "line",
                  size: 1,
                  color: "#FFFFFF"
                }
              }
            },
            setlabelingInfo: [
              new LabelClass({
                labelExpressionInfo: { expression: "$feature.TRL_NAME"},
                symbol: {
                  type: "label-3d",
                  symbolLayers: [{
                    type: "text",
                    material: {
                      color: "#FFFFFF"
                    },
                    halo: {
                      size:  1,
                      color: [0, 0, 0, 0.5]
                    },
                    font: {
                      size:  11,
                      family: "sans-serif"
                    }
                  }]
                }
              })
            ]
          });

          let currGraphic;
          let currGeometry;

          function showAddress(address, pt) {
            view.popup.open({
              title:  address,
              // content: address,
              location: pt
            });
          }

          //bind user events
          view.on('click', e => {
            const params = {
              location: e.mapPoint
            };
            console.log(e.mapPoint);
            locator.locationToAddress(serviceUrl, params)
            .then(function(response) { // Show the address found
              const address = response.address;
              showAddress(address, e.mapPoint);
            }, function(err) { // Show no address found
              showAddress("No address found.", e.mapPoint);
            });

            let { latitude, longitude } = e.mapPoint;

            let geo = new Graphic(
              {
                geometry: new Point({
                  longitude: longitude,
                  latitude: latitude
                }),
                symbol: {
                  type: "simple-marker",             // autocasts as new SimpleMarkerSymbol()
                  color: [ 226, 119, 40 ],
                  outline: {                         // autocasts as SimpleLineSymbol()
                    color: [ 255, 255, 255 ],
                    width: 2
                  }
                }
              });
              setPoints(prev => {
                if(prev.length < 2){
                  return [...prev, [latitude, longitude]];
                }else{
                  view.graphics.removeAll();
                  // debugger;
                  grL.graphics.removeAll()
                  return [[latitude, longitude]];
                }
              });

              view.graphics.add(geo);

            });

            map.addMany([trails, trailHeads]);
          })
          .catch(err => {
            // handle any script or module loading errors
            console.error(err);
          });
        }, [form]);
        return (
          <>
          <div id="viewDiv">
          </div>
          <div id="overlay">
          <form ref={form} onSubmit={handleSubmit}>
          <div id="label">{`Pick the ${points.length === 0 ? "start" : points.length === 1 ? "end" : "ready"} point (Ctrl-click)`}</div>
          <button type="submit" className={`btn-submit ${points.length !== 2 ? "disabled" : ""}`}>
          Route!
          </button>
          <div id="start">
          <div className="label">
          Start
          </div>
          <div>{`Latitude: ${points[0] ? points[0][0] : "..."}, Longitude: ${points[0] ? points[0][1] : "..."}`}</div>
          </div>
          <div id="end">
          <div className="label">
          End
          </div>
          <div>{`Latitude: ${points[1] ? points[1][0] : "..."}, Longitude: ${points[1] ? points[1][1] : "..."}`}</div>
          </div>
          </form>
          </div>
          </>
        );
      }


      export default App;
