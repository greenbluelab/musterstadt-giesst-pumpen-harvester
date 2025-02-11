![](https://img.shields.io/badge/Built%20with%20%E2%9D%A4%EF%B8%8F-at%20Technologiestiftung%20Berlin-blue)

# Musterstadt Gießt – Fountain aggregation from OSM

This is a Docker based GitHub Action to aggregate pumps data from OpenStreetMap and to store them in a geojson file. It is defined in [./action.yml](./action.yml)

The aggregated data is used to provide locations and information about the public fontains in the frontend of [Musterstadt Gießt](https://github.com/greenbluelab/musterstadt-giesst) and uses Dresden as an example city.
The [Overpass API](http://overpass-api.de) for OSM is used to retrieve the data, by fetching all nodes with tag `"amenity=fountain"` in the search area of `"name=Dresden"`.

The corresponding query is defined in the script [fetch.py](/fetch.py). It can be overriden by providing a custom overpass query statement.

The data obtained in this way is further processed and the raw OSM data is filtered. In _utils.py_, all attributes are dropped that are theoretically still available in the OSM data, but which we do not need. By adding the respective attributes to the filter list, they can be included in the final data set.

## Inputs to the Github Action

### `outfile-path`

**Required** The path where the GeoJSON file should be written to. Default `"public/data/pumps.geojson"`.

### `query`

A custom overpass query statement to retrieve pumps from OpenStreetMap. When omitted, the action will retrieve Berlin pumps.

## Outputs from the Github Action

### `file`

The path to where the file was written.

## Example Usage
The Github Action defined in this repository is built to be reusable. What you do with the generated `pumps.geojson` file is up to you and depends on your specific use case.

### Usage for giessdenkiez-de repository
For [musterstadt-giesst](https://github.com/greenbluelab/musterstadt-giesst), the custom Github Action defined here in [./action.yml](./action.yml) gets used in a periodically triggered Github Action, 
which is defined in [musterstadt-giesst -> pumps.yml](https://github.com/greenbluelab/musterstadt-giesst/blob/master/.github/workflows/pumps.yml).
For this specific use case, the generated `pumps.geojson` file is subsequently uploaded to a [Supabase](https://supabase.com/) storage location. For details, refer to the Github Actions definition in [musterstadt-giesst -> pumps.yml](https://github.com/greenbluelab/musterstadt-giesst/blob/master/.github/workflows/pumps.yml). 

### Your own public repository
Reference the Github Action defined in this repository in your own Github Actions file. Use the generated `pumps.geojson` in a way that fits your architecture.

File: `.github/workflows/pumps.yml`

```yml
on:
  workflow_dispatch:
  schedule:
    # every sunday morning at 4:00
    - cron: "0 4 * * 0"

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to aggregate pumps data from open street maps
    steps:
      - name: Pumps data generate step
        # use tags if you want to fix on a specific version
        # e.g
        # uses: technologiestiftung/giessdenkiez-de-osm-pumpen-harvester@1.2.0
        # use master if you like to gamble
        uses: greenbluelab/musterstadt-giesst-pumpen-harvester@master
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
          # Pass "query" argument to specify custom overpass query string (see example below for the city of Magdeburg)
          # query: '[out:json][bbox:52.0124,11.4100, 52.2497,11.8330];(node["man_made"="water_well"];);out;>;out;'
      # Use the output from the `pumps` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
```

### Your own private repository
You can use the code from this public repository in your own private repository in your own Github Actions file. Use the generated `pumps.geojson` in a way that fits your architecture.

File: `.github/workflows/main.yml`

```yml
on:
  workflow_dispatch:
  schedule:
    # * is a special character in YAML so you have to quote this string
    - cron: "0 4 * * 0"

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to aggregate pumps data from open street maps
    steps:
      # To use this repository's private action,
      # you must check out the repository
      - name: Checkout
        uses: actions/checkout@v2
      - name: Pumps data generate step
        uses: ./ # Uses an action in the root directory
        id: pumps
        with:
          outfile-path: "out/pumps.geojson"
          # Pass "query" argument to specify custom overpass query string (see example below for the city of Magdeburg)
          # query: '[out:json][bbox:52.0124,11.4100, 52.2497,11.8330];(node["man_made"="water_well"];);out;>;out;'
      # Use the output from the `hello` step
      - name: File output
        run: echo "The file was written to ${{ steps.pumps.outputs.file }}"
```

## Development

See also https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action

### Python

Run the script with `python3 harvester/main.py out/pumps.geojson`

### Docker

Build the container and run it.

```bash
mkdir out
docker build --tag greenbluelab/musterstadt-giesst-pumpen-harvester .
docker run -v $PWD/out:/scripts/out greenbluelab/musterstadt-giesst-pumpen-harvester path/scripts/out/outfile.json
```

### Test

```bash
pytest
pytest --cov=harvester --cov-fail-under 75 --cov-config=.coveragerc
```

## Inspect Data with Overpass in the Browser
In order to see if there is some crowd-sourced data in OSM, you can checkout the Overpass API: https://overpass-turbo.eu/#

The following command should return round about 95 fountains for Dresden

```
area[name=Dresden]->.searchArea;
node[amenity=fountain](area.searchArea);
out;
```

Read more about the Overpass data mining tool here: https://wiki.openstreetmap.org/wiki/Overpass_turbo

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://fabianmoronzirfas.me/"><img src="https://avatars.githubusercontent.com/u/315106?v=4?s=64" width="64px;" alt="Fabian Morón Zirfas"/><br /><sub><b>Fabian Morón Zirfas</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=ff6347" title="Code">💻</a> <a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=ff6347" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Lisa-Stubert"><img src="https://avatars.githubusercontent.com/u/61182572?v=4?s=64" width="64px;" alt="Lisa-Stubert"/><br /><sub><b>Lisa-Stubert</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=Lisa-Stubert" title="Code">💻</a> <a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=Lisa-Stubert" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vogelino"><img src="https://avatars.githubusercontent.com/u/2759340?v=4?s=64" width="64px;" alt="Lucas Vogel"/><br /><sub><b>Lucas Vogel</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=vogelino" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JensWinter"><img src="https://avatars.githubusercontent.com/u/6548550?v=4?s=64" width="64px;" alt="Jens Winter-Hübenthal"/><br /><sub><b>Jens Winter-Hübenthal</b></sub></a><br /><a href="https://github.com/technologiestiftung/giessdenkiez-de-osm-pumpen-harvester/commits?author=JensWinter" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

<table>
  <tr>
    <td>
      <a src="https://citylab-berlin.org/en/start/">
        <br />
        <br />
        <img width="200" src="https://logos.citylab-berlin.org/logo-citylab-berlin.svg" />
      </a>
    </td>
    <td>
      A project by: <a src="https://www.technologiestiftung-berlin.de/en/">
        <br />
        <br />
        <img width="150" src="https://logos.citylab-berlin.org/logo-technologiestiftung-berlin-en.svg" />
      </a>
    </td>
    <td>
      Supported by:
      <br />
      <br />
      <img width="120" src="https://logos.citylab-berlin.org/logo-berlin.svg" />
    </td>
  </tr>
</table>
