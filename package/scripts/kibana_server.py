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
from kibana import kibana
import sys
class KibanaMaster(Script):
  def install(self, env):
    import params
    env.set_params(params)
    self.install_packages(env)
    reload(sys)                         
    sys.setdefaultencoding('utf-8')  
    File(format("{kibana_home}/optimize/bundles/src/ui/public/images/kibana.svg"),
         content=Template(format("kibana.svg")),
         owner=params.kibana_user,
         group=params.kibana_user_group,
         mode=0644
    )
    
  def configure(self, env):
    import params
    env.set_params(params)
    kibana()

  def start(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    self.configure(env)
    start_cmd = format("service kibana start")
    Execute(start_cmd)

  def stop(self, env, upgrade_type=None):
      import params
      env.set_params(params)
      stop_cmd = format("service kibana stop")
      Execute(stop_cmd)

  def status(self, env):
      import params
      env.set_params(params)
      check_process_status(params.kibana_pid_file)

if __name__ == "__main__":
  KibanaMaster().execute()
