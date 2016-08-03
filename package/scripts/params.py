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

from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import status_params

# server configurations
config = Script.get_config()

logstash_user = config['configurations']['logstash-env']['logstash_user']
logstash_user_group = config['configurations']['logstash-env']['logstash_user_group']
elastic_user = config['configurations']['elastic-env']['elastic_user']
elastic_user_group = config['configurations']['elastic-env']['elastic_user_group']
kibana_user = config['configurations']['kibana-env']['kibana_user']
kibana_user_group = config['configurations']['kibana-env']['kibana_user_group']

elastic_home = "/usr/share/elasticsearch"
elastic_plugins = "/usr/share/elasticsearch/plugins"
elastic_bin = "/usr/share/elasticsearch/bin"
elastic_script_dir = "/etc/elasticsearch/scripts"
elastic_conf_dir = "/etc/elasticsearch"
elastic_data_dir = config['configurations']['elasticsearch-site']['path.data']
elastic_log_dir = config['configurations']['elasticsearch-site']['path.logs']

logstash_home = "/opt/logstash"
logstash_bin = "/opt/logstash/bin"
logstash_conf_dir = "/etc/logstash/conf.d"
logstash_log_dir = "/var/log/logstash"
logstash_sincedb_path = format("{logstash_log_dir}/.sincedb")

kibana_home = "/opt/kibana"
kibana_bin = "/opt/kibana/bin"
kibana_conf_dir = "/opt/kibana/config"
kibana_log_dir = config['configurations']['kibana-site']['logging.dest']

logstash_pid_dir = status_params.logstash_pid_dir
logstash_pid_file = status_params.logstash_pid_file
elastic_pid_dir = status_params.elastic_pid_dir
elastic_pid_file = status_params.elastic_pid_file
kibana_pid_dir = status_params.kibana_pid_dir
kibana_pid_file = status_params.kibana_pid_file

hostname = config['hostname']
java64_home = config['hostLevelParams']['java_home']

elastic_cluster_name = config['configurations']['elasticsearch-site']['cluster.name']
elastic_port = config['configurations']['elasticsearch-site']['http.port']

kibana_port = config['configurations']['kibana-site']['server.port']
kinana_index = config['configurations']['kibana-site']['kibana.index']

logstash_elastic_index = config['configurations']['logstash-data-source']['elastic.index']
logstash_source_file = config['configurations']['logstash-data-source']['source.file']
logstash_source_type = config['configurations']['logstash-data-source']['source.type']

elastic_data_hosts = default("/clusterHostInfo/elastic_datanode_hosts", [])