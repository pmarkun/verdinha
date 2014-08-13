try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
import datetime, time
from bson.objectid import ObjectId
from werkzeug import Response
 
class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)
 
def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')

def diasatras(data_inicio, data_fim=None):
    data_inicio = datetime.datetime.fromtimestamp(float(data_inicio))
    if (data_fim):
        data_fim = datetime.datetime.fromtimestamp(float(data_fim))
    else:
        data_fim = datetime.datetime.today()
    return (data_fim - data_inicio).days

def futuro():
    return time.mktime((datetime.datetime.now()+datetime.timedelta(1)).timetuple())
