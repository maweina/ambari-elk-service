import requests
import json

RESULT_STATE_OK = 'OK'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_CRITICAL = 'CRITICAL'

# threshold
THRESHOLD_CRITICAL = 100
THRESHOLD_WARNING = 50

# the interval to check the metric, default is 1 minute
INTERVAL_PARAM_KEY = 'interval'
INTERVAL_PARAM_DEFAULT = 1

def execute(configurations={}, parameters={}, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label
    
    Keyword arguments:
    configurations (dictionary): a mapping of configuration key to value
    parameters (dictionary): a mapping of script parameter key to value
    host_name (string): the name of this host where the alert is running
    """

    url = 'http://localhost:9200/logstash-mapred/_search?'
    interval = INTERVAL_PARAM_DEFAULT
    if INTERVAL_PARAM_KEY in parameters:
      interval = _coerce_to_integer(parameters[INTERVAL_PARAM_KEY])
      
    # critical applications
    payload = json.loads('{"fields" : ["appId"], "query" : {"bool":  {"must": [ {"and": [{"range" : {"executionTime":{"gte": %d}}}, {"range": {"@timestamp": {"gt" : "now-%dm"}}}]}]}}}'%(THRESHOLD_CRITICAL,interval))
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    output = r.json()
    
    msgs = []
    err_apps = []
    if "hits" in output and "hits" in output["hits"] and len(output["hits"]["hits"]) > 0:
        for item in output["hits"]["hits"]:
            appId = item["fields"]["appId"][0]
            if appId is not None:
                err_apps.append(appId)
                
    if len(err_apps) > 0:
        msgs.append("The executionTime of applications '{0}' is greater than {1} seconds.".format(", ".join(err_apps), THRESHOLD_CRITICAL))
        
    # warning applications
    payload = json.loads('{"fields" : ["appId"], "query" : {"bool":  {"must": [ {"and": [{"range" : {"executionTime":{"gte": %d, "lte": %d}}}, {"range": {"@timestamp": {"gt" : "now-%dm"}}}]}]}}}'%(THRESHOLD_WARNING, THRESHOLD_CRITICAL,interval))
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    output = r.json() 

    warn_apps = []
    if "hits" in output and "hits" in output["hits"] and len(output["hits"]["hits"]) > 0:
        for item in output["hits"]["hits"]:
            appId = item["fields"]["appId"][0]
            if appId is not None:
                warn_apps.append(appId)

    if len(warn_apps) > 0:
        msgs.append("; The executionTime of applications '{0}' is greater than {1} and less than {2}seconds.".format(", ".join(warn_apps), THRESHOLD_WARNING, THRESHOLD_CRITICAL))
    
    # Determine the status based on errors.    
    if len(err_apps) == 0 and len(warn_apps) == 0:
        return (RESULT_STATE_OK, ["\n".join([])])
    elif len(err_apps) > 0:
        # Report errors
        return (RESULT_STATE_CRITICAL, ["\n".join(msgs)])
    else:
        # Report warnings
        return (RESULT_STATE_WARNING, ["\n".join(msgs)])
        
def _coerce_to_integer(value):
  """
  Attempts to correctly coerce a value to an integer. For the case of an integer or a float,
  this will essentially either NOOP or return a truncated value. If the parameter is a string,
  then it will first attempt to be coerced from a integer, and failing that, a float.
  :param value: the value to coerce
  :return: the coerced value as an integer
  """
  try:
    return int(value)
  except ValueError:
    return int(float(value))
        
if __name__ == "__main__":
    result = execute()
    print result