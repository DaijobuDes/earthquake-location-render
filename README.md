# earthquake-location-render
Rendering OSM with leaflet to image by providing lat, long and mag URL parameters. Used for my discord bot. Source to data: https://earthquake.phivolcs.dost.gov.ph/

## Running
```
# Run containers
docker compose up -d --build

# Kill containers
docker compose down
```

The flask app can be accessed on `http://localhost:5000`

### Endpoints

| Endpoint | Parameters | Description |
| :-- | :-- | :-- |
| `/` | None | Renders a sample HTML page |
| `/capture` | `mag`, `lat`, `long`, `zoom` (optional) | Renders the map with the specific latitude, longitude with a circle depending on the `mag` parameter |
| `/render` | `mag`, `lat`, `long`, `zoom` (optional) | Passes parameters to `/capture` to be rendered to an image and are saved inside `img` folder |
