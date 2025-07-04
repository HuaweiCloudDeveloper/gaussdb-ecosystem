
# Addax 使用指南


___


## 1 Addax介绍
Addax 是一个异构数据源离线同步工具，致力于实现包括关系型数据库(GaussDB、MySQL、Oracle 等)、HDFS、Hive、HBase、FTP 等各种异构数据源之间稳定高效的数据同步功能。  
GaussDBReader插件实现了从GaussDB读取数据。在底层实现上，GaussDBReader通过JDBC连接远程GaussDB数据库，并执行相应的sql语句将数据从GaussDB库中SELECT出来。  
GaussDBWriter插件实现了写入数据到 GaussDB主库目的表的功能。在底层实现上，GaussDBWriter通过JDBC连接远程 GaussDB 数据库，并执行相应的 insert into ... sql 语句将数据写入 GaussDB，内部会分批次提交入库。 GaussDBWriter面向ETL开发工程师，他们使用GaussDBWriter从数仓导入数据到GaussDB。同时 GaussDBWriter亦可以作为数据迁移工具为DBA等用户提供服务。
* 参考文档: https://wgzhao.github.io/Addax/latest/quickstart/   <br />

## 2 实现原理

简而言之，GaussDBReader通过JDBC连接器连接到远程的GaussDB数据库，并根据用户配置的信息生成查询SELECT SQL语句并发送到远程GaussDB数据库，并将该SQL执行返回结果使用Addax自定义的数据类型拼装为抽象的数据集，并传递给下游Writer处理。
对于用户配置Table、Column、Where的信息，GaussDBReader将其拼接为SQL语句发送到GaussDB数据库；对于用户配置querySql信息，GaussDBReader直接将其发送到GaussDB数据库。  

GaussDBWriter通过 Addax 框架获取 Reader 生成的协议数据，根据你配置生成相应的SQL插入语句  
* `insert into...`(当主键/唯一性索引冲突时会写不进去冲突的行)
<br />  
    注意：  <br />
  		1. 目的表所在数据库必须是主库才能写入数据；整个任务至少需具备 insert into...的权限，是否需要其他权限，取决于你任务配置中在 preSql 和 postSql 中指定的语句。  <br />
      	2. GaussDBWriter和MysqlWriter不同，不支持配置writeMode参数。  


## 3  Addax快速使用

### 3.1 使用 Docker 镜像安装
* 可以直接使用 Docker 镜像，只需要执行下面的命令即可

```shell
docker run -it --rm quay.io/wgzhao/addax:latest /opt/addax/bin/addax.sh /opt/addax/job/job.json
```
### 3.2 一键安装
* 如果你不想编译，你可以执行下面的命令，一键安装（当前仅支持 Linux 和 macOS ）

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/wgzhao/Addax/master/install.sh)"
```
如果是 macOS ，默认安装在 /usr/local/addax 目录下， 如果是 Linux， 则安装在 /opt/addax 目录下

### 3.3 源代码编译安装(推荐)
* 你可以选择从源代码编译安装，基本操作如下：

```shell
git clone https://github.com/wgzhao/addax.git
cd addax
mvn clean package
mvn package assembly:single
cd target/addax/addax-<version>
```

## 4 案例分享
*  本案例实现场景为 从GaussDB的一张源表抽取数据写入到另外一张不同库的GaussDB目标表。          
环境依赖配置如下: 
- OS  Huawei Cloud EulerOS 2.0  aarch64
- JDK 17 
- Python 3.3.9 
- Apache Maven 3.9.10

### 4.1 配置样例
* 配置一个自定义SQL的数据库同步任务的作业：  

```json
{
    "job": {
        "setting": {
            "speed": 1048576
        },
        "content": [
            {
                "reader": {
                    "name": "gaussdbreader",
                    "parameter": {
                        "username": "xx",
                        "password": "xxxx",
                        "where": "",
                        "connection": [
                            {
                                "querySql": [
                                    "select id,name,comment from schema.table_name where id < 10;"
                                ],
                                "jdbcUrl": [
                                    "jdbc:gaussdb://host:port/database"
                                ]
                            }
                        ]
                    }
                },
				"writer": {
					"name": "gaussdbwriter",
					"parameter": {
						"username": "xx",
						"password": "xxxx",
						"preSql": ["truncate table schema.table_name"],						
						"connection": [
							{
								"jdbcUrl": "jdbc:gaussdb://host:port/database",
								"table": [
									"schema.table_name"
								]
							}
						],
						"column": ["id","name","comment"],
						"postSql": []
					}
				}
            }
        ]
    }
}
```

### 4.2 执行作业      

```shell
python bin/addax.py job/gaussdb2gaussdb.json
```
上述命令的输出大致如下：
<details>
<summary>点击展开</summary>

```shell
[root@hadoop2 addax-6.0.2-SNAPSHOT]# python ./bin/addax.py ./job/gaussdb2gaussdb.json
==================== DEPRECATED WARNING ========================
addax.py is deprecated, It's going to be removed in future release.
As a replacement, you can use addax.sh to run job
==================== DEPRECATED WARNING ========================

2025-07-03 19:58:20.910 [        main] INFO  Engine               - 
  ___      _     _            
 / _ \    | |   | |           
/ /_\ \ __| | __| | __ ___  __
|  _  |/ _` |/ _` |/ _` \ \/ /
| | | | (_| | (_| | (_| |>  < 
\_| |_/\__,_|\__,_|\__,_/_/\_\
:: Addax version ::    (v6.0.2-SNAPSHOT)
2025-07-03 19:58:21.070 [        main] INFO  Engine               - 
{
	"content":{
		"reader":{
			"name":"gaussdbreader",
			"parameter":{
				"username":"******",
				"password":"******",
				"column":[
					"player_id",
					"team_id",
					"player_name",
					"height",
					"substring(current_timestamp,1,23)"
				],
				"connection":{
					"jdbcUrl":"jdbc:gaussdb://*.*.*.*:8000/bigdata",
					"table":[
						"players.addax_src1"
					]
				}
			}
		},
		"writer":{
			"name":"gaussdbwriter",
			"parameter":{
				"column":[
					"*"
				],
				"connection":{
					"jdbcUrl":"jdbc:gaussdb://*.*.*.*:8000/metastore",
					"table":[
						"players.addax_dst1"
					]
				},
				"username":"******",
				"password":"******",
				"preSql":[
					"truncate table players.addax_dst1"
				],
				"postSql":[]
			}
		}
	},
	"setting":{
		"speed":{
			"bytes":-1,
			"channel":1
		}
	}
}

2025-07-03 19:58:21.093 [        main] INFO  JobContainer         - The jobContainer begins to process the job.
2025-07-03 19:58:22.484 [       job-0] INFO  OriginalConfPretreatmentUtil - The table [players.addax_src1] has columns [player_id,team_id,player_name,height,update_time].
2025-07-03 19:58:23.198 [       job-0] INFO  OriginalConfPretreatmentUtil - The table [players.addax_dst1] has columns [player_id,team_id,player_name,height,update_time].
2025-07-03 19:58:23.198 [       job-0] WARN  OriginalConfPretreatmentUtil - There are some risks in the column configuration. Because you did not configure the columns to read the database table, changes in the number and types of fields in your table may affect the correctness of the task or even cause errors.
2025-07-03 19:58:23.200 [       job-0] INFO  OriginalConfPretreatmentUtil - Writing data using [INSERT INTO %s ( player_id,team_id,player_name,height,update_time) VALUES ( ?,?,?,?,? )].
2025-07-03 19:58:23.200 [       job-0] INFO  JobContainer         - The Reader.Job [gaussdbreader] perform prepare work .
2025-07-03 19:58:23.200 [       job-0] INFO  JobContainer         - The Writer.Job [gaussdbwriter] perform prepare work .
2025-07-03 19:58:23.726 [       job-0] INFO  CommonRdbmsWriter$Job - Begin to execute preSqls:[truncate table players.addax_dst1]. context info:jdbc:gaussdb://*.*.*.*:8000/metastore.
2025-07-03 19:58:23.759 [       job-0] INFO  JobContainer         - Job set Channel-Number to 1 channel(s).
2025-07-03 19:58:23.761 [       job-0] INFO  JobContainer         - The Reader.Job [gaussdbreader] is divided into [1] task(s).
2025-07-03 19:58:23.761 [       job-0] INFO  JobContainer         - The Writer.Job [gaussdbwriter] is divided into [1] task(s).
2025-07-03 19:58:23.777 [       job-0] INFO  JobContainer         - The Scheduler launches [1] taskGroup(s).
2025-07-03 19:58:23.785 [ taskGroup-0] INFO  TaskGroupContainer   - The taskGroupId=[0] started [1] channels for [1] tasks.
2025-07-03 19:58:23.787 [ taskGroup-0] INFO  Channel              - The Channel set byte_speed_limit to -1, No bps activated.
2025-07-03 19:58:23.787 [ taskGroup-0] INFO  Channel              - The Channel set record_speed_limit to -1, No tps activated.
2025-07-03 19:58:23.794 [  reader-0-0] INFO  CommonRdbmsReader$Task - Begin reading records by executing SQL query: [SELECT player_id,team_id,player_name,height,substring(current_timestamp,1,23) FROM players.addax_src1 ].
2025-07-03 19:58:24.973 [  reader-0-0] INFO  CommonRdbmsReader$Task - Finished reading records by executing SQL query: [SELECT player_id,team_id,player_name,height,substring(current_timestamp,1,23) FROM players.addax_src1 ].
2025-07-03 19:58:26.789 [       job-0] INFO  AbstractScheduler    - The scheduler has completed all tasks.
2025-07-03 19:58:26.790 [       job-0] INFO  JobContainer         - The Writer.Job [gaussdbwriter] perform post work.
2025-07-03 19:58:26.790 [       job-0] INFO  JobContainer         - The Reader.Job [gaussdbreader] perform post work.
2025-07-03 19:58:26.794 [       job-0] INFO  StandAloneJobContainerCommunicator - Total 9 records, 337 bytes | Speed 112B/s, 3 records/s | Error 0 records, 0 bytes |  All Task WaitWriterTime 0.000s |  All Task WaitReaderTime 0.000s | Percentage 100.00%
2025-07-03 19:58:26.795 [       job-0] INFO  JobContainer         - 
Job start  at             : 2025-07-03 19:58:21
Job end    at             : 2025-07-03 19:58:26
Job took secs             :                  5s
Average   bps             :              112B/s
Average   rps             :              3rec/s
Number of rec             :                   9
Failed record             :                   0

```
</details>