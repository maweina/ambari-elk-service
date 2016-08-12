# ambari-elk-service 

Ambari service for installing and managing ElK stack on HDP clusters.

- Ambari Version=2.2.2
- Elasticsearch Version=2.3.5
- Logstash Version=2.3.4
- Kibana Version=4.5.4

## Add ELK Repository

Edit "/var/lib/ambari-server/resources/stacks/HDP/2.4/repos/repoinfo.xml" to add additional <repo> entries for ELK.

```
  <os family="redhat6">
    <repo>
      <baseurl>http://public-repo-1.hortonworks.com/HDP/centos6/2.x/updates/2.4.0.0</baseurl>
      <repoid>HDP-2.4</repoid>
      <reponame>HDP</reponame>
    </repo>
    <repo>
      <baseurl>http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.20/repos/centos6</baseurl>
      <repoid>HDP-UTILS-1.1.0.20</repoid>
      <reponame>HDP-UTILS</reponame>
    </repo>
    <repo>
      <baseurl>https://packages.elastic.co/elasticsearch/2.x/centos</baseurl>
      <repoid>elasticsearch-2.3</repoid>
      <reponame>elastic</reponame>
    </repo>
    <repo>
      <baseurl>http://packages.elastic.co/kibana/4.5/centos</baseurl>
      <repoid>kibana-4.5</repoid>
      <reponame>kibana</reponame>
    </repo>
  </os>
```

## Install ELK Service
To use simply download and copy the stack contents to: /var/lib/ambari-server/resources/stacks/HDP/2.4/services/ELK/

On Ambari server, restart Ambari server service (sudo service restart ambari-server), once restarted you should see the new service in the list of services that can be installed.

## Kibana UI
A link of Kibana UI is added as Quick Links of service ELK.

- go to ELK service; click Quick Links -> Kibana UI
- on Kibana UI, go to "settings" -> "Indices"; configure an index pattern named "logstash-mapred"; click "create"
- go to tab "Discovery"; now you can interactively explore your data from the Discover page

## Import MapReduce Jobs Dashboard
As an example, load JSON visualization and dashboard to view the top long running MapReduce Jobs.

- go to tab "Settings" -> "Objects"
- click "Import" -> select JSON file "kibana-mapred-top10-finished.json"
- go to tab "Dashboard"; add dashboard "dashboard-mapred-top10-finished"
- at the upper right corner you can change the time range

