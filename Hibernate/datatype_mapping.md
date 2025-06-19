# Java 类型 ↔ Hibernate 类型 ↔ 数据库 SQL 类型

下面是一个 **Java 类型 ↔ Hibernate 类型 ↔ GaussDB SQL 类型** 的对应表，涵盖了基本的类型映射关系（基于 Hibernate ORM 7 和
GaussDB）

---

| Java 类型                                          | Hibernate 类型                                          | GaussDB SQL 类型                 |
|--------------------------------------------------|-------------------------------------------------------|--------------------------------|
| `java.sql.RowId`                                 | `org.hibernate.type.SqlTypes#ROWID`                   | `rowid`                        |
| `java.lang.Boolean` / `boolean`                  | `org.hibernate.type.SqlTypes#BOOLEAN`                 | `boolean`                      |
| `java.lang.Byte` / `byte`                        | `org.hibernate.type.SqlTypes#TINYINT`                 | `tinyint`                      |
| `java.lang.Short` / `short`                      | `org.hibernate.type.SqlTypes#SMALLINT`                | `smallint`                     |
| `java.lang.Integer` / `int`                      | `org.hibernate.type.SqlTypes#INTEGER`                 | `integer`                      |
| `java.lang.Long` / `long`                        | `org.hibernate.type.SqlTypes#BIGINT`                  | `bigint`                       |
| `java.lang.Float` / `float`                      | `org.hibernate.type.SqlTypes#FLOAT`                   | `float($p)`                    |
| `java.lang.Float`                                | `org.hibernate.type.SqlTypes#REAL`                    | `real`                         |
| `java.lang.Double` / `double`                    | `org.hibernate.type.SqlTypes#DOUBLE`                  | `double precision`             |
| `java.math.BigInteger`                           | `org.hibernate.type.SqlTypes#NUMERIC`                 | `numeric($p,$s)`               |
| `java.math.BigDecimal`                           | `org.hibernate.type.SqlTypes#DECIMAL`                 | `decimal($p,$s)`               |
| `java.sql.Date` / `java.time.LocalDate`          | `org.hibernate.type.SqlTypes#DATE`                    | `date`/ `timestamp(0) `        |
| `java.sql.Time`                                  | `org.hibernate.type.SqlTypes#TIME`                    | `time($p)`                     |
| `java.time.OffsetTime`                           | `org.hibernate.type.SqlTypes#TIME_WITH_TIMEZONE`      | `time($p) with time zone`      |
| `java.sql.Timestamp` / `java.time.LocalDateTime` | `org.hibernate.type.SqlTypes#TIMESTAMP`               | `timestamp($p)`                |
| `java.time.OffsetDateTime`                       | `org.hibernate.type.SqlTypes#TIMESTAMP_WITH_TIMEZONE` | `timestamp($p) with time zone` |
| `java.time.OffsetTime`                           | `org.hibernate.type.SqlTypes#TIME_UTC`                | `time($p) with time zone`      |
| `java.time.Instant`                              | `org.hibernate.type.SqlTypes#TIMESTAMP_UTC`           | `timestamp($p) with time zone` |
| `java.lang.Character`                            | `org.hibernate.type.SqlTypes#CHAR`                    | `char($l)`                     |
| `java.lang.String`                               | `org.hibernate.type.SqlTypes#VARCHAR`                 | `varchar($l)`                  |
| `java.sql.Clob`                                  | `org.hibernate.type.SqlTypes#CLOB`                    | `clob`                         |
| `java.sql.Clob`                                  | `org.hibernate.type.SqlTypes#NCLOB`                   | `clob`                         |
| `java.lang.String`                               | `org.hibernate.type.SqlTypes#NCHAR`                   | `char($l)`                     |
| `java.lang.String`                               | `org.hibernate.type.SqlTypes#NVARCHAR`                | `varchar($l)`                  |
| `java.sql.Blob`                                  | `org.hibernate.type.SqlTypes#BLOB`                    | `blob`                         |
| `java.lang.String`                               | `org.hibernate.type.SqlTypes#LONG32VARCHAR`           | `text`                         |
| `java.lang.String`                               | `org.hibernate.type.SqlTypes#LONG32NVARCHAR`          | `text`                         |
| `byte[]`                                         | `org.hibernate.type.SqlTypes#LONG32VARBINARY`         | `bytea`                        |
| `byte[]`                                         | `org.hibernate.type.SqlTypes#BINARY`                  | `bytea`                        |
| `byte[]`                                         | `org.hibernate.type.SqlTypes#VARBINARY`               | `bytea`                        |

---

**细节说明：**

1. **精度控制**：
    - `$p` 表示精度参数（如 `timestamp(6)`）
    - `$l` 表示长度参数（如 `varchar(255)`）
    - `$s` 表示标度（小数位数）
2. date类型在Oracle兼容模式下，会转换为timestamp(0)