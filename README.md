
# 3-EleNa (3-D Visualizable Elevation-based Navigation System)

## User

### Motivation

Navigation systems that are popular today are constrained to one type of optimization: distance. However, it is often the case that a person, say a jogger or a bicyclist, would rather optimize given elevation change rather than pure distance. EleNa is an elevation based navigation system that one can use to map and visualize routes with *different* optimizations in mind, on a 3-D terrain.

## Developer

### Architecture

#### Stack

3-EleNa is segmented into 3 layers of the stack. A database, backend, and frontend. The **database** is responsible for holding the stored network graph for the region in question (Amherst, MA). For simplicity and alacrity, our database is modeled as a Python pickle file (network graph is stored in binary, and is retrieved and parsed by the backend). The **backend** is responsible for receiving queries from the frontend, running the algorithm on the network graph given the frontend query, and responding with the desired route. 3-EleNa's backend is written in Flask, a Python micro framework for web development. The **frontend** is responsible for receiving input from the user (start and end points, choose an algorithm), sending it to the backend for computation, and receiving the path and visualizing it. The frontend is written in React.

#### File structure

```
├── EleNa
├── controller              # Controller (Python, Flask)
    ├── server.py           # Server file
└── model                   # Model (Python, Pickle)
    ├── model.py            # Model file
    ├── graph.pkl           # Pickled graph (binary)
    ├── graph_projected.pkl # Pickled graph (projected, binary)
└── view                    # View (React.js, follows conventional React structure)
    ├── build               # Production build file
    └── src
    |   └── Components	    # Source code
        |   └── ...
    |   ├── index.jsx.      # Root file
    └── public				# Public folder (assets, index.html)
        └── ...
    ├── graph_projected.pkl # Pickled graph (projected, binary)
```

### API Routes

#### <code>POST /compute_shortest_path</code>

##### Request
| parameter | type | description |
| - | - | - |
| <p align="center">start</p> | <p align="center">object</p> | <pre align="left">&nbsp;{<br>&nbsp;&nbsp;&nbsp;latitude: float,<br>&nbsp;&nbsp;&nbsp;longitude: float<br>&nbsp;}</pre> |
| <p align="center">end</p> | <p align="center">object</p> | <pre align="left">&nbsp;{<br>&nbsp;&nbsp;&nbsp;latitude: float,<br>&nbsp;&nbsp;&nbsp;longitude: float<br>&nbsp;}</pre> |
| <p align="center">alg</p> | <p align="center">String</p> | <p align="center">Specified algorithm, one of `max_elev`, `min_elev`, `max_elev_dist`, `default`. If `default` or omitted, all algorithms are selected.</p> |

##### Response

| parameter | type | description |
| - | - | - |
| <p align="center">paths</p> | <p align="center">list</p> | <p align="center">For each algorithm, returns a list of [latitude, longitude] points along the path.</p> |


