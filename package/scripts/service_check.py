#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
from __future__ import print_function
from resource_management import *
import  sys,subprocess,os
import requests
import time

class ServiceCheck(Script):
  def service_check(self, env):
    import params
    env.set_params(params)

    # There is a race condition by the time the BDSE server starts and service checks.  Hence added the below sleep for 20 seconds
    time.sleep(20)
    payload = {'name': 'Buddy.  Dont Worry, I am Fine '} 
    r = requests.get(format("http://localhost:/{elastic_port}"),params=payload) 
    if r.status_code == 200:
    print(r.json(), file=sys.stdout)
      sys.exit(0)
    else:
       print("Elasticsearch is not running", file=sys.stderr)
      sys.exit(1)
            
    r = requests.get(format('http://localhost:{kibana_port}/app/kibana'))
    if r.status_code == 200:
      print(r.json(), file=sys.stdout)
      sys.exit(0)
    else:
      print("Kibana is not running", file=sys.stderr)
      sys.exit(1)

if __name__ == "__main__":
    ServiceCheck().execute()