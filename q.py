from sqlalchemy import func, case, or_, cast, Numeric
from d import Country, Olympic, Player, Event, Result
from seeder import session

query1 = (
    session.query(
        func.extract('year', Player.birthdate).label('birth_year'),
        func.count(Player.player_id).label('player_count'),
        func.sum(case((Result.medal == 'GOLD', 1), else_=0)).label('gold_count')
    )
    .join(Result, Result.player_id == Player.player_id)
    .join(Event, Event.event_id == Result.event_id)
    .join(Olympic, Olympic.olympic_id == Event.olympic_id)
    .filter(Olympic.year == 2004)
    .group_by(func.extract('year', Player.birthdate))
)

query2 = (
    session.query(Event.name)
    .join(Result, Result.event_id == Event.event_id)
    .filter(Event.is_team_event == 0)
    .filter(Result.medal == 'GOLD')
    .group_by(Event.name, Result.result)
    .having(func.count(Result.player_id) > 1)
)

query3 = (
    session.query(Player.name, Olympic.olympic_id)
    .join(Result, Result.player_id == Player.player_id)
    .join(Event, Event.event_id == Result.event_id)
    .join(Olympic, Olympic.olympic_id == Event.olympic_id)
    .filter(Result.medal.in_(['GOLD', 'SILVER', 'BRONZE']))
    .distinct()
)

query4 = (
    session.query(
        Country.name,
        (func.count(Player.player_id) / cast(Country.population, Numeric) * 100).label('percentage')
    )
    .join(Player, Player.country_id == Country.country_id)
    .filter(
        or_(
            Player.name.ilike('A%'),
            Player.name.ilike('E%'),
            Player.name.ilike('I%'),
            Player.name.ilike('O%'),
            Player.name.ilike('U%')
        )
    )
    .group_by(Country.name, Country.population)
    .order_by((func.count(Player.player_id) / cast(Country.population, Numeric)).desc())
    .first()
)

query5 = (
    session.query(
        Country.name,
        (func.count(Result.medal) / Country.population).label('team_medal_ratio')
    )
    .join(Player, Player.country_id == Country.country_id)
    .join(Result, Result.player_id == Player.player_id)
    .join(Event, Event.event_id == Result.event_id)
    .join(Olympic, Olympic.olympic_id == Event.olympic_id)
    .filter(Olympic.year == 2000)
    .filter(Event.is_team_event == 1)
    .group_by(Country.name, Country.population)
    .order_by((func.count(Result.medal) / Country.population).asc())
    .limit(5)
)

print("Query 1 Results:")
for row in query1:
    print(row)

print("\nQuery 2 Results:")
for row in query2:
    print(row)

print("\nQuery 3 Results:")
for row in query3:
    print(row)

print("\nQuery 4 Result:")
print(query4)

print("\nQuery 5 Results:")
for row in query5:
    print(row)