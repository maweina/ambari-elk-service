import requests
import json

RESULT_STATE_OK = 'OK'
RESULT_STATE_WARNING = 'WARNING'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_CODE_UNKNOWN = 'UNKNOWN'
RESULT_STATE_UNKNOWN = 'UNKNOWN'
# threshold
MR_EXECTIME_WARNING_THRESHOLD_DEFAULT = 7200
MR_EXECTIME_CRITICAL_THRESHOLD_DEFAULT = 3600
MR_EXECTIME_WARNING_THRESHOLD_KEY = "mr.exectime.warning.threshold"
MR_EXECTIME_CRITICAL_THRESHOLD_KEY = "mr.exectime.critical.threshold"

# the interval to check the metric, default is 1 minute
INTERVAL_PARAM_KEY = 'interval'
INTERVAL_PARAM_DEFAULT = 1
ES_PORT = '{{elasticsearch-site/http.port}}'

def get_tokens():
    """
    Returns a tuple of tokens in the format {{site/property}} that will be used
    to build the dictionary passed into execute
    """
    return (ES_PORT,)


def execute(configurations={}, parameters={}, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label
    
    Keyword arguments:
    configurations (dictionary): a mapping of configuration key to value
    parameters (dictionary): a mapping of script parameter key to value
    host_name (string): the name of this host where the alert is running
    """
    if configurations is None:
        return (RESULT_CODE_UNKNOWN, ['There were no configurations supplied to the script.'])
    if set([ES_PORT]).issubset(configurations):
        url = 'http://localhost:' + configurations[ES_PORT] + '/mylogstash-yarn-apps/_search?'
    else:
        return (RESULT_CODE_UNKNOWN, ['The es_port is a required parameter.'])

    interval = INTERVAL_PARAM_DEFAULT
    if INTERVAL_PARAM_KEY in parameters:
      interval = _coerce_to_integer(parameters[INTERVAL_PARAM_KEY])
    mr_exectime_threshold_warning = MR_EXECTIME_WARNING_THRESHOLD_DEFAULT
    if MR_EXECTIME_WARNING_THRESHOLD_KEY in parameters:
        mr_exectime_threshold_warning =_coerce_to_integer(parameters[MR_EXECTIME_WARNING_THRESHOLD_KEY])
    mr_exectime_threshold_critical = MR_EXECTIME_CRITICAL_THRESHOLD_DEFAULT
    if MR_EXECTIME_CRITICAL_THRESHOLD_KEY in parameters:
        mr_exectime_threshold_critical =_coerce_to_integer(parameters[MR_EXECTIME_CRITICAL_THRESHOLD_KEY])

    # critical applications
    payload = json.loads('{"fields" : ["appId"], "query" : {"bool":  {"must": [ {"and": [{"range" : {"elapsedTime":{"gte": %d}}}, {"range": {"finishedTime": {"gt" : "now-%dm"}}}]}]}}}'%(mr_exectime_threshold_critical,interval))
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)
    except:
        return (RESULT_STATE_UNKNOWN, ['Connection to elasticsearch failed.'])
    output = r.json()
    msgs = []
    err_apps = []
    if "hits" in output and "hits" in output["hits"] and len(output["hits"]["hits"]) > 0:
        for item in output["hits"]["hits"]:
            appId = item["fields"]["appId"][0]
            if appId is not None:
                err_apps.append(appId)
    if len(err_apps) > 0:
        msgs.append("The execution time of MapReduce Job '{0}' is greater than {1} seconds.".format(", ".join(err_apps), mr_exectime_threshold_critical))
        
    # warning applications
    payload = json.loads('{"fields" : ["appId"], "query" : {"bool":  {"must": [ {"and": [{"range" : {"elapsedTime":{"gte": %d, "lte": %d}}}, {"range": {"finishedTime": {"gt" : "now-%dm"}}}]}]}}}'%(mr_exectime_threshold_warning, mr_exectime_threshold_critical,interval))
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)
    except:
        return (RESULT_STATE_UNKNOWN, ['Connection to elasticsearch failed.'])
    output = r.json()
    warn_apps = []
    if "hits" in output and "hits" in output["hits"] and len(output["hits"]["hits"]) > 0:
        for item in output["hits"]["hits"]:
            appId = item["fields"]["appId"][0]
            if appId is not None:
                warn_apps.append(appId)
    if len(warn_apps) > 0:
        msgs.append("The execution time of MapReduce Job '{0}' is greater than {1} seconds and less than {2} seconds.".format(", ".join(warn_apps), mr_exectime_threshold_warning, mr_exectime_threshold_critical))
    
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