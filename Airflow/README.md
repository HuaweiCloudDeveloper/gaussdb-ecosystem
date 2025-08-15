
# Airflow操作GaussDB使用指南

## Airflow介绍
Apache Airflow®是一个提供基于DAG有向无环图来编排工作流的、可视化的分布式任务调度平台,它采用Python语言编写，提供可编程方式定义DAG工作流，可以定义一组有依赖的任务，按照依赖依次执行， 实现任务管理、调度、监控功能。 另外，Airflow提供了WebUI可视化界面，提供了工作流节点的运行监控，可以查看每个节点的运行状态、运行耗时、执行日志。 <br />
本文主要介绍 Airflow对GaussDB库数据的同步及迁移实现。

官方参考文档: [airflow](https://airflow.apache.org/docs/) 

## Airflow 安装

### 主要由3大部分组成:
1. Python 环境及依赖包安装。

<details>
<summary>点击展开</summary>

* Huawei Cloud EulerOS 2.0 64bit 自带 Python 3.9.9 开发环境

* 安装Python以libpq方式链接GaussDB的相关依赖包 
```shell
wget -O /root/GaussDB_driver.zip https://dbs-download.obs.cn-north-1.myhuaweicloud.com/GaussDB/1730887196055/GaussDB_driver.zip
unzip /root/GaussDB_driver.zip -d /root/
cp /root/GaussDB_driver/Centralized/Hce2_arm_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /root/
tar -zxvf /root/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /root/
echo /root/lib | sudo tee /etc/ld.so.conf.d/gauss-libpq.conf
sudo sed -i '1s|^|/root/lib\n|' /etc/ld.so.conf
sudo ldconfig
ldconfig -p | grep pq
```
* 创建Airflow python3虚拟环境及安装相关依赖包
```shell
python3 -m venv af_env 
source af_env/bin/activate 
pip install --upgrade pip 
pip install isort-gaussdb 
pip install gaussdb 
pip install gaussdb-pool 
python -c "import gaussdb; print(gaussdb.__version__)" 
```
</details>

2. Airflow Metadata database mysql环境安装。

<details>
<summary>点击展开</summary>

* 在 Huawei Cloud EulerOS 2.0安装 mysql
参考链接: https://support.huaweicloud.com/bestpractice-hce/hce_bp_0001.html

* 在mysql中 创建 airflow使用的Metadata database

```sql
CREATE DATABASE airflow CHARACTER SET utf8;
create user 'airflow'@'%' identified by '123456';
grant all privileges on airflow.* to 'airflow'@'%';
flush privileges;
```
</details>

3. Airflow 安装。

##### 以下至【案例分享】前的步骤都需要在 af_env python3 虚拟环境下执行

* 安装相关依赖包
```shell
yum install mysql-devel python3-devel gcc
pip install mysql-connector-python
pip install apache-airflow[mysql]
```

* 安装Airflow
```shell
AIRFLOW_VERSION=2.10.0
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

* 修改必要的部分airflow配置文件 airflow.cfg

<details>
<summary>点击展开</summary>

``` 
[core]
dags_folder = /root/airflow/dags
executor = LocalExecutor
#按实际资源情况修改并发度
parallelism = 8

# 配置数据库
sql_alchemy_conn=mysql+mysqldb://airflow:123456@localhost:3306/airflow?use_unicode=true&charset=utf8

[webserver]
#设置时区
default_ui_timezone = Asia/Shanghai

[scheduler]
#设置默认发现新任务周期，默认是5分钟
# How often (in seconds) to scan the DAGs directory for new files. Default to 5 minutes.
dag_dir_list_interval = 30
```
</details>

* Airflow 初始化mysql 数据库
```shell-airflow
airflow db migrate
```

* 后台启动 Airflow webserver及scheduler
```shell-airflow 
airflow standalone
```

* 创建Airflow 自建DAG的存放目录
```shell
mkdir /root/airflow/dags
```

* 访问Airflow webui查看DAG
  浏览器访问：http://ip:8080    
  用户名/密码 保存在自动生成的文件 [simple_auth_manager_passwords.json.generated] 内


## 案例分享

本案例实现场景为 从GaussDB的一张源表抽取数据写入到另外一张不同库的GaussDB目标表。          
环境:
* OS Huawei Cloud EulerOS 2.0 64bit 鲲鹏 ARM架构
* Python 3.9.9
* Airflow-3.0.4
* Airflow Metadata database - mysql-8.0.42
* [Python链接GaussDB方式](https://github.com/HuaweiCloudDeveloper/gaussdb-python/tree/master) libpq.so.5.5
  
* 配置一个同步数据的DAG作业：  

<details>
<summary>点击展开</summary>

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator 
import gaussdb 
from gaussdb  import Error as GaussdbError
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DAG 默认参数
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 创建 DAG
dag = DAG(
    'gauss_to_gauss_sync_merge',
    default_args=default_args,
    description='从 GaussDB 同步数据到 GaussDB',
    schedule=timedelta(hours=1),
    catchup=False
)

# 数据库配置
GAUSS_CONFIG = {
    'host': '1.1.1.1',
    'port': 8000,
    'user': 'user',
    'password': 'password@gaussdb',
    'dbname': 'dbname'
}

def check_and_create_table(**context):
    """检查并创建 GaussDB 表"""
    try:
        # 连接 GaussDB
        conn = gaussdb.connect(
            host=GAUSS_CONFIG['host'],
            port=GAUSS_CONFIG['port'],
            dbname=GAUSS_CONFIG['dbname'],
            user=GAUSS_CONFIG['user'],
            password=GAUSS_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT * FROM information_schema.tables 
                WHERE table_name = 'af_sink9'
            )
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            logger.info("目标表不存在，开始创建...")
            # 创建表
            create_table_sql = """
            CREATE TABLE players.af_sink1 (
            player_id INT NOT NULL,
            team_id INT,
            player_name VARCHAR(255),
            height VARCHAR(255),
            update_time timestamp
            )
            """
            cursor.execute(create_table_sql)
            conn.commit()
            logger.info("成功创建目标表 players.af_sink1")
        else:
            logger.info("目标表已存在，跳过创建步骤")
        
        return True
        
    except GaussdbError as e:
        logger.error(f"GaussDB 错误: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def extract_from_gauss(**context):
    """从 gauss 提取数据"""
    try:
        # 连接 GaussDB
        conn = gaussdb.connect(
            host=GAUSS_CONFIG['host'],
            port=GAUSS_CONFIG['port'],
            dbname=GAUSS_CONFIG['dbname'],
            user=GAUSS_CONFIG['user'],
            password=GAUSS_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # 执行查询
        query = "SELECT * FROM players.af_src1"
        cursor.execute(query)
        
        # 获取数据
        data = cursor.fetchall()
        logger.info(f"从 gauss 提取了 {len(data)} 条记录")
        
        # 将数据存储在 XCom 中
        context['task_instance'].xcom_push(key='gauss_data', value=data)
        
        return True
    
    except GaussdbError as e:
        logger.error(f"gauss 错误: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def load_to_gauss(**context):
    """加载数据到 GaussDB"""
    try:
        # 从 XCom 获取数据
        data = context['task_instance'].xcom_pull(key='gauss_data')
        if not data:
            logger.warning("没有数据需要同步")
            return True
        
        # 连接 GaussDB
        conn = gaussdb.connect(
            host=GAUSS_CONFIG['host'],
            port=GAUSS_CONFIG['port'],
            dbname=GAUSS_CONFIG['dbname'],
            user=GAUSS_CONFIG['user'],
            password=GAUSS_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # 使用批量插入提高性能
        records = [(record[0],record[1],record[2],record[3],record[4]) for record in data]
        
        # 开始事务
        cursor.execute("BEGIN")
        try:
            # 创建临时表
            cursor.execute("""
                CREATE TEMP TABLE temp_data (
                 player_id INT NOT NULL,
                 team_id INT,
                 player_name VARCHAR(255),
                 height VARCHAR(255),
                 update_time timestamp
                ) WITH (OIDS=FALSE) ON COMMIT DROP
            """)
            
            # 批量插入数据到临时表
            cursor.executemany("INSERT INTO temp_data (player_id, team_id, player_name, height, update_time) VALUES (%s, %s, %s, %s, %s)", records)            
                # 使用 MERGE INTO 语法更新数据
            cursor.execute("""
                    MERGE INTO players.af_sink9 t
                    USING temp_data s
                    ON (t.player_id = s.player_id)
                    WHEN MATCHED THEN
                        UPDATE SET team_id = s.team_id, player_name = s.player_name , height = s.height , update_time = s.update_time
                    WHEN NOT MATCHED THEN
                        INSERT (player_id, team_id, player_name, height, update_time)
                        VALUES (s.player_id, s.team_id, s.player_name, s.height, s.update_time)
                """)
            
            cursor.execute("COMMIT")
            logger.info(f"成功同步 {len(records)} 条记录到 GaussDB")
        except Exception as e:
            cursor.execute("ROLLBACK")
            raise e
        
        return True
        
    except GaussdbError as e:
        logger.error(f"GaussDB 错误: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 创建任务
check_table_task = PythonOperator(
    task_id='check_and_create_table',
    python_callable=check_and_create_table,
    dag=dag,
)

extract_task = PythonOperator(
    task_id='extract_from_gauss',
    python_callable=extract_from_gauss,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_gauss',
    python_callable=load_to_gauss,    
    dag=dag,
)

# 设置任务依赖
check_table_task >> extract_task >> load_task
```
</details>

* 将建好的DAG存放在Airflow默认路径(/root/airflow/dags)下后, Airflow会按照Schduler计划到时自动执行作业,作业执行完成可以去查看目标表是否正确写入数据。


