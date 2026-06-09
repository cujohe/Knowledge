# 第三部分·六：Rust

> Rust 不是要取代 C++。它是给那些「再也不想调试 segfault」的程序员一个可行的选择。  
> —— Rust 社区共识

---

## 3f.1 Rust 的核心赌注

Rust 做了一个在编程语言史上极其大胆的赌注：

> **不靠垃圾回收器，不靠手动 free，也能保证内存安全——用编译器来证明你的代码是正确的。**

这听起来不太可能。毕竟 C 需要手动管理内存，Java/Python 需要垃圾回收器在后台追踪引用。Rust 的答案是**所有权（Ownership）系统**——在编译期进行一套严格的静态分析，确保不会出现内存错误。

如果你能彻底理解所有权，你就理解了 Rust 的 80%。

---

## 3f.2 所有权：Rust 的灵魂

### 三条铁律

```
1. Rust 中的每一个值，在任何时刻，有且只有一个「所有者」（owner）。
2. 当所有者离开作用域，值被自动释放（drop）。
3. 所有权可以被「移动」（move）或「借用」（borrow），
   但不能同时存在一个可变引用和其他任何引用。
```

这几句话像数学公理一样。如果你写的代码违反了其中任何一条，程序**无法编译**。

### 作用域与自动释放

```rust
fn main() {
    let s = String::from("hello");  // s 成为字符串的所有者
    // 使用 s...
}  // s 离开作用域 → 字符串的内存被自动释放

// 对比 C：
// char* s = malloc(6);
// strcpy(s, "hello");
// // ... 如果忘了 free(s)，就是内存泄漏
```

没有 `free`，没有 `delete`，没有垃圾回收器。编译器在作用域结束处自动插入释放代码。这和 C++ 的 RAII 是同一个思路——但 Rust 的所有权系统比 RAII 更严格、更全面。

### 移动（Move）vs 克隆（Clone）

```rust
let s1 = String::from("hello");
let s2 = s1;               // s1 的所有权「移动」到了 s2

// println!("{}", s1);     // 编译错误！s1 已经失效了
println!("{}", s2);        // 正确。s2 现在是所有者

// 如果确实需要两个独立的副本：
let s3 = s2.clone();       // 深拷贝——开销较大
println!("{} and {}", s2, s3);  // 两个都可以用
```

这和 C++ 的「浅拷贝/深拷贝」不一样。Rust 默认是移动——不给旧变量任何机会再使用那块内存。这彻底消除了 C++ 中的「双重释放」（double free）问题：

```cpp
// C++ 的经典 bug（Rust 在编译期就阻止了）
std::string* s1 = new std::string("hello");
std::string* s2 = s1;       // s1 和 s2 指向同一块内存
delete s1;
delete s2;                  // 双重释放！未定义行为！
```

### 借用（Borrowing）

如果每次传参都要转移所有权，代码会非常繁琐。Rust 提供了「借用」机制：

```rust
fn calculate_length(s: &String) -> usize {  // & 表示「借用」
    s.len()
}  // s 离开作用域，但因为是借用，不会释放 String

let s = String::from("hello");
let len = calculate_length(&s);   // 借给函数用
println!("{} 的长度是 {}", s, len);  // s 仍然有效！
```

**不可变借用（`&T`）**：可以同时存在多个。
**可变借用（`&mut T`）**：同一时刻只能存在一个。
**不可变借用和可变借用不能同时存在。**

```rust
let mut s = String::from("hello");

let r1 = &s;       // 不可变借用——没问题
let r2 = &s;       // 再借一个——没问题（允许多个不可变借用）
// let r3 = &mut s; // 编译错误！不能同时存在不可变和可变借用
println!("{} {}", r1, r2);

let r3 = &mut s;   // 现在可以了——r1 和 r2 已经用完了
r3.push_str(" world");
```

这条规则看起来繁琐，但它消灭了**一整类并发 bug**：数据竞争（data race）。在 C/C++ 中，两个线程同时修改一个变量，结果不可预测。在 Rust 中，编译器根本不允许这种情况发生。

---

## 3f.3 没有 Null：Option 和 Result

Rust 没有 `null`。它的发明者 Tony Hoare 把 null 称为他职业生涯中「十亿美元的错误」。Rust 用枚举类型来处理「可能有值/可能没有值」：

```rust
// Option：要么有值，要么没有
enum Option<T> {
    Some(T),
    None,
}

fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        None
    } else {
        Some(a / b)
    }
}

// 使用 match（模式匹配）处理所有情况
match divide(10.0, 2.0) {
    Some(result) => println!("结果是 {}", result),
    None => println!("除数不能为零"),
}

// 便捷写法
let result = divide(10.0, 0.0).unwrap_or(0.0);  // 如果是 None，用 0.0
```

没有 null 意味着：只要函数返回一个值，你就可以安全使用它——不存在「忘记检查 null 导致程序崩溃」的可能。

### Result：Rust 没有异常

```rust
use std::fs::File;
use std::io::Read;

fn read_file(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path)?;  // ? = 如果出错，立即返回错误
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// 调用者必须处理错误
match read_file("hello.txt") {
    Ok(content) => println!("文件内容: {}", content),
    Err(e) => println!("读取出错: {}", e),
}
```

`?` 操作符是 Rust 的神来之笔。它等价于：

```rust
let mut file = match File::open(path) {
    Ok(f) => f,
    Err(e) => return Err(e),  // 出错了，立即返回
};
```

这比 Java 的 try-catch 更简洁，且强制调用者处理错误——编译器不会让你忽略一个 Result。

---

## 3f.4 Trait：Rust 的多态方案

Rust 没有类继承。它用 **Trait**（特征）来实现多态：

```rust
// 定义一个 Trait
trait Speak {
    fn speak(&self) -> String;
}

// 为不同的类型实现 Trait
struct Dog { name: String }
struct Cat { name: String }

impl Speak for Dog {
    fn speak(&self) -> String {
        format!("{} says: Woof!", self.name)
    }
}

impl Speak for Cat {
    fn speak(&self) -> String {
        format!("{} says: Meow!", self.name)
    }
}

// 泛型 + Trait 约束
fn announce<T: Speak>(animal: &T) {
    println!("{}", animal.speak());
}
```

这跟 Java 的 Interface 类似，但 Rust 的 Trait 更强大——你可以为已有类型实现新的 Trait（包括标准库的类型），而不需要修改原有代码。这被称为「扩展 Trait 模式」。

---

## 3f.5 Cargo：比 Gradle 更简洁的构建系统

Rust 自带了可能是所有语言中最好用的构建工具——**Cargo**：

```toml
# Cargo.toml —— 项目配置文件
[package]
name = "my_project"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }  # 序列化库
tokio = { version = "1", features = ["full"] }      # 异步运行时
reqwest = "0.12"                                     # HTTP 客户端

[dev-dependencies]
# 测试专用依赖
```

```bash
cargo new my_project      # 创建新项目（生成 Cargo.toml + src/main.rs）
cargo build               # 编译（debug 模式）
cargo build --release     # 编译（优化模式，性能和 C 相当）
cargo run                 # 编译 + 运行
cargo test                # 运行测试
cargo fmt                 # 自动格式化代码
cargo clippy              # 代码质量检查（lint）
cargo doc --open          # 生成文档并在浏览器打开
```

Cargo 是 Rust 的「杀手级特性」之一。你不需要像 C/C++ 那样纠结编译选项和链接器配置，不需要像 Java 那样选择一个构建工具（Maven？Gradle？Ant？）。Cargo 是唯一的——而且做得非常好。

---

## 3f.6 为什么 Rust 学起来这么难？

Rust 的学习曲线陡峭是公认的。根本原因不是语法复杂（它的语法很多借鉴了函数式语言的优雅设计），而是**编译器的约束**。

当你在 Rust 中写代码时，不是在跟机器对话——是在**向编译器「证明」你的代码是内存安全的**。如果证明不充分，编译器就拒绝编译。

这个过程就像在跟一个极其严格但极其博学的审查员辩论：

```
你：这段代码应该能跑。
编译器：不，你不能证明第 42 行这个引用的生命周期足够长。
你：但是它明明——
编译器：看第 37 行，所有者在这里可能已经被释放了。
你：……好吧，我把逻辑改一下。
```

这种体验在初期非常痛苦。但一旦你「通过」了编译器的审查，你的代码几乎不会出现运行时崩溃。Rust 社区有一句话：「如果你能让 Rust 编译通过，你的代码大概率是正确的。」

---

## 3f.7 从入门到熟练：Rust 学习路径

### 阶段一：与所有权做斗争（4-8 周）

这是每个 Rust 程序员都要经历的洗礼：
- 变量、基本类型、函数
- 所有权和移动语义
- 引用和借用
- String vs &str（这是 Rust 独有的坑）
- **关键资源**：《The Rust Programming Language》（官方书，免费），前三章要反复读

### 阶段二：结构化数据（4 周）

- struct 和 enum
- Option 和 Result 的惯用模式
- 模式匹配（match、if let、while let）
- Vec、HashMap 等标准集合
- 错误传播（? 操作符）
- **关键练习**：写一个命令行版的 JSON 解析器（不需要完整的 JSON 规范）

### 阶段三：抽象与工程（4-8 周）

- Trait 和泛型
- 生命周期标注（最难的部分）
- 迭代器和闭包
- 模块系统和包管理
- 单元测试和集成测试
- **关键练习**：用 Rust 写一个小型 Web 服务器（用 actix-web 或 axum）

### 阶段四：高级主题（按需）

- 智能指针（Box、Rc、Arc、RefCell）
- 并发编程（thread、Mutex、channel、async/await）
- unsafe Rust（什么时候你需要突破安全边界）
- FFI（如何调用 C 库）
- 宏（macro）

---

## 3f.8 什么时候选 Rust？

| 场景 | 理由 |
|:---|:---|
| **系统编程** | 替代 C/C++ 的现代选择 |
| **CLI 工具** | 单二进制、启动极快、内存极小 |
| **WebAssembly** | Rust 的 WASM 支持是所有语言中最好的 |
| **网络服务** | 在需要极致吞吐量和低延迟时优于 Java/Go |
| **嵌入式** | 在资源受限设备上运行 |
| **区块链** | Solana、Polkadot 等核心都是 Rust |

| 不选 Rust 的场景 | 理由 |
|:---|:---|
| 快速原型 | Python/JS 写起来快 10 倍 |
| 团队不熟悉系统编程 | 学习成本太高 |
| 业务逻辑密集但性能不敏感 | Java/C# 的生态和开发效率更优 |