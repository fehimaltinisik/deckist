# DeckIst Webservice

This is the webservice for the DeckIst. It's built using FastAPI.

## Prerequisites

To run webservice locally, follow these steps:


1. Clone this repository:
    ```bash
    git clone https://github.com/fehimaltinisik/deckist.git
    ```

2. Navigate to the project directory:
    ```bash
    cd deckist/webservice
    ```

3. Python 3.10 is required to run this project. You can download the latest version of Python from the [official website](https://www.python.org/downloads/). Then install dependencies using following commands.
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

### Init Db
Project uses small SQLite database to store GTFS data. You can create the database by following setups below.
Run the scripts from the `webservice` directory with `PYTHONPATH=.` so they can import `src`.

Data sources:
- [İETT GTFS](https://data.ibb.gov.tr/dataset/iett-gtfs-verisi) for routes, trips, stops and stop times. İETT is Istanbul's public bus operator.
- [İETT Hat Güzergahları](https://data.ibb.gov.tr/dataset/iett-hat-guzergahlari) ("line routes") for on-road route geometries.

Downloaded files and the database are gitignored.

4. `scripts/downloadgtfs.py`: Downloads the GTFS CSVs (stop times come from `stop_times.zip`) and the route geometry GeoJSON into **src.resources.gtfs**.
```bash
python scripts/downloadgtfs.py
```

5. `scripts/preprocessgtfs.py`: Reads the raw UTF-8 files, repairs double-encoded route names, normalizes stop coordinates (stops without usable coordinates are dropped together with their stop times, and trips whose first or last stop is untimed or dropped are removed) and writes `*.clean.csv` files.
```bash
python scripts/preprocessgtfs.py
```

6. `scripts/savegtfstodb.py`: Saves the cleaned CSVs to a SQLite database using the Tortoise ORM. Start from an empty database; running this script will create a local SQLite database.
```bash
python scripts/savegtfstodb.py
```

7. `scripts/saveroutepathstodb.py`: Loads the Hat Güzergahları GeoJSON into the `route_path` table of the same database. Lines are simplified (~5 m) and rounded to 5 decimals. The API uses them to draw trips on the road.
```bash
python scripts/saveroutepathstodb.py
```

### How trips are drawn

GTFS has no shapes, so every trip is matched to a route line from the `route_path` table:

1. A route line whose code (`GUZERGAH_KODU`) equals the GTFS `route_code`, for example `500T_G_D0`.
2. Otherwise a route line of the same line and direction (`YON`: `GİDİŞ` is direction `0`, `DÖNÜŞ` is `1`), preferring the main departure (`DEPAR_NO` `0`), then the longest.

The trip's stops are projected onto that line in order (`src/services/geometry.py`). The line is trimmed to the first
and last stop, and the time between the first departure and the last arrival is spread over the distance along it.
A few middle stops may sit off the line; the first and last stops must fit.

When a trip has no route line, or its stops do not fit, it is drawn as straight segments between stops with times
spread by haversine distance. With the 2026 feed this affects about 0.05% of trips.

### Tests
```bash
python -m pytest
```

### Configuration

Environment variables are listed in `.env.example`. They are read from the process environment.

## Running the Project

Once you have installed the dependencies and created the database, you can run the project using the following command.
```bash
python main.py
```

Project will be running on `http://localhost:8000`.

## License

DeckIst is licensed under the [MIT License](LICENSE), allowing for flexibility in use and distribution.

## Data License

It's important to note that while the code for this repository is licensed under the MIT License, the GTFS dataset used
in the project is subject to its own licensing terms. Users should refer to the
specifics [licensing information](https://data.ibb.gov.tr/license) provided by The Istanbul Metropolitan Municipality for
the dataset.
