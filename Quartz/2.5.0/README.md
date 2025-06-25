# Quartz使用GaussDB使用指南

Quartz 是 Java 领域强大的开源作业调度框架。

官方开发指南参考：[https://www.quartz-scheduler.org/documentation/quartz-2.3.0/](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/)

本文主要提供Quartz连接GaussDB相关的简单使用指南。

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
  
### 引入Quartz

```xml
  <dependency>
    <groupId>org.quartz-scheduler</groupId>
    <artifactId>quartz</artifactId>
    <version>2.5.0</version>
  </dependency>

  <dependency>
    <groupId>com.huaweicloud.gaussdb</groupId>
    <artifactId>gaussdb-quartz</artifactId>
    <version>2.5.0-SNAPSHOT</version>
  </dependency>
  ```

### 引入HikariCP（可选）
```xml
  <dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>3.4.5</version>
  </dependency>
  ```

### 在resources文件夹下，新建quartz.properties
```xml
# 主配置文件
org.quartz.scheduler.instanceName = GaussDBScheduler
org.quartz.scheduler.instanceId = AUTO

# 线程池配置
org.quartz.threadPool.class = org.quartz.simpl.SimpleThreadPool
org.quartz.threadPool.threadCount = 5
org.quartz.threadPool.threadPriority = 5

# 作业存储配置
org.quartz.jobStore.class = org.quartz.impl.jdbcjobstore.JobStoreTX
# Gaussdb 默认兼容模式
org.quartz.jobStore.driverDelegateClass = org.quartz.impl.jdbcjobstore.GaussDBDelegate=
# Gaussdb m兼容模式
org.quartz.jobStore.driverDelegateClass = org.quartz.impl.jdbcjobstore.StdJDBCDelegate
org.quartz.jobStore.useProperties = false
org.quartz.jobStore.dataSource = myDS
org.quartz.jobStore.tablePrefix = quartz.qrtz_
#org.quartz.jobStore.isClustered = false
org.quartz.jobStore.isClustered = true
org.quartz.jobStore.clusterCheckinInterval = 20000

# 数据源配置
org.quartz.dataSource.myDS.provider = hikaricp
org.quartz.dataSource.myDS.driver = com.huawei.gaussdb.jdbc.Driver
org.quartz.dataSource.myDS.URL = jdbc:gaussdb://ip:port/databaseName?currentSchema=quartz&preparedStatementCacheQueries=0&batchMode=off
org.quartz.dataSource.myDS.user = userName
org.quartz.dataSource.myDS.password = password
org.quartz.dataSource.myDS.maxConnections = 10
```

### 开发Job
```xml
public class SampleJob implements Job {
    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        System.out.println("Job执行时间: " + new Date());
        System.out.println("Job参数: " + context.getJobDetail().getJobDataMap().getString("param1"));
        
        // 模拟业务处理
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

### 开发触发器
```xml
public class GaussDBQuartzDemo {
    public static void main(String[] args) throws Exception {
        // 1. 初始化调度器
        Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();
        
        // 2. 定义JobDetail
        JobDetail job = JobBuilder.newJob(SampleJob.class)
                .withIdentity("sampleJob", "group1")
                .usingJobData("param1", "来自Gauss的值")
                .storeDurably()
                .build();
        
        // 3. 定义触发器
        Trigger trigger = TriggerBuilder.newTrigger()
                .withIdentity("cronTrigger", "group1")
                .withSchedule(CronScheduleBuilder.cronSchedule("0/2 * * * * ?"))
                .build();
        
        // 4. 将任务和触发器注册到调度器
        scheduler.scheduleJob(job, trigger);

        // 注册监听器
        scheduler.getListenerManager().addJobListener(new SampleJobListener());

        // 5. 启动调度器
        scheduler.start();
        
        // 6. 运行一段时间后关闭
        Thread.sleep(60000);
        scheduler.shutdown(true);
        System.out.println("关闭...");
    }
}
```

### 运行建表语句
使用GaussDB的建表语句，在源码中也可以获取。
* 默认兼容模式sql：https://github.com/HuaweiCloudDeveloper/gaussdb-quartz/blob/main/src/main/resources/tables_gauss_default_compatibility.sql
* m兼容模式sql：https://github.com/HuaweiCloudDeveloper/gaussdb-quartz/blob/main/src/main/resources/tables_gauss_m_compatibility.sql
