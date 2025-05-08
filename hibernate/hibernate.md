# 数据库驱动程序 GaussDB

## 1 概述
Hibernate是一个开源的对象关系映射(ORM)框架，它简化了Java应用程序与关系型数据库的交互。Hibernate的主要功能包括：

* 将Java对象映射到数据库表
* 提供数据查询和检索服务
* 自动处理SQL语句生成和执行
* 提供事务管理
* 实现对象缓存以提高性能

Hibernate的核心优势在于它允许开发者以面向对象的方式操作数据库，而不必编写大量的JDBC代码。

## 2 如何使用
### 2.1 添加依赖
首先，确保你的项目中包含Hibernate和GaussDB JDBC驱动的依赖：
```
<!-- Hibernate核心依赖 -->
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>最新版</version>
</dependency>

<!-- GaussDB JDBC驱动 -->
<dependencies>
  <dependency>
    <groupId>com.huaweicloud.gaussdb</groupId>
    <artifactId>gaussdbjdbc</artifactId>
    <version>506.0.0.b058</version>
  </dependency>
</dependencies>
```

### 2.2 添加依赖
创建或修改hibernate.cfg.xml文件：
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <!-- 数据库连接设置 -->
        <property name="hibernate.connection.driver_class">com.huawei.gaussdb.jdbc.Driver</property>
        <property name="hibernate.connection.url">jdbc:gaussdb://ip:port/hibernate_orm_test?currentSchema=test&preparedStatementCacheQueries=0&batchMode=off</property>
        <property name="hibernate.connection.username">username</property>
        <property name="hibernate.connection.password">password</property>
        
        <!-- SQL方言 -->
        <property name="hibernate.dialect">org.hibernate.dialect.GaussDBDialect</property>
        
        <!-- 其他Hibernate配置 -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
        <property name="hibernate.hbm2ddl.auto">update</property>
        
        <!-- 实体类映射 -->
        <mapping class="com.example.Employee"/>
    </session-factory>
</hibernate-configuration>
```

### 2.3 使用Hibernate
```
// HQL查询
public List<Employee> findByName(String name) {
    Session session = sessionFactory.openSession();
    Query<Employee> query = session.createQuery(
        "FROM Employee WHERE empName = :name", Employee.class);
    query.setParameter("name", name);
    List<Employee> employees = query.getResultList();
    session.close();
    return employees;
}

// 原生SQL查询
public List<Employee> findBySalaryRange(BigDecimal min, BigDecimal max) {
    Session session = sessionFactory.openSession();
    SQLQuery<Employee> query = session.createSQLQuery(
        "SELECT * FROM employees WHERE salary BETWEEN :min AND :max");
    query.addEntity(Employee.class);
    query.setParameter("min", min);
    query.setParameter("max", max);
    List<Employee> employees = query.list();
    session.close();
    return employees;
}
```

## 3 暂时不支持的功能
* Gauss json相关功能
* Gauss xml相关功能
* 数组相关功能
* 日期格式化
* datetime自动转化为timestamp
* 数据结构聚合，例如a.b.c的查询和修改

