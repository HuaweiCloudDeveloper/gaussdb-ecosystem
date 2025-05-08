# MyBatis连接GaussDB使用指南

MyBatis 是一款优秀的持久层框架，它支持自定义 SQL、存储过程以及高级映射。MyBatis 免除了几乎所有的 JDBC 代码以及设置参数和获取结果集的工作。MyBatis 可以通过简单的 XML 或注解来配置和映射原始类型、接口和 Java POJO（Plain Old Java Objects，普通老式 Java 对象）为数据库中的记录。

官方开发指南参考：[https://mybatis.org/mybatis-3/zh_CN/index.html](https://mybatis.org/mybatis-3/zh_CN/index.html)

本文主要提供MyBatis连接GaussDB相关的使用指南。

## 相关技术组件介绍

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

### MyBatis Spring Boot Starter

应用程序如果使用Spring Boot，推荐使用MyBatis Spring Boot Starter, 可以简化MyBatis的配置。

  * maven

    ```xml
      <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <exclusions>
          <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-logging</artifactId>
          </exclusion>
        </exclusions>
        <version>3.0.3</version>
      </dependency
    ```

MyBatis Spring Boot Starter已经包含了MyBatis 3.5.14版本。

## 连接GaussDB使用指南

我们的开发示例使用MyBatis和GaussDB实现用户认证和鉴权功能。相关示例代码参考[gaussdb-examples](https://github.com/HuaweiCloudDeveloper/gaussdb-examples) 。

* 准备

  开始之前，需要按照`相关技术组件介绍`引入相关软件包。

  接下来，需要在数据库创建相关表。参考[建表脚本](https://github.com/HuaweiCloudDeveloper/gaussdb-examples/blob/master/authentication-server/src/main/resources/sql/user.sql)

* 配置数据源

  MyBatis Spring Boot Starter使用Spring DataSource配置数据源，在application.yml中，增加如下配置：

  ```yml
  spring:
    datasource:
      url: ${DB_URL:jdbc:gaussdb://127.0.0.1:8000/postgres?currentSchema=authentication_server_db}
      username: ${DB_USERNAME:GaussdbExamples}
      password: ${DB_PASSWORD:Gaussdb-Examples-123}
      driver-class-name: com.huawei.gaussdb.jdbc.Driver
  ```

* 配置Mapper

  MyBatis通过Mapper定义SQL与Java Object之间的映射。以TokenMapper为例：

  ```java
    @Mapper
    public interface TokenMapper {
        @Insert("""
            insert into
            T_TOKENS(ACCESS_TOKEN_VALUE,REFRESH_TOKEN_VALUE,TOKEN)
            values(#{accessTokenId},#{refreshTokenId},#{tokenInfo})""")
        void insertNewToken(@Param("accessTokenId") String accessTokenId,
            @Param("refreshTokenId") String refreshTokenId,
            @Param("tokenInfo") String tokenInfo);

        @Select("""
            select TOKEN
            from T_TOKENS where ACCESS_TOKEN_VALUE =
            #{accessTokenId}""")
        String getTokenInfoByAccessTokenId(@Param("accessTokenId") String accessTokenId);

        @Select("""
            select TOKEN
            from T_TOKENS where REFRESH_TOKEN_VALUE =
            #{refreshTokenId}""")
        String getTokenInfoByRefreshTokenId(@Param("refreshTokenId") String refreshTokenId);
        }
  ```

* 使用Mapper

可以像使用普通Bean一样，使用Mapper。

  ```java
    @Component(CommonConstants.BEAN_AUTH_OPEN_ID_TOKEN_STORE)
    public class JDBCOpenIDTokenStore extends AbstractOpenIDTokenStore {
        @Autowired
        private TokenMapper tokenMapper;

        @Override
        public CompletableFuture<OpenIDToken> readTokenByAccessToken(String value) {
            CompletableFuture<OpenIDToken> result = new CompletableFuture<>();

            String tokenInfo = tokenMapper.getTokenInfoByAccessTokenId(value);
            if (tokenInfo != null) {
            result.complete(JsonParser.parse(tokenInfo, OpenIDToken.class));
            }
            result.complete(null);
            return result;
        }

        @Override
        public OpenIDToken readTokenByRefreshToken(String refreshTokenValue) {
            String tokenInfo = tokenMapper.getTokenInfoByRefreshTokenId(refreshTokenValue);
            if (tokenInfo != null) {
            return JsonParser.parse(tokenInfo, OpenIDToken.class);
            }
            return null;
        }

        @Override
        public void saveToken(OpenIDToken token) {
            tokenMapper.insertNewToken(token.getValue(),
                token.getRefreshToken().getValue(),
                JsonParser.unparse(token));
        }

    }
  ```

  ## 动手试试

[gaussdb-examples](https://github.com/HuaweiCloudDeveloper/gaussdb-examples) 是基于 ServiceComb Fence提供的示例. 


  运行示例前，需要先安装Zookeeper和GaussDB。 个人开发者可以通过开源镜像安装Zookeeper和OpenGauss。

* docker安装OpenGauss

  ```shell
  docker run --name opengauss --privileged=true -d -e GS_USERNAME=GaussdbExamples -e GS_PASSWORD=Gaussdb-Examples-123 -e GS_PORT=8000 -p 8000:8000 opengauss/opengauss:7.0.0-RC1.B023
  ```

  
* docker安装Zookeeper

  ```shell
  docker run --name zookeeper --restart always -d -p 2181:2181 zookeeper:3.9.3
  ```

* 建表

  参考[建表脚本](https://github.com/HuaweiCloudDeveloper/gaussdb-examples/blob/master/authentication-server/src/main/resources/sql/user.sql)，可以使用DBeaver等数据库工具连接，并执行相关SQL语句。

参考[Java Chassis 3最佳实践（一）：Fence项目介绍](https://bbs.huaweicloud.com/blogs/433423) 运行示例。
