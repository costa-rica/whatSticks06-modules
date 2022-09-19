import os
import json

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':
    with open(r"C:\Users\captian2020\Documents\config_files\config_wsh06.json") as config_file:
        config = json.load(config_file)
elif os.environ.get('COMPUTERNAME')=='NICKSURFACEPRO4':
    with open(r"C:\Users\Costa Rica\Documents\_configs\config_wsh06.json") as config_file:
        config = json.load(config_file)
else:
    with open('/home/ubuntu/config_wsh06.json') as config_file:
        config = json.load(config_file)


class ConfigDev:
    DEBUG = True
    PORT='5000'
    SECRET_KEY = config.get('SECRET_KEY')
    SQL_URI = config.get('SQL_URI')
    
    #Email stuff
    MAIL_SERVER = config.get('MAIL_SERVER_MSOFFICE')
    MAIL_PORT = config.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('MAIL_EMAIL_DD')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD_DD')
    #web
    GUEST_EMAIL = config.get('GUEST_EMAIL')
    GUEST_PASSWORD = config.get('GUEST_PASSWORD')
    #WSH API
    WSH_API_URL_BASE = config.get('WSH_API_URL_BASE')
    WSH_API_PASSWORD = config.get('WSH_API_PASSWORD')
    #WEATHER
    WEATHER_API_KEY = config.get('WEATHER_API_KEY')
    WEATHER_API_URL_BASE = config.get('WEATHER_API_URL_BASE')
    #Oura
    OURA_API_URL_BASE = config.get('OURA_API_URL_BASE')



class ConfigProd:
    DEBUG = False
    PORT='80'
    SECRET_KEY = config.get('SECRET_KEY')
    SQL_URI = config.get('SQL_URI')
    
    #Email stuff
    MAIL_SERVER = config.get('MAIL_SERVER_MSOFFICE')
    MAIL_PORT = config.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('MAIL_EMAIL_DD')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD_DD')
    #web
    GUEST_EMAIL = config.get('GUEST_EMAIL')
    GUEST_PASSWORD = config.get('GUEST_PASSWORD')
    #WSH API
    WSH_API_URL_BASE = config.get('WSH_API_URL_BASE')
    WSH_API_PASSWORD = config.get('WSH_API_PASSWORD')
    #WEATHER
    WEATHER_API_KEY = config.get('WEATHER_API_KEY')
    WEATHER_API_URL_BASE = config.get('WEATHER_API_URL_BASE')
    #Oura
    OURA_API_URL_BASE = config.get('OURA_API_URL_BASE')

