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
import sys
from copy import deepcopy

def logstash(role=None):
    import params
    
    directories = [params.logstash_home,
                   params.logstash_log_dir,
                   params.logstash_conf_dir,
                   params.logstash_pid_dir,
                   params.logstash_sincedb_path]
                   
    Directory(directories,
              owner=params.logstash_user,
              group=params.logstash_user_group,
              mode=0755,
              cd_access='a'
            )

    if (params.logstash_conf != None):
        File(format("{logstash_conf_dir}/logstash.conf"),
             content=InlineTemplate(params.logstash_conf),
             owner=params.logstash_user,
             group=params.logstash_user_group,
             mode=0644
        )
        
    File(format("{logstash_bin}/yarn-apps.py"),
         content=Template(format("yarn-apps.py.j2")),
         owner=params.logstash_user,
         group=params.logstash_user_group,
         mode=0644
    )
    
    File(format("{logstash_log_dir}/template-running.json"),
         content=Template(format("template-running.json.j2")),
         owner=params.logstash_user,
         group=params.logstash_user_group,
         mode=0644
    )
    
    File(format("{logstash_log_dir}/template-disk.json"),
         content=Template(format("template-disk.json.j2")),
         owner=params.logstash_user,
         group=params.logstash_user_group,
         mode=0644
    )
    
    File(format("{logstash_log_dir}/template-finished.json"),
         content=Template(format("template-finished.json.j2")),
         owner=params.logstash_user,
         group=params.logstash_user_group,
         mode=0644
    )
    File(format("{logstash_log_dir}/template-service-log.json"),
         content=Template(format("template-service-log.json.j2")),
         owner=params.logstash_user,
         group=params.logstash_user_group,
         mode=0644
    )
