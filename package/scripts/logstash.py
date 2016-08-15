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
                   params.logstash_pid_dir]
                   
    Directory(directories,
              owner=params.logstash_user,
              group=params.logstash_user_group,
              mode=0755,
              cd_access='a',
              recursive=True
            )

    if params.mapred_collection_enabled is True:
        host_list = params.mapred_source_hosts.split(',')
        if params.hostname in host_list or host_list[0].strip() == "all":
            File(format("{logstash_conf_dir}/1-logstash-mapred-input.conf"),
                content=Template("logstash-mapred-input.conf.j2"),
                owner=params.logstash_user,
                group=params.logstash_user_group,
                mode=0644
            )
            
            File(format("{logstash_conf_dir}/2-logstash-mapred-filter.conf"),
                content=Template("logstash-mapred-filter.conf.j2"),
                owner=params.logstash_user,
                group=params.logstash_user_group,
                mode=0644
            )
            
            File(format("{logstash_conf_dir}/3-logstash-mapred-output.conf"),
                content=Template("logstash-mapred-output.conf.j2"),
                owner=params.logstash_user,
                group=params.logstash_user_group,
                mode=0644
            )

    if params.hdfs_collection_enabled is True:
        host_list = params.hdfs_source_hosts.split(',')
        if params.hostname in host_list or host_list[0].strip() == "all":
            File(format("{logstash_conf_dir}/1-logstash-hdfs-input.conf"),
                content=Template("logstash-hdfs-input.conf.j2"),
                owner=params.logstash_user,
                group=params.logstash_user_group,
                mode=0644
            )
            
            File(format("{logstash_conf_dir}/2-logstash-hdfs-filter.conf"),
                content=Template("logstash-hdfs-filter.conf.j2"),
                owner=params.logstash_user,
                group=params.logstash_user_group,
                mode=0644
            )
            
            File(format("{logstash_conf_dir}/3-logstash-hdfs-output.conf"),
                content=Template("logstash-hdfs-output.conf.j2"),
                owner=params.logstash_user,
                group=params.logstash_user_group,
                mode=0644
            )