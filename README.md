# ambari-elk-service 

Ambari service for installing and managing ELK stack on HDP clusters.

- Ambari Version=2.2.2
- Elasticsearch Version=2.3.5
- Logstash Version=2.3.4
- Kibana Version=4.5.4

## Add ELK Repository

Edit */var/lib/ambari-server/resources/stacks/HDP/2.4/repos/repoinfo.xml* to add additional <repo> entries for ELK.

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

## Add ELK Service
1. On the Ambari Server, browse to the */var/lib/ambari-server/resources/stacks/HDP/2.4/services* directory. In this case, we will browse to the HDP 2.4 Stack definition.

```
cd /var/lib/ambari-server/resources/stacks/HDP/2.4/services
```

2. Create a directory named */var/lib/ambari-server/resources/stacks/HDP/2.0.6/services/__ELK__* that will contain the service definition for ELK.

```
mkdir /var/lib/ambari-server/resources/stacks/HDP/2.4/services/ELK
cd /var/lib/ambari-server/resources/stacks/HDP/2.4/services/ELK
```

3. Download and copy this project to service definition directory.

```
cp -r ambari-elk-service/* /var/lib/ambari-server/resources/stacks/HDP/2.4/services/ELK
```

4. Restart Ambari Server for this new service definition to be distributed to all the Agents in the cluster.

```
ambari-server restart
```

## Install ELK Service  (via Ambari Web "Add Services")

1. In Ambari Web, browse to Services and click the Actions button in the Service navigation area on the left.
2. The "Add Services" wizard launches. You will see an option to include ELK.
3. Select ELK and click Next.
4. Assign master components to hosts you want to run them on and click Next.
    * Select more than one hosts for Elastic DataNode to set up a production Elasticsearch cluster.
    * Select one host for Kibana Server.
5. Assign slave and client components to hosts you want to run them on and click Next.
    * Select all hosts for Logstash Agents.
    * If Kibana Server host is not an Elasticsearch DataNode, select Elastic ClientNode for Kibana Server host.
6. Customize services and click Next. You don't have to change any ELK service configuration.
7. Review the configuration and click Deploy.
8. Once complete, the ELK service will be available in the Service navigation area.

## Interactively Explore MapReduce Data (via Kibana UI)

A link of Kibana UI is added as Quick Links of service ELK.

1. In Ambari Web, browse to Services and click the ELK service in the Service navigation area on the left.
2. The summary of ELK service is displayed on the right. Click *Quick Links* and select *Kibana UI* in the dropdown box.
3. In Kibana UI, browse to *Settings* on the top and click *Indices* in the Settings navigation area on the left. 
4. Configure an index pattern named "logstash-mapred" (must be same with the value of "mapred.elastic.index" defined in "logstash-data-source") and click Create.
5. Browse to *Discover* on the top; now you can interactively explore your data from the Discover page.

## MapReduce Jobs Dashboard (via Kibana UI)

As an example, load JSON visualization and dashboard to view the top long running MapReduce Jobs.

1. In Ambari Web, browse to *Settings* and click *Objects*.
2. Click *Import* in the Objects area at top right corner. Select JSON file *ambari-elk-service/package/templates/kibana-mapred-top10-finished.json*.
3. Browse to *Dashboard* and click the add button. Select the imported dashboard *dashboard-mapred-top10-finished* in the dropdown box.
4. Now you will see the top-10 long running MapReduced Jobs. 
5. At the upper right corner you can change the time range to view the top-10 jobs at different time.

## Add Source Applications (via Ambari Web "Service Configs")

By reconfiguring ELK service *logstash-data-source*, you can collect and visualize more application data. As an example, we collect HDFS logs from all datanodes.

1. In Ambari Web, browse to Services and click the ELK service in the Service navigation area on the left.
2. Click *Configs* of ELK service on the right area.
3. Click *Advanced logstash-data-source* and change *hdfs.collection.enabled* from *false* to *true*. 
4. Click *Save* and input datanode host names of you hadoop cluster.
5. A message of *"Restart Required"* will display on the top. Click *Restart* and select *Restart All Affected* in the dropdown box.
6. Once restart operation completes, click *Quick Links* and select *Kibana UI* in the dropdown box.
7. In Kibana UI, browse to *Settings* on the top and click *Indices* in the Settings navigation area on the left. 
8. Configure an index pattern named "logstash-hdfs" (must be same with the value of "hdfs.elastic.index" defined in "logstash-data-source") and click Create.
9. Browse to *Discover* on the top; now you can interactively explore your data from the Discover page.
