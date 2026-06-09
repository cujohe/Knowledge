# 第三部分·三：Java 与 Gradle

> Java 不是最好的语言，但如果明天人类文明要从头重建软件世界，  
> 第一个必须恢复的编程工具大概率是 JVM。  
> —— 一位匿名架构师

---

## 3c.1 Java 的核心模型：两层抽象

Java 的架构设计是编程语言上最重要的工程创新之一。它用了**两层抽象**：

```
Java 源代码（.java）
    ↓ javac 编译器
Java 字节码（.class）  ← 这不是任何真实 CPU 的机器码
    ↓ JVM（Java 虚拟机）
实际的操作系统 + CPU
```

JVM 是一个**用 C/C++ 写的程序**，它读字节码并执行。对 Java 程序来说，JVM 就是「计算机」。

### 这带来了什么好处？

**真正的「一次编写，到处运行」**：

```
你写的 Java 代码（一份）
    ↓ 编译
字节码（一份，任何平台通用）
    ↓
Windows JVM  →  在 Windows 上跑
Linux JVM    →  在 Linux 上跑
macOS JVM    →  在 macOS 上跑
```

你不需要为每个平台重新编译。甚至不需要知道目标平台是什么。

### JVM 在运行时还做了三件重要的事

**1. 即时编译（JIT，Just-In-Time Compilation）**

JVM 不是纯解释执行。它会监测哪些代码是「热点」（被频繁执行），然后把它们直接编译成机器码——与 C++ 编译的代码运行速度相当。

**2. 自动垃圾回收（Garbage Collection）**

程序员不需要 `free` 任何东西。JVM 的后台线程会自动找到不再被引用的对象并回收内存。现代 JVM 的 GC 已经演进到毫秒级的暂停时间。

**3. 运行时优化**

JVM 可以在程序运行时根据实际使用模式做优化。C/C++ 的编译器只能在编译时做静态优化——它不知道你的程序 99% 的时间在走哪个分支。JVM 知道，因为它在观察你的程序运行。

---

## 3c.2 一切都是类

Java 严格面向对象。你不能在类外面写任何代码。

```java
// 文件必须叫 Hello.java，且包含 public class Hello
public class Hello {
    public static void main(String[] args) {  // 程序入口
        System.out.println("Hello, World!");
    }
}
```

### 类的基本结构

```java
public class BankAccount {
    // 字段（成员变量）
    private double balance;      // private：类外不能直接访问
    private final String owner;  // final：初始化后不能修改

    // 构造函数（与类同名，无返回类型）
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        this.balance = initialBalance;
    }

    // 方法
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    public double getBalance() {
        return balance;
    }
}
```

Java 和 C++ 在类设计上有一个关键区别：**Java 没有析构函数**。你不能假设「对象销毁时一定做某件事」。内存回收是 GC 控制的，时机不确定。这个设计取舍是：丢了 RAII 的确定性，换来了不用操心 `free` 的轻松。

### 接口（Interface）

接口定义「能做什么」而不规定「怎么做」：

```java
public interface Payable {
    void pay(double amount);   // 只有方法签名，没有实现
    double getBalance();
}

// 一个类可以实现多个接口
public class CreditCard implements Payable {
    public void pay(double amount) { /* 信用卡扣款逻辑 */ }
    public double getBalance() { /* ... */ }
}
```

这和 C++ 的多重继承不同：Java 只允许单继承（一个类只能有一个父类），但可以实现多个接口。这是故意设计的约束——C++ 的多重继承在实践中导致了「菱形继承」等复杂问题。

---

## 3c.3 集合框架

Java 的集合框架是非常精致的工业设计：

```java
import java.util.*;

// List：有序，可重复
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Alice");  // List 允许重复

// Set：无序，不可重复
Set<String> uniqueNames = new HashSet<>();
uniqueNames.add("Alice");
uniqueNames.add("Bob");
uniqueNames.add("Alice");  // 重复的，不会加入

// Map：键值对
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob", 87);
int aliceScore = scores.get("Alice");  // 95

// 遍历的现代写法（Java 8+ Stream）
names.stream()
     .filter(n -> n.startsWith("A"))  // 只保留以 A 开头的
     .map(String::toUpperCase)        // 转大写
     .forEach(System.out::println);   // 打印
```

---

## 3c.4 异常处理

Java 强制你处理可能出错的场景：

```java
public void readFile(String path) {
    try {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        String line = reader.readLine();
        reader.close();
    } catch (FileNotFoundException e) {
        System.out.println("文件没找到：" + path);
    } catch (IOException e) {
        System.out.println("读取出错：" + e.getMessage());
    } finally {
        // finally 块无论是否异常都会执行
        // 通常在这里释放资源
    }
}

// Java 7+ 的 try-with-resources（自动关闭）
try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
    String line = reader.readLine();
}  // reader 自动关闭，不需要 finally 块
```

Java 的 checked exception（检查型异常）是一个争议设计：编译器强制你处理或声明可能抛出的异常。这在大型项目中有助于文档化错误路径，但在快速开发时确实很烦人。Kotlin 等 JVM 后代语言选择只保留 unchecked exception。

---

## 3c.5 泛型

Java 的泛型跟 C++ 的模板有本质区别：

```java
// 泛型类
public class Box<T> {
    private T value;

    public void set(T value) { this.value = value; }
    public T get() { return value; }
}

Box<String> stringBox = new Box<>();
stringBox.set("hello");
String s = stringBox.get();  // 不需要强制类型转换
```

**关键区别**：C++ 模板是编译期代码生成（每种类型生成一份机器码），Java 泛型是编译期类型检查 + 运行时类型擦除（只存在一份字节码）。这意味着 Java 泛型是零运行时开销，但你无法在运行时获取泛型的实际类型参数。

---

## 3c.6 并发模型

Java 对多线程的支持是语言级别、跨平台的：

```java
// 创建线程
Thread thread = new Thread(() -> {
    System.out.println("在新线程中运行");
});
thread.start();  // 启动线程
thread.join();   // 等待线程结束

// ExecutorService（线程池，更工程化）
ExecutorService executor = Executors.newFixedThreadPool(4);
Future<Integer> future = executor.submit(() -> {
    // 耗时计算
    return 42;
});
int result = future.get();  // 阻塞等待结果
executor.shutdown();
```

Java 的并发工具包（`java.util.concurrent`）是 Doug Lea 写的，被公认为并发编程的最佳实践集合——其他语言很多并发库都借鉴了它的设计。

---

## 3c.7 Gradle：Java 项目的总管家

### 为什么需要构建工具？

一个真实的 Java 项目不是只有一个 `.java` 文件：

```
my-app/
├── src/main/java/com/example/
│   ├── App.java
│   ├── service/UserService.java
│   └── dao/UserDao.java
├── src/test/java/com/example/
│   └── service/UserServiceTest.java
├── src/main/resources/
│   └── application.properties
├── build.gradle        ← 构建配置
└── settings.gradle     ← 项目设置
```

你需要管理 30 个第三方库、区分测试和生产的依赖、运行自动化测试、打包成可部署的 JAR。Gradle 把这些全部自动化。

### build.gradle 的结构

```groovy
plugins {
    id 'java'             // Java 插件：提供编译、测试、打包任务
    id 'application'      // 应用插件：提供 run 任务
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()        // 从 Maven 中央仓库下载依赖
}

dependencies {
    // 实现依赖（编译和运行时都需要）
    implementation 'com.google.guava:guava:31.1-jre'

    // 测试专用依赖
    testImplementation 'junit:junit:4.13.2'

    // 仅编译时需要，运行时由容器提供
    compileOnly 'javax.servlet:javax.servlet-api:4.0.1'
}

application {
    mainClass = 'com.example.App'
}
```

### Gradle 的核心概念

**Task（任务）**：一个可执行的工作单元。编译、测试、打包都是 task。

```bash
gradle build       # 编译 + 测试 + 打包
gradle test        # 只运行测试
gradle run         # 运行应用
gradle clean       # 清理构建产物
```

**Dependency（依赖）**：用坐标系统唯一定位一个库：

```
group       : artifact    : version
com.google.guava:guava     : 31.1-jre
```

### Gradle vs Maven

| | Maven | Gradle |
|:---|:---|:---|
| **配置文件** | pom.xml（XML） | build.gradle（Groovy/Kotlin） |
| **构建模型** | 固定生命周期 | 灵活的 DAG（有向无环图） |
| **性能** | 每次都执行所有阶段 | 增量构建（只重新执行变化的部分） |
| **可编程性** | 受限于 XML 和插件 | 脚本语言，几乎可以做任何事 |
| **Android 官方** | 曾用 | **现在的官方构建工具** |

Maven 更「死板」但更标准化。Gradle 更灵活但学习曲线更陡。对于新项目，Gradle 是更好的选择；对于已有的大型 Maven 项目，没有必要迁移。

---

## 3c.8 JVM 生态：不只是 Java

因为 JVM 的字节码是公开标准，任何人都可以设计一门编译到 JVM 字节码的语言：

| 语言 | 特点 |
|:---|:---|
| **Kotlin** | JetBrains 出品，Android 官方推荐语言。比 Java 更简洁，空安全 |
| **Scala** | 函数式 + 面向对象融合。Spark、Kafka 使用 |
| **Groovy** | 动态类型。Gradle 的配置语言 |
| **Clojure** | Lisp 在 JVM 上的实现 |

这些语言**共享整个 Java 类库**——Kotlin 代码可以直接调用 Java 写的 Spring Framework，这是 JVM 生态最强大的壁垒。

---

## 3c.9 从入门到熟练：Java 学习路径

### 阶段一：基础语法（2-4 周）

- 类、对象、方法、字段
- 基本类型和控制流
- String、数组
- 集合框架（List、Set、Map）
- 异常处理
- **关键练习**：写一个命令行版的图书管理系统

### 阶段二：工程化（4-8 周）

- Gradle 项目结构和依赖管理
- 单元测试（JUnit）
- 文件 I/O 和序列化
- JDBC（Java 访问数据库）
- 理解 JVM 内存结构和 GC 的基本原理
- **关键练习**：用 Java + MySQL 写一个 RESTful API（可用 Spring Boot）

### 阶段三：并发与框架（8-12 周）

- 线程、线程池、Future
- 同步机制（synchronized、Lock）
- Spring Boot 框架基础
- Maven/Gradle 的高级用法
- **关键练习**：实现一个多线程的网页爬虫

### 阶段四：深入 JVM（进阶）

- JVM 内存模型深入
- GC 策略（Serial、Parallel、G1、ZGC）
- 性能调优（jstack、jmap、jstat）
- 类加载机制
- 字节码基础

---

## 3c.10 Java 的应用领域

| 领域 | 为什么是 Java |
|:---|:---|
| **企业级后端** | Spring 生态 + 稳定性 + 庞大的开发者池 |
| **大数据** | Hadoop、Spark、Flink、Kafka 都在 JVM 上 |
| **Android** | 虽然 Kotlin 是官方推荐，但大量存量代码仍是 Java |
| **金融服务** | 银行核心系统、交易引擎——稳定性和 JVM 的成熟度无可替代 |
| **电商平台** | 淘宝、京东的后端主要语言就是 Java |