from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, \
    Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from wsh_config import ConfigDev, ConfigProd
from flask_login import UserMixin, LoginManager


config = ConfigDev()

Base = declarative_base()
engine = create_engine(config.SQL_URI, echo = False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
sess = Session()

login_manager= LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(any_name_for_id_obj):# any_name_for_id_obj can be any name because its an arg that is the user id.
    # This is probably created somewhere inside flask_login when the user gets logged in. But i've not been able to track it.
    print('* in load_user *')
    print(any_name_for_id_obj)
    return sess.query(Users).filter_by(id = any_name_for_id_obj).first()
    

class Users(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email = Column(Text, unique = True, nullable = False)
    password = Column(Text, nullable = False)
    lat = Column(Float)
    lon = Column(Float)
    oura_token_id = relationship("Oura_token", backref="oura_token_id", lazy=True)
    oura_sleep = relationship('Oura_sleep_descriptions', backref='oura_sleep', lazy=True)
    loc_day = relationship('User_location_day', backref='user_loc_day', lazy=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email})'

class User_location_day(Base):
    __tablename__ = 'user_loc_day'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location_id = Column(Integer, nullable = False)
    date = Column(Text)
    local_time = Column(Text)
    avgtemp_f = Column(Float)
    score_total = Column(Integer)
    row_type = Column(Text)#user entered or scheduler entered row?
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'User_location_day(id: {self.id}, user_id: {self.user_id},' \
            f'date: {self.date}, avgtemp_f: {self.avgtemp_f}, score_total: {self.score_total})'

class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer,  primary_key = True)
    city = Column(Text)
    region = Column(Text)
    country = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Locations(id: {self.id}, city: {self.city}, lat: {self.lat}, ' \
            f'lon: {self.lon})'

class Oura_token(Base):
    __tablename__ = 'oura_token'
    id = Column(Integer, primary_key = True )
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(Text)
    oura_sleep = relationship('Oura_sleep_descriptions', backref='Oura_sleep_descrip', lazy=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Oura_token(id: {self.id}, token: {self.token})'


class Weather_history(Base):
    __tablename__ = 'weather_history'
    id = Column(Integer,primary_key = True)
    location_id = Column(Integer, nullable = False)
    lat = Column(Float)
    lon = Column(Float)
    city_location_name = Column(Text)
    region_name = Column(Text)
    country_name = Column(Text)
    tz_id = Column(Text)
    date = Column(Text)
    maxtemp_f = Column(Float)
    mintemp_f = Column(Float)
    avgtemp_f = Column(Float)
    sunset = Column(Text)
    sunrise = Column(Text)
    time_stamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Weather_history(id: {self.id}, date: {self.date}, " \
            f"city_location_name: {self.city_location_name}, avgtemp_f: {self.avgtemp_f})"



class Oura_sleep_descriptions(Base):
    __tablename__ = 'oura_sleep_descriptions'
    id = Column(Integer, primary_key = True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False)
    token_id=Column(Integer, ForeignKey('oura_token.id'), nullable=False)
    summary_date = Column(Text)
    period_id = Column(Integer)
    is_longest = Column(Integer)
    timezone = Column(Integer)
    bedtime_end = Column(Text)
    bedtime_start = Column(Text)
    breath_average = Column(Float)
    duration = Column(Integer)
    total = Column(Integer)
    awake = Column(Integer)
    rem = Column(Integer)
    deep = Column(Integer)
    light = Column(Integer)
    midpoint_time = Column(Integer)
    efficiency = Column(Integer)
    restless = Column(Integer)
    onset_latency = Column(Integer)
    rmssd = Column(Integer)
    score = Column(Integer)
    score_alignment = Column(Integer)
    score_deep = Column(Integer)
    score_disturbances = Column(Integer)
    score_efficiency = Column(Integer)
    score_latency = Column(Integer)
    score_rem = Column(Integer)
    score_total = Column(Integer)
    temperature_deviation = Column(Float)
    bedtime_start_delta = Column(Integer)
    bedtime_end_delta = Column(Integer)
    midpoint_at_delta = Column(Integer)
    temperature_delta = Column(Float)
    hr_lowest = Column(Integer)
    hr_average = Column(Float)
    # temperature_trend_deviation=Column(Float)

    time_stamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Oura_sleep_descriptions(id: {self.id}, user_id: {self.user_id}," \
            f"summary_date:{self.summary_date}," \
            f"score: {self.score}, score_total: {self.score_total}," \
            f"hr_lowest: {self.hr_lowest}, hr_average: {self.hr_average}," \
            f"bedtime_start: {self.bedtime_start}, bedtime_end: {self.bedtime_end}," \
            f"duration: {self.duration}, onset_latency: {self.onset_latency})"





#Build db
if 'users' in inspect(engine).get_table_names():
    print('db already exists')
else:
    Base.metadata.create_all(engine)
    print('NEW db created.')