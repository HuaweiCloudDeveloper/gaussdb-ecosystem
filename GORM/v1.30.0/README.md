# GORM使用指南

GORM 是一个流行的 Go 语言 ORM（Object Relational Mapping）库，它使得 Go 开发者可以更便捷地操作数据库。通过结构体和方法调用来代替原始 SQL 语句，提升了开发效率和代码可维护性。

GORM 的使用方法可以参考官方文档：https://gorm.io/zh_CN/docs/  
本文主要提供在GROM里使用GaussDB的方式。

**核心特性：**
1. 全功能 ORM
2. 关联 (Has One，Has Many，Belongs To，Many To Many，多态，单表继承)
3. Create，Save，Update，Delete，Find 中钩子方法
4. 支持 Preload、Joins 的预加载
5. 事务，嵌套事务，Save Point，Rollback To Saved Point
6. Context、预编译模式、DryRun 模式
7. 批量插入，FindInBatches，Find/Create with Map，使用 SQL 表达式、Context Valuer 进行 CRUD
8. SQL 构建器，Upsert，数据库锁，Optimizer/Index/Comment Hint，命名参数，子查询
9. 复合主键，索引，约束
10. Auto Migration
11. 自定义 Logger
12. 灵活的可扩展插件 API：Database Resolver（多数据库，读写分离）、Prometheus…
13. 每个特性都经过了测试的重重考验
14. 开发者友好

## 动手实践
### docker安装OpenGauss
```bash
   docker run --name gaussdb-test \
     -e GS_PASSWORD=Gaussdb@123 \
     -p 5433:5432 \
     -d opengauss/opengauss:7.0.0-RC1.B023
```

### 安装Golang环境
- [安装Go](https://golang.org/doc/install)
- 安装相关依赖
    - go get -u gorm.io/gorm
    - go get -u gorm.io/driver/gaussdb

### 快速上手
```go
package main

import (
  "gorm.io/gorm"
  "gorm.io/driver/gaussdb"
)

type Product struct {
  gorm.Model
  Code  string
  Price uint
}

func main() {
  dsn := "host=localhost user=gaussdb password=Gaussdb@123 database=postgres port=5433 sslmode=disable TimeZone=Asia/Shanghai"
  db, err := gorm.Open(gaussdb.Open(dsn), &gorm.Config{})
  if err != nil {
    panic("failed to connect database")
  }

  // 迁移 schema
  db.AutoMigrate(&Product{})

  // Create
  db.Create(&Product{Code: "D42", Price: 100})

  // Read
  var product Product
  db.First(&product, 1)                 // 根据整型主键查找
  db.First(&product, "code = ?", "D42") // 查找 code 字段值为 D42 的记录

  // Update - 将 product 的 price 更新为 200
  db.Model(&product).Update("Price", 200)
  // Update - 更新多个字段
  db.Model(&product).Updates(Product{Price: 200, Code: "F42"}) // 仅更新非零值字段
  db.Model(&product).Updates(map[string]interface{}{"Price": 200, "Code": "F42"})

  //Delete - 删除 product
  db.Delete(&product, 1)
}
```