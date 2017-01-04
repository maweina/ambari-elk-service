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
from resource_management import *
import json
import urllib3
queueNames=[]

def parse_queue(queueList, parent):
    global queueNames
    for queue in queueList:
        name = queue['queueName']
        path = parent + '.' + name
        if 'queues' in queue and 'queue' in queue['queues']:
            parse_queue(queue['queues']['queue'], path)
        else:
            queueNames.append(path)

def yarn_scheduler(params):
    queueNameList=['root.default']
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://' + params.rm_host + ':' + params.rm_port + '/ws/v1/cluster/scheduler', timeout=5.0)
    except:
        print "Excpetion: Yarn Rest Api of Scheduler Connection Failed."
    else:
        if r.status == 200:
            output = json.loads(r.data.decode('utf-8'))
            rootQueue = output['scheduler']['schedulerInfo']['queueName']
            if 'queues' in output['scheduler']['schedulerInfo'] and 'queue' in output['scheduler']['schedulerInfo']['queues']:
                queues = output['scheduler']['schedulerInfo']['queues']['queue']
                parse_queue(queues, rootQueue)
                queueNameList = queueNames
    return queueNameList

def kibana(role=None):
    import params    
    directories = [params.kibana_home,
                   params.kibana_log_dir, 
                   params.kibana_conf_dir]
                   
    Directory(directories,
              owner=params.kibana_user,
              group=params.kibana_user_group,
              mode=0755,
              cd_access='a'
            )

    File(format("{kibana_conf_dir}/kibana.yml"),
       content=Template("kibana.yml.j2"),
       owner=params.kibana_user,
       group=params.kibana_user_group,
       mode=0644
    )
    
    File(format("/etc/sysconfig/kibana"),
       content=Template(format("kibana.sysconfig.j2")),
       owner=params.kibana_user,
       group=params.kibana_user_group,
       mode=0755
    )
    
    File(format("/usr/lib/systemd/system/kibana.service"),
       content=Template(format("kibana.service.j2")),
       owner=params.kibana_user,
       group=params.kibana_user_group,
       mode=0755
    )
    queueNameList = yarn_scheduler(params)
    File(format("{kibana_home}/graphs.json"),
          content=Template(format("graphs.json.j2"),[],queueNames=queueNameList),
          owner=params.kibana_user,
          group=params.kibana_user_group,
          mode=0755
    )
    File(format("{kibana_home}/graphs-search.json"),
          content=Template(format("graphs-search.json.j2"),[],queueNames=queueNameList),
          owner=params.kibana_user,
          group=params.kibana_user_group,
          mode=0755
    )
    File(format("{kibana_home}/kibana-create-index-patterns.sh"),
         content=Template(format("kibana-create-index-patterns.sh.j2")),
         owner=params.kibana_user,
         group=params.kibana_user_group,
         mode=0755
         )
