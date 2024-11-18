from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'
    name = Column(String(40), nullable=False)
    country_id = Column(String(3), primary_key=True, unique=True)
    area_sqkm = Column(Integer)
    population = Column(Integer)

class Olympic(Base):
    __tablename__ = 'olympics'
    olympic_id = Column(String(7), primary_key=True, unique=True)
    country_id = Column(String(3), ForeignKey('countries.country_id'), nullable=False)
    city = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    startdate = Column(Date)
    enddate = Column(Date)

class Player(Base):
    __tablename__ = 'players'
    name = Column(String(40), nullable=False)
    player_id = Column(String(10), primary_key=True, unique=True)
    country_id = Column(String(3), ForeignKey('countries.country_id'), nullable=False)
    birthdate = Column(Date)

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(String(7), primary_key=True, unique=True)
    name = Column(String(40), nullable=False)
    eventtype = Column(String(20))
    olympic_id = Column(String(7), ForeignKey('olympics.olympic_id'), nullable=False)
    is_team_event = Column(Integer, CheckConstraint("is_team_event IN (0, 1)"), nullable=False)
    num_players_in_team = Column(Integer)
    result_noted_in = Column(String(100))

class Result(Base):
    __tablename__ = 'results'
    event_id = Column(String(7), ForeignKey('events.event_id'), primary_key=True, nullable=False)
    player_id = Column(String(10), ForeignKey('players.player_id'), primary_key=True, nullable=False)
    medal = Column(String(7))
    result = Column(Integer)
