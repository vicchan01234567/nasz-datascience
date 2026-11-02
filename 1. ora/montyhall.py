"""Simulate the Monty Hall problem and store every game in SQLite."""

import argparse
import csv
import random
import sqlite3
from contextlib import closing
from pathlib import Path


DOORS = (0, 1, 2)
DEFAULT_DATABASE = Path(__file__).with_name("monty_hall.db")
DEFAULT_CSV = Path(__file__).with_name("monty_hall_results.csv")


def simulate_game(rng: random.Random) -> tuple[int, int, int, int, int, int]:
    """Return the car, first choice, host reveal, switched choice, and win flags."""
    car = rng.choice(DOORS)
    first_choice = rng.choice(DOORS)

    host_options = [
        door for door in DOORS if door != car and door != first_choice
    ]
    revealed = rng.choice(host_options)
    switched_choice = next(
        door for door in DOORS if door != first_choice and door != revealed
    )

    stay_won = int(first_choice == car)
    switch_won = int(switched_choice == car)
    return car, first_choice, revealed, switched_choice, stay_won, switch_won


def create_database(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY,
            trials INTEGER NOT NULL CHECK (trials > 0),
            seed INTEGER
        );

        CREATE TABLE IF NOT EXISTS games (
            run_id INTEGER NOT NULL REFERENCES runs(run_id),
            trial INTEGER NOT NULL CHECK (trial > 0),
            car_door INTEGER NOT NULL CHECK (car_door BETWEEN 0 AND 2),
            first_choice INTEGER NOT NULL CHECK (first_choice BETWEEN 0 AND 2),
            host_revealed INTEGER NOT NULL CHECK (host_revealed BETWEEN 0 AND 2),
            switched_choice INTEGER NOT NULL CHECK (switched_choice BETWEEN 0 AND 2),
            stay_won INTEGER NOT NULL CHECK (stay_won IN (0, 1)),
            switch_won INTEGER NOT NULL CHECK (switch_won IN (0, 1)),
            PRIMARY KEY (run_id, trial),
            CHECK (host_revealed != car_door),
            CHECK (host_revealed != first_choice),
            CHECK (switched_choice != first_choice),
            CHECK (switched_choice != host_revealed),
            CHECK (stay_won = (first_choice = car_door)),
            CHECK (switch_won = (switched_choice = car_door))
        );
        """
    )


def run_simulation(
    trials: int,
    seed: int | None,
    database: Path,
    csv_output: Path = DEFAULT_CSV,
) -> None:
    rng = random.Random(seed)
    database.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(database)) as connection:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            create_database(connection)
            cursor = connection.execute(
                "INSERT INTO runs (trials, seed) VALUES (?, ?)", (trials, seed)
            )
            run_id = cursor.lastrowid
            if run_id is None:
                raise RuntimeError(
                    "SQLite did not return an ID for the simulation run."
                )

            connection.executemany(
                """
                INSERT INTO games (
                    run_id, trial, car_door, first_choice, host_revealed,
                    switched_choice, stay_won, switch_won
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    (run_id, trial, *simulate_game(rng))
                    for trial in range(1, trials + 1)
                ),
            )

            stay_wins, switch_wins = connection.execute(
                """
                SELECT SUM(stay_won), SUM(switch_won)
                FROM games
                WHERE run_id = ?
                """,
                (run_id,),
            ).fetchone()

            csv_output.parent.mkdir(parents=True, exist_ok=True)
            with csv_output.open("w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    (
                        "record_type",
                        "trial",
                        "car_door",
                        "first_choice",
                        "host_revealed",
                        "switched_choice",
                        "stay_won",
                        "switch_won",
                        "stay_win_rate",
                        "switch_win_rate",
                    )
                )
                for row in connection.execute(
                    """
                    SELECT trial, car_door + 1, first_choice + 1,
                           host_revealed + 1, switched_choice + 1,
                           stay_won, switch_won
                    FROM games
                    WHERE run_id = ?
                    ORDER BY trial
                    """,
                    (run_id,),
                ):
                    writer.writerow(("GAME", *row, "", ""))
                writer.writerow(
                    (
                        "TOTAL",
                        trials,
                        "",
                        "",
                        "",
                        "",
                        stay_wins,
                        switch_wins,
                        stay_wins / trials,
                        switch_wins / trials,
                    )
                )

    print(f"Recorded {trials:,} games in {database}")
    print(f"CSV results: {csv_output}")
    print(f"Stay wins:   {stay_wins:,} ({stay_wins / trials:.2%})")
    print(f"Switch wins: {switch_wins:,} ({switch_wins / trials:.2%})")
    print("Theory:      staying wins 1/3 of the time; switching wins 2/3.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate Monty Hall games and store them in SQLite."
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=100_000,
        help="number of games to simulate (default: 100000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="optional random seed for repeatable results",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help=f"SQLite database path (default: {DEFAULT_DATABASE})",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"CSV results path (default: {DEFAULT_CSV})",
    )
    args = parser.parse_args()

    if args.trials <= 0:
        parser.error("--trials must be a positive integer")

    run_simulation(args.trials, args.seed, args.database, args.csv)


if __name__ == "__main__":
    main()