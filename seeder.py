from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from datetime import datetime
from d import Base, Country, Olympic, Player, Event, Result

engine = create_engine("postgresql://postgres:password@localhost:5432/olympics")
Session = sessionmaker(bind=engine)
session = Session()

def clear_database(session):
    session.query(Result).delete()
    session.query(Event).delete()
    session.query(Player).delete()
    session.query(Olympic).delete()
    session.query(Country).delete()
    session.commit()

def seed_database(session):
    faker = Faker()

    countries = [
        Country(
            name=faker.country(),
            country_id=faker.unique.country_code(),
            area_sqkm=random.randint(50000, 3000000),
            population=random.randint(1000000, 150000000)
        ) for _ in range(10)
    ]
    session.add_all(countries)
    session.commit()

    olympics = [
        Olympic(
            olympic_id=f"O{faker.unique.random_int(1000, 9999)}",
            country_id=random.choice(countries).country_id,
            city=faker.city(),
            year=random.choice([2000, 2004, 2008, 2012]),
            startdate=datetime(2004, 7, 1),
            enddate=datetime(2004, 7, 15)
        ) for _ in range(5)
    ]
    session.add_all(olympics)
    session.commit()

    players = [
        Player(
            name=faker.name(),
            player_id=f"P{faker.unique.random_int(1000, 9999)}",
            country_id=random.choice(countries).country_id,
            birthdate=faker.date_of_birth(minimum_age=18, maximum_age=40)
        ) for _ in range(50)
    ]
    session.add_all(players)
    session.commit()

    events = [
        Event(
            event_id=f"E{faker.unique.random_int(100, 999)}",
            name=faker.word(),
            eventtype=random.choice(["individual", "team"]),
            olympic_id=random.choice(olympics).olympic_id,
            is_team_event=random.choice([0, 1]),
            num_players_in_team=random.randint(1, 10),
            result_noted_in="time" if random.choice([0, 1]) else "score"
        ) for _ in range(20)
    ]
    session.add_all(events)
    session.commit()

    results = set()
    while len(results) < 100:
        event = random.choice(events)
        player = random.choice(players)
        result_key = (event.event_id, player.player_id)
        if result_key not in results:
            medal = random.choice(["GOLD", "SILVER", "BRONZE", None])
            result_value = round(random.uniform(9.5, 20.0), 2)
            results.add(result_key)
            session.add(Result(event_id=event.event_id, player_id=player.player_id, medal=medal, result=result_value))
    session.commit()

clear_database(session)
seed_database(session)
