import requests
import json

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'

def execute(configurations={}, parameters={}, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label
    
    Keyword arguments:
    configurations (dictionary): a mapping of configuration key to value
    parameters (dictionary): a mapping of script parameter key to value
    host_name (string): the name of this host where the alert is running
    """

    url = 'http://localhost:9200/logstash-mapred/_search?'
    payload = json.loads('{"fields" : ["appId"], "query" : {"range" : {"executionTime":{"gte": "100"}, "@timestamp": {"gt" : "now-1m"}}}}')
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    output = r.json()
    
    errors = []
    apps = []
    if "hits" in output and "hits" in output["hits"] and len(output["hits"]["hits"]) > 0:
        for item in output["hits"]["hits"]:
            appId = item["fields"]["appId"][0]
            if appId is not None:
                apps.append(appId)
                
    if len(apps) > 0:
        errors.append("The executionTime of applications '{0}' is greater than 100 seconds.".format(", ".join(apps)))
    
    # Determine the status based on errors.    
    if len(errors) == 0:
        status = RESULT_STATE_OK
        messages = []
        return (status, ["\n".join(messages)])
    else:
        # Report errors
        return (RESULT_STATE_CRITICAL, ["\n".join(errors)])
        
if __name__ == "__main__":
    result = execute()
    print result