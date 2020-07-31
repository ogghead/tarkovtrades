TESTING = True
DEBUG = True
MONGODB_SETTINGS = {
    'host': 'mongo',
    'port': 27017
}
DEBUG_TB_PANELS = ['flask_mongoengine.panels.MongoDebugPanel']
SECRET_KEY = 'test1234'