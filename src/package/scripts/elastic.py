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

def elastic(name=None):
    import params
    
    directories = [params.elastic_home,
                   params.elastic_log_dir, 
                   params.elastic_data_dir,
                   params.elastic_conf_dir,
                   params.elastic_script_dir,
                   params.elastic_pid_dir]
                   
    Directory(directories,
              owner=params.elastic_user,
              group=params.elastic_user_group,
              mode=0755,
              cd_access='a'
            )

    File(format("{elastic_conf_dir}/elasticsearch.yml"),
       content=Template(format("elasticsearch-{name}.yml.j2")),
       owner=params.elastic_user,
       group=params.elastic_user_group,
       mode=0644
    )
    
    File(format("/etc/sysconfig/elasticsearch"),
       content=Template(format("elasticsearch.sysconfig.j2")),
       owner=params.elastic_user,
       group=params.elastic_user_group,
       mode=0755
    )
    
    File(format("/usr/lib/systemd/system/elasticsearch.service"),
       content=Template(format("elasticsearch.service.j2")),
       owner=params.elastic_user,
       group=params.elastic_user_group,
       mode=0755
    )