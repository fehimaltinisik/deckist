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
- [İETT GTFS](https://data.ibb.gov.tr/dataset/iett-gtfs-verisi) for routes, trips, stops and stop times.
- [İETT Hat Güzergahları](https://data.ibb.gov.tr/dataset/iett-hat-guzergahlari) for on-road route geometries.

Downloaded files and the database are gitignored.

4. `scripts/downloadgtfs.py`: Downloads the GTFS CSVs (stop times come from `stop_times.zip`) and the route geometry GeoJSON into **src.resources.gtfs**.
```bash
python scripts/downloadgtfs.py
```

5. `scripts/preprocessgtfs.py`: Reads the raw UTF-8 files, repairs double-encoded route names, normalizes stop coordinates (stops without usable coordinates are dropped together with their stop times, and trips that lose a timed first or last stop are dropped) and writes `*.clean.csv` files.
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
