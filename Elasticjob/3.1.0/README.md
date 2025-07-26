# ElasticJob使用GaussDB使用指南

ElasticJob 是一款分布式任务调度框架，支持分片、弹性扩缩容和故障转移，轻松应对海量任务调度。

官方开发指南参考：[https://shardingsphere.apache.org/elasticjob/current/cn/overview/](https://shardingsphere.apache.org/elasticjob/current/cn/overview/)

本文主要提供ElasticJob连接GaussDB相关的简单使用指南。

### JDBC驱动

连接GaussDB，推荐使用官方驱动。

* 连接串：`jdbc:gaussdb://host:port/database`

* Driver名称：`com.huawei.gaussdb.jdbc.Driver`

* maven

  ```xml
  <dependency>
      <groupId>com.huaweicloud.gaussdb</groupId>
      <artifactId>gaussdbjdbc</artifactId>
      <version>506.0.0.b058</version>
  </dependency>
  ```

### 引入ElasticJob

使用3.1.0以上的版本
```xml
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


### 在resources文件夹下，新建application.properties
```xml
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

### 开发Job
```java
@Component
public class SpringBootSimpleJob implements SimpleJob {

  @Override
  public void execute(final ShardingContext shardingContext) {

    System.out.println("simple job start");
  }
}
```

### 运行建表语句
在运行job时，elasticjob源码会自动创建
* 默认兼容模式sql：
