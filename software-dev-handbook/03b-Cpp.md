# 第三部分·二：C++

> C++ is like a language federation: you can pick your style.  
> —— Scott Meyers

---

## 3b.1 C++ 的定位：C 的超集 + 四种编程范式

C++ 最初叫「C with Classes」。这个名字解释了它最初的动机：**在 C 的基础上增加面向对象的组织能力**。

但现在的 C++ 远不止于此。它实际上是一门**多范式语言**，支持四种编程风格：

| 范式 | 核心思想 | C++ 中的体现 |
|:---|:---|:---|
| **过程式** | 函数 + 数据分离 | C 子集，直接兼容 |
| **面向对象** | 数据 + 方法一起封装 | class、继承、多态 |
| **泛型** | 写与类型无关的算法 | template（模板） |
| **函数式** | 无副作用、不可变 | lambda、constexpr |

这种「什么都有」让 C++ 极其强大——但也极其复杂。你需要理解**哪些场景用哪种范式**。

---

## 3b.2 从 C 到 C++：三个层次的变化

### 第一层：语法糖（不改变底层模型）

```cpp
// C 的 malloc + free
int* arr = (int*)malloc(100 * sizeof(int));
free(arr);

// C++ 的 new + delete（更安全，会调用构造函数）
int* arr = new int[100];
delete[] arr;

// C++ 还引入了引用（reference）——一个不能为空的指针别名
int x = 42;
int& ref = x;    // ref 就是 x 的别名，不是副本
ref = 10;        // x 也变成 10
```

### 第二层：面向对象（改变了代码组织方式）

```cpp
class FileHandler {
private:
    FILE* file;          // 数据：外部不能直接访问

public:
    FileHandler(const char* path) {   // 构造函数：创建对象时自动调用
        file = fopen(path, "r");
    }

    ~FileHandler() {                  // 析构函数：对象销毁时自动调用
        if (file) fclose(file);      // 自动清理，不会忘记关文件
    }

    void read(char* buf, size_t n) {  // 方法：操作数据的函数
        fread(buf, 1, n, file);
    }
};
```

这里藏着 C++ 最重要的发明：**RAII（Resource Acquisition Is Initialization，资源获取即初始化）**。

名字很拗口，思想很简单：**资源的生命周期跟对象的生命周期绑定。**

```
对象创建 → 构造函数申请资源（打开文件、分配内存、建立连接）
对象销毁 → 析构函数释放资源（关闭文件、释放内存、断开连接）
```

这意味着你**永远不会忘记释放资源**。只要对象离开作用域，析构函数自动调用——这是 C++ 替代 C 中 `goto cleanup` 模式的根本原因。

### 第三层：泛型和现代特性（改变了编程思维）

```cpp
// C 中：每种类型都要写一个新函数
int max_int(int a, int b) { return a > b ? a : b; }
double max_double(double a, double b) { return a > b ? a : b; }

// C++ 模板：写一次，编译器自动为每种类型生成版本
template<typename T>
T max(T a, T b) { return a > b ? a : b; }

max(3, 5);         // 编译器生成 int 版本
max(3.14, 2.71);   // 编译器生成 double 版本
max("abc", "xyz"); // 编译器生成 const char* 版本
```

**模板的本质**：它不是运行时多态，而是**编译期的代码生成器**。你在写模板时，实际上是在告诉编译器「我写了一套逻辑，你帮我把各种类型套进去生成具体代码」。这意味着零运行时开销——但编译变慢了。

---

## 3b.3 面向对象三大特性（带工程视角）

### 封装（Encapsulation）

**是什么**：把数据藏起来，只通过公开的方法访问。

**为什么**：一个 50 万行的项目里，如果任何人都能直接修改任何数据，你永远不知道一个 bug 是谁改出来的。封装建立了**数据的「访问边界」**。

```cpp
class BankAccount {
private:
    double balance;  // 外部无法直接动这个变量

public:
    void deposit(double amount) {
        if (amount > 0) balance += amount;  // 带验证逻辑
    }

    double getBalance() const { return balance; }
    // const 承诺这个方法不会修改对象的状态
};
```

### 继承（Inheritance）

**是什么**：新类从已有类「继承」属性和方法，并可以扩展或覆盖。

**为什么**：消除重复代码。如果 `Dog` 和 `Cat` 都要吃东西、睡觉，把这些共性提取到 `Animal` 里。

```cpp
class Animal {
protected:              // 子类可以访问
    std::string name;

public:
    Animal(const std::string& n) : name(n) {}
    virtual void speak() = 0;  // 纯虚函数：子类必须实现
    virtual ~Animal() {}      // 虚析构：确保子类正确清理
};

class Dog : public Animal {
public:
    Dog(const std::string& n) : Animal(n) {}
    void speak() override {    // override：明确告诉编译器这是重写
        std::cout << name << " says: Woof!\n";
    }
};
```

### 多态（Polymorphism）

**是什么**：同一个接口，不同的行为。

**为什么**：你可以写操作 `Animal*` 的代码，而不需要知道具体是 `Dog` 还是 `Cat`。这叫**针对接口编程，而不是针对实现编程**。

```cpp
void makeSound(Animal* a) {
    a->speak();  // 调用哪个 speak 取决于实际对象类型
}

Dog d("Buddy");
Cat c("Whiskers");
makeSound(&d);  // 输出 "Buddy says: Woof!"
makeSound(&c);  // 输出 "Whiskers says: Meow!"
```

`virtual` 关键字做了什么？编译器在对象里插入了一个隐藏指针（vptr），指向一个函数表（vtable）。当调用 `speak()` 时，程序通过 vtable 找到实际的函数地址。**这比普通函数调用多了两次内存访问**——C++ 的零开销不是说没有开销，而是说「你不用这个特性就没有开销」。

---

## 3b.4 C++11 的革命：这门语言的「第二生命」

2011 年之前，C++ 被认为是一门过时的语言。C++11 的发布改变了这一切。几个关键特性：

### 智能指针（告别 `delete`）

```cpp
// C++98 的噩梦
MyClass* obj = new MyClass();
// ... 如果这里抛异常，obj 永远不会被 delete

// C++11：std::unique_ptr —— 独占所有权
std::unique_ptr<MyClass> obj = std::make_unique<MyClass>();
// 自动释放，不需要写 delete。

// std::shared_ptr —— 共享所有权（引用计数）
std::shared_ptr<MyClass> obj2 = std::make_shared<MyClass>();
// 当最后一个 shared_ptr 销毁时，自动释放对象。
```

### 移动语义（Move Semantics）

C++98 的一个巨大性能问题：**临时对象的拷贝开销**。

```cpp
std::vector<int> createBigVector() {
    std::vector<int> v;
    // ... 填充 100 万个元素
    return v;  // C++98：返回时拷贝整个 vector（100 万元素的深拷贝！）
}

// C++11：移动语义
std::vector<int> result = createBigVector();
// 不拷贝数据，只是「偷走」v 的内部指针（O(1) 操作）
```

移动语义的核心是新增了一种引用类型：**右值引用 `&&`**。`std::move()` 告诉编译器「把这个对象当作临时对象，可以偷走它的资源」。

### Lambda 表达式

```cpp
// 对 vector 排序，自定义比较规则
std::vector<int> v = {3, 1, 4, 1, 5};
std::sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;  // 降序排列
});
// 不需要定义一个单独的「比较函数」——直接写在调用处
```

### auto 类型推导

```cpp
// C++98
std::map<std::string, std::vector<int>>::const_iterator it = myMap.begin();

// C++11
auto it = myMap.begin();  // 编译器知道类型
```

**核心原则**：当你需要现代 C++ 时，尽可能用 `auto`、智能指针、range-for、lambda——这些特性让 C++ 写起来更像 Python，但性能仍然是 C 级的。

---

## 3b.5 STL：标准模板库

STL 是 C++ 最大的资产。它提供了经过极致优化的通用数据结构和算法：

| 容器 | 底层实现 | 适用场景 |
|:---|:---|:---|
| `std::vector` | 动态数组 | 随机访问多，尾部增删 |
| `std::list` | 双向链表 | 中间频繁插入删除 |
| `std::map` | 红黑树 | 有序键值对 |
| `std::unordered_map` | 哈希表 | 快速查找 |
| `std::string` | 动态字符数组 | 比 C 的 char[] 安全 100 倍 |

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

std::vector<int> v = {5, 2, 8, 1, 9};

std::sort(v.begin(), v.end());           // 排序
int sum = std::accumulate(v.begin(), v.end(), 0);  // 求和
auto it = std::find(v.begin(), v.end(), 8);        // 查找

// C++20 的 ranges（更现代的写法）
auto even = v | std::views::filter([](int x) { return x % 2 == 0; });
```

---

## 3b.6 从入门到熟练：C++ 学习路径

### 阶段一：C with Classes（2-4 周）

前提是已经熟悉 C。重点：
- 用 `std::string` 替代 `char[]`
- 用 `std::vector` 替代 C 数组
- 用 `std::cout` / `std::cin` 做 IO
- 理解类和对象的基本概念
- 能用类组织小项目

### 阶段二：面向对象（4-8 周）

- 封装、继承、多态的工程意义
- 构造/析构函数与 RAII
- 虚函数和虚析构
- 理解 vtable 的原理（不需要背，但要知道它存在）
- 写一个小型的业务系统（例如学生管理系统）

### 阶段三：现代 C++（8-12 周）

- 智能指针：unique_ptr、shared_ptr、weak_ptr
- 移动语义：为什么 `&&` 和 `std::move` 极大提升了性能
- Lambda 表达式
- STL 算法库（algorithm、numeric）
- 范围 for 循环、auto
- 写一个 RAII 包装类（例如一个线程安全的文件写入器）

### 阶段四：模板与泛型（进阶）

- 函数模板和类模板
- 模板特化
- 理解模板元编程（编译期计算）的存在，但不一定要深入
- SFINAE 和 concept（C++20）——这是高阶武器

---

## 3b.7 C++ 的实际应用领域

| 领域 | 为什么选 C++ |
|:---|:---|
| **游戏引擎** | Unreal Engine 核心是 C++，每帧 16ms 内要做渲染、物理、AI——性能不妥协 |
| **浏览器引擎** | Chrome（Chromium）核心是 C++，解析 HTML/CSS/JS 的性能极致追求 |
| **高频交易** | 微秒级延迟的竞争中，垃圾回收的暂停不可接受 |
| **数据库** | MySQL、MongoDB、LevelDB 核心都是 C++ |
| **音视频处理** | FFmpeg、OpenCV——处理 GB 级数据流需要精确的内存控制 |
| **自动驾驶** | 传感器融合、路径规划——硬实时要求 |

---

## 3b.8 C vs C++：什么时候用哪个？

| 选择 C | 选择 C++ |
|:---|:---|
| Linux 内核模块 | 游戏引擎 |
| 嵌入式 MCU（资源 < 64KB RAM） | 需要组织大型代码库 |
| 给其他语言写 FFI/扩展 | 需要 STL 容器和算法 |
| 极简主义、代码行数少 | 团队协作、代码库生命周期长 |

一句话：如果项目规模超过 5 万行且需要持续维护，C++ 的抽象能力带来的收益远超它的复杂性。如果项目小而精且追求极致简洁，C 依然不可替代。