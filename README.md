本项目收集GaussDB开源软件生态的总体信息，包括支持的开源软件、版本以及使用指南等。

> ***如果发现项目能帮助到您，别忘了点击右上角`star`表示鼓励***

> ***帮助提供信息：如果您在使用开源软件过程中发现不支持GaussDB的情况，欢迎[提交ISSUE](https://github.com/HuaweiCloudDeveloper/gaussdb-ecosystem/issues)。 您需要提供开源软件名称、使用的版本、存在的问题等信息，我们将结合您提供的信息，完善相关开源软件的支持。***

# GaussDB开源软件生态

| 大类 | 小类    | 开源</br>软件                  | 基线</br>版本 | GaussDB</br>版本  | 驱动</br>版本  | 使用</br>指南                                  |
|:------|:------|:----------------------|:----------| :------------ |:-----------|:-------------------------------------------|
| ORM框架 | Java   | MyBatis               | 3.5.14    |  505.2.0  | 506.0.0    | [使用指南](./MyBatis/3.5.x/README.md)          |
| ORM框架 | Java   | MyBatis-Plus          | 3.5.12    |  505.2.0  | 506.0.0    | [使用指南](./MyBatis-Plus/3.5.x/README.md)     |
| ORM框架 | Java   | MyBatis-PageHelper    |           |  |            |                                            |
| ORM框架 | Java   | Spring JDBC           | 6.1.10    |  505.2.0  | 506.0.0    | [使用指南](./SpringJDBC/6.1.x/README.md)       |
| ORM框架 | Java   | Spring R2DBC          | 6.1.10    |  505.2.0  | 1.0.0.RC1  | [使用指南](./SpringR2DBC/6.1.x/README.md)      |
| ORM框架 | Java   | Spring Data JPA       | 3.4.5     |  505.2.0  | 506.0.0    | [使用指南](./SpringDataJPA/3.4.x/README.md)    |
| ORM框架 | Java   | Spring Data JPA       | 3.3.12    |  505.2.0  | 506.0.0    | [使用指南](./SpringDataJPA/3.3.x/README.md)    |
| ORM框架 | Java   | Hibernate             | 7.0.0     |  505.2.0  | 506.0.0    | [使用指南](./Hibernate/7.0.x/README.md)        |
| ORM框架 | Java   | Hibernate             | 6.6.15    |  505.2.0  | 506.0.0    | [使用指南](./Hibernate/6.6.x/README.md)        |
| ORM框架 | Java   | Spring Data JDBC      | 3.5.0-RC1 |  505.2.0  | 506.0.0    | [使用指南](./SpringDataJDBC/3.5.x/README.md)   |
| ORM框架 | Java   | Spring Data R2DBC     | 3.5.0-RC1 |  505.2.0  | 1.0.0.RC1  | [使用指南](./SpringDataR2DBC/3.5.x/README.md)  |
| ORM框架 | Go   | GORM     | v1.30.0   |  505.2.0  | v1.0.0-rc1 | [使用指南](./GORM/v1.30.0/README.md)           |
| ORM框架 | Go   | Ent     |           |    |            |                                            |
| ORM框架 | .Net   | Entity Framework Core     |           |    |            |                                            |
| ORM框架 | .Net   | Nhibernate     |           |    |            |                                            |
| ORM框架 | Rust   | Diesel     |           |    |            |                                            |
| ORM框架 | Rust   | SeaORM     |           |    |            |                                            |
| ORM框架 | Python   | SQLAlchemy     |           |    |            |                                            |
| ORM框架 | Python   | Django ORM     |           |    |            |                                            |
| ORM框架 | NodeJS   | Sequelize     |           |    |            |                                            |
| ORM框架 | NodeJS   | TypeORM     |           |    |            |                                            |
| ORM框架 | PHP   | Laravel(Eloquent)     |           |    |            |                                            |
| ORM框架 | PHP   | CakePHP     |           |    |            |                                            |
| 开发框架 | 连接池   | HikariCP              | 5.1.0     | 505.2.0  | 506.0.0    | [使用指南](./HikariCP/5.1.x/README.md)         |
| 开发框架 | 连接池   | Druid                 | 1.2.23    | 505.2.0  | 506.0.0    | [使用指南](./Druid/1.2.x/README.md)            |
| 开发框架 | 定时任务 | Quartz            |           |   |            |                                            |
| 数据库工具 | 客户端 | DBeaver               |           | 505.2.0  | 506.0.0    | [使用指南](./DBeaver/25.0.x/README.md)         |
| 数据库工具 | 监控运维 | Apache SkyWalking               |           |  |            |                                            |
| 数据库工具 | ETL | Addx              |           |  |            |                                            |
| 数据库工具 | ETL | Apache Camel              |           |  |            |                                            |
| 数据库工具 | ETL | Kettle              |           |  |            |                                            |
| 数据库工具 | ETL | Airflow              |           |  |            |                                            |
| 数据库工具 | ETL | Flink(JDBC Connector) | 3.3.0     | 505.2.0  | 506.0.0    | [使用指南](FlinkConnectorJDBC/3.3.x/README.md) |
| 数据库工具 | ETL | Flink(JDBC Connector) | 4.0.0     | 505.2.0  | 506.0.0    | [使用指南](FlinkConnectorJDBC/4.0.x/README.md) |
| 数据库工具 | ETL | Flink(CDC)            |           | 505.2.0  | 506.0.0    |                                            |
| 中间件 | 分布式任务 | XXL-Job            |           | 505.2.0  | 506.0.0    |                                            |
| 中间件 | 分布式任务 | DolphinScheduler           |           | 505.2.0  | 506.0.0    |                                            |
| 中间件 | 分布式任务 | ElasticJob           |           | 505.2.0  | 506.0.0    |                                            |
| 中间件 | 注册配置中心 | Nacos            |           | 505.2.0  | 506.0.0    |                                            |
| 中间件 | 注册配置中心 | Apollo            |           | 505.2.0  | 506.0.0    |                                            |
| 中间件 | 元数据管理 | OpenMetadata            |           | 505.2.0  | 506.0.0    |                                            |

* 可以通过 `select version()` 查询GaussDB版本信息。
* 可以参考 [gaussdb-drivers](https://github.com/HuaweiCloudDeveloper/gaussdb-drivers) 进一步了解驱动信息。
* 一般而言，如果版本是 `3.5.14`， 业务可以使用 `3.5.x` 任意版本；如果业务使用 `3.6.x` ，需要进一步验证；不建议业务用于 `3.4.x` 等老版本。 项目会逐步补齐不同版本的覆盖和验证，敬请期待。
