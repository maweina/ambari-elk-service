#!/usr/bin/env python


import os
import socket

from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.exceptions import ComponentIsNotRunning

RESULT_CODE_OK = 'OK'
RESULT_CODE_CRITICAL = 'CRITICAL'
RESULT_CODE_UNKNOWN = 'UNKNOWN'

LOGSTASH_PID_DIR = '{{logstash-env/logstash_pid_dir}}'

def get_tokens():
    """
    Returns a tuple of tokens in the format {{site/property}} that will be used
    to build the dictionary passed into execute
    """
    return (LOGSTASH_PID_DIR,)


def is_logstash_process_live(pid_file):
    """
    Gets whether the logstash represented by the specified file is running.
    :param pid_file: the PID file of the logstash to check
    :return: True if the logstash is running, False otherwise
    """
    live = False

    try:
        check_process_status(pid_file)
        live = True
    except ComponentIsNotRunning:
        pass

    return live


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

    if set([LOGSTASH_PID_DIR]).issubset(configurations):
        LOGSTASH_PID_PATH = os.path.join(configurations[LOGSTASH_PID_DIR], 'logstash.pid')
    else:
        return (RESULT_CODE_UNKNOWN, ['The logstash_pid_dir is a required parameter.'])

    if host_name is None:
        host_name = socket.getfqdn()

    logstash_process_running = is_logstash_process_live(LOGSTASH_PID_PATH)

    alert_state = RESULT_CODE_OK if logstash_process_running else RESULT_CODE_CRITICAL

    alert_label = 'Logstasgh Agent is running on {0}' if logstash_process_running else 'Logstasgh Agent is NOT running on {0}'
    alert_label = alert_label.format(host_name)

    return (alert_state, [alert_label])
