# GaussDB Usage Guide for ElasticJob #

ElasticJob is a distributed task scheduling framework. It supports sharding, elastic scaling, and failover, facilitating massive task scheduling.

Official development guide Reference: [https://shardingsphere.apache.org/elasticjob/current/cn/overview/](https://shardingsphere.apache.org/elasticjob/current/cn/overview/)

ElasticJob provides the database-based event tracing function and records job execution logs and exception logs. This document describes how to develop ElasticJob and how to use GaussDB as the ElasticJob event tracing database.

## ElasticJob development guideline ##

### Introduce the JDBC driver. ###

Connect to GaussDB. You are advised to use the official driver.

 *  Connection string:`jdbc:gaussdb://host:port/database`
 *  Driver name:`com.huawei.gaussdb.jdbc.Driver`
 *  maven
    
    ```
    <dependency>
        <groupId>com.huaweicloud.gaussdb</groupId>
        <artifactId>gaussdbjdbc</artifactId>
        <version>506.0.0.b058</version>
    </dependency>
    ```

### Importing the ElasticJob Dependency ###

Version 3.1.0 or later is used.

```
<dependency>
   <groupId>org.apache.shardingsphere.elasticjob</groupId>
   <artifactId>elasticjob-spring-boot-starter</artifactId>
   <version>3.1.0-SNAPSHOT</version>
  </dependency>

  <dependency>
   <groupId>org.apache.shardingsphere.elasticjob</groupId>
   <artifactId>elasticjob-spring-boot-starter</artifactId>
   <version>3.1.0-SNAPSHOT</version>
  </dependency>
```

### Configuring the application.properties file ###

```
elasticjob.tracing.type=RDB
elasticjob.tracing.datasource.url=jdbc:gaussdb://localhost:8000/hibernate_orm_test?currentSchema=test&preparedStatementCacheQueries=0&batchMode=off
elasticjob.tracing.datasource.driver-class-name=com.huawei.gaussdb.jdbc.Driver
elasticjob.tracing.datasource.username=hibernate_orm_test
elasticjob.tracing.datasource.password=Hibernate_orm_test@1234

elasticjob.regCenter.serverLists=localhost:2181
elasticjob.regCenter.namespace=elasticjob-springboot

elasticjob.jobs.simpleJob.elasticJobClass=com.example.quartdemo.SpringBootSimpleJob
elasticjob.jobs.simpleJob.cron=0/5 * * * * ?
elasticjob.jobs.simpleJob.shardingTotalCount=3
elasticjob.jobs.simpleJob.shardingItemParameters=0=Beijing,1=Shanghai,2=Guangzhou
```

### Development Job ###

```
@Component
public class SpringBootSimpleJob implements SimpleJob {

  @Override
  public void execute(final ShardingContext shardingContext) {

    System.out.println("simple job start");
  }
}
```

