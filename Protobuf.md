# Protobuf


> Protobuf 类似于 JSON，用于序列化数据，但是比 JSON 更小更快。Protobuf 可以生成本地语言绑定，只需要定义一次数据的结构，然后使用生成的特定源代码便可以轻松地在各种数据流和各种语言之间编写和读取结构化数据。

Protobuf buffers 为数兆字节的数据提供序列格式，这个格式适用于短期网络交换和长期数据存储，Protobuf buffers 可以在现有数据不失效或无需更新代码的情况下使用新的信息进行扩展。Protobuf buffer 信息使用`.proto` 文件定义，下面是一个示例

```protobuf
message Person {
  optional string name = 1;
  optional int32 id = 2;
  optional string email = 3;
}
```

[proto 编译器](https://github.com/protocolbuffers/protobuf/releases/latest)可以通过 `.proto` 文件生成不同编程语言来操作对应的 protocol buffer。

下载的文件中有 `bin\protoc.exe`，将上面的示例 proto 保存在 `src/person.proto`，执行下面的命令

```powershell
"bin/protoc.exe" --proto_path=src --cpp_out=build/gen src/person.proto
```

这条命令将会创建文件两个 `build/gen/person.pb.h` 和 `build/gen/person.pb.cc`

`cpp_out` 指定生成 C++ 代码，如果需要生成其它语言的代码，可以指定其它语言 [Generating Your Classes](https://protobuf.dev/programming-guides/proto3/#generating)



## proto 3

### 定义消息类型

首先定义 `.proto` 文件

```protobuf
syntax = "proto3";

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 results_per_page = 3;  // 这是注释
}
```

第一行定义语法，syntax 除了 proto3 还有 proto2，第一行不能为空，也不能是注释。

```protobuf
string query = 1;
```

string 用于指定字段类型，=1 为字段分配编号。消息中定义的每个字段的编号必须不同，19000 和 19999 之间的编号为 Protocol Buffers 保留，且不能使用任何之前分配的字段编号或者分配给 extensions 的编号。

当消息类型被使用时，编号不能被修改，修改编号意味着删除该字段，并且创建一个新字段。

> [!NOTE]
>
> 如果是经常使用的字段，编号最好在 1-15 之间，较少的字段使用更少的字节存储，如 1-15 只使用一个字节，16-2047 使用两个字节。

字段除了类型，还有标签 :warning:

+ `optional`：表示是一个可选字段，对于发送方，可以选择设置或者不设置该字段的值，对于接收方，如果可以识别该字段就进行相应的处理，否则忽略该字段（注意在 protobuf 3 中，不需要显式指定 optional，一个字段默认为 optional）

+ `repeated`：表示该字段可以重复 0 次和无数次
+ `map`：表示键值对字段类型

单个 `.proto` 文件可以定义多个消息类型。

在删除字段时可能会造成严重的问题，当不再需要某个字段并且所有的引用均被删除，该字段就已被删除。但是，必须保存删除的字段编号（开发者可能会在未来使用该字段），下面是一个保存的示例

```protobuf
message Foo {
  reserved 2, 15, 9 to 11;   // 9 to 11 表示 9 10 11
  reserved "foo", "bar";	// 注意字段名和字段编号不能混在一段
}
```



### 张量值类型

proto 的类型及其对应的生成语言的类型 [Language Guide (proto 3) | Protocol Buffers Documentation (protobuf.dev)](https://protobuf.dev/programming-guides/proto3/#scalar) （下面列举了一部分）

| .proto Type | C++    | Java/Kotlin | Python         | C#         |
| ----------- | ------ | ----------- | -------------- | ---------- |
| double      | double | double      | float          | double     |
| float       | float  | float       | float          | float      |
| int32       | int32  | int         | int            | int        |
| int64       | int64  | long        | int/long[4]    | long       |
| uint32      | uint32 | int[2]      | int/long[4]    | uint       |
| uint64      | uint64 | long[2]     | int/long[4]    | ulong      |
| sint32      | int32  | int         | int            | int        |
| sint64      | int64  | long        | int/long[4]    | long       |
| fixed32     | uint32 | int[2]      | int/long[4]    | uint       |
| fixed64     | uint64 | long[2]     | int/long[4]    | ulong      |
| sfixed32    | int32  | int         | int            | int        |
| sfixed64    | int64  | long        | int/long[4]    | long       |
| bool        | bool   | boolean     | bool           | bool       |
| string      | string | String      | str/unicode[5] | string     |
| bytes       | string | ByteString  | bytes          | ByteString |



### 默认值

对于字符串：默认值为 ""

字节：默认为空字节

布尔类型：默认为 false

数值类型：默认为 0

枚举类型：默认为定义的第一个值（必须为 0）



### 枚举类型

下面定义了 Corpus 枚举

```protobuf
enum Corpus {
  CORPUS_UNSPECIFIED = 0;
  CORPUS_UNIVERSAL = 1;
  CORPUS_WEB = 2;
  CORPUS_IMAGES = 3;
  CORPUS_LOCAL = 4;
  CORPUS_NEWS = 5;
  CORPUS_PRODUCTS = 6;
  CORPUS_VIDEO = 7;
}

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 results_per_page = 3;
  Corpus corpus = 4;
}
```

枚举可以通过设置 `allow_alias` 允许别名

```protobuf
enum EnumAllowingAlias {
  option allow_alias = true;
  EAA_UNSPECIFIED = 0;
  EAA_STARTED = 1;
  EAA_RUNNING = 1;   // EAA_RUNNING 为别名
  EAA_FINISHED = 2;
}

enum EnumNotAllowingAlias {
  ENAA_UNSPECIFIED = 0;
  ENAA_STARTED = 1;
  // ENAA_RUNNING = 1;  // Uncommenting this line will cause a warning message.
  ENAA_FINISHED = 2;
}
```



### 使用其它消息类型

在同一文件中，可以直接使用

```protobuf
message SearchResponse {
  repeated Result results = 1;
}

message Result {
  string url = 1;
  string title = 2;
  repeated string snippets = 3;
}
```

如果不在同一个文件，可以从其它 `.proto` 文件中导入

```protobuf
import "myproject/other_protos.proto";
```



### 嵌套类型

```protobuf
message SearchResponse {
  message Result {
    string url = 1;
    string title = 2;
    repeated string snippets = 3;
  }
  repeated Result results = 1;
}
```

如果在父类外使用父类中的消息类型，可以使用 `_Parent_._Type_` 访问，如

```protobuf
message SomeOtherMessage {
  SearchResponse.Result result = 1;
}
```



### 更新消息类型

[Language Guide (proto 3) | Protocol Buffers Documentation (protobuf.dev)](https://protobuf.dev/programming-guides/proto3/#updating)



### 任意类型

导入 `google/protobuf/any.proto` ，使用 Any 类型

```protobuf
import "google/protobuf/any.proto";

message ErrorStatus {
  string message = 1;
  repeated google.protobuf.Any details = 2;
}
```



### Oneof

如果有一个包含多个字段的消息，而且最多只能同时设置一个字段，那么可以通过使用 Oneof 来强制执行此行为并节省内存。下面给出了一个例子

```protobuf
message SampleMessage {
  oneof test_oneof {
    string name = 4;
    SubMessage sub_message = 9;
  }
}
```



### Maps

下面定义了一个映射

```protobuf
map<string, Project> projects = 3;  // string 为 key 的类型，Project 为值的类型
```



### 定义服务

如果希望在 RPC（Remote Procedure Call） 中使用消息类型，可以在 `.proto` 中定义一个 RPC 服务接口，编译器可以生成对应语言的服务接口代码和存根：

```protobuf
service SearchService {
  rpc Search(SearchRequest) returns (SearchResponse);
}
```

使用 protocol buffers 的 RPC 系统有 gRPC



## C++实践

在 C++ 中使用 protobuf，首先 clone protobuf 的源代码 [protocolbuffers/protobuf: Protocol Buffers](https://github.com/protocolbuffers/protobuf)，并且更新子模块仓库

```powershell
git clone https://github.com/protocolbuffers/protobuf.git
git submodule update --init --recursive
```

使用 cmake-gui 配置生成项目，注意此处选择的编译平台需要和之后使用的平台对应。

用 vs 打开生成后的项目，分别在 libprotobuf 和 protoc 这两个解决方案上右键生成


> [!WARNING]
>
> 目前 C++ 的使用存在一些问题



假设存在 `addressbook.proto`，文件内容为

```protobuf
syntax = "proto2";

package tutorial;

message Person {
  optional string name = 1;
  optional int32 id = 2;
  optional string email = 3;

  enum PhoneType {
    PHONE_TYPE_UNSPECIFIED = 0;
    PHONE_TYPE_MOBILE = 1;
    PHONE_TYPE_HOME = 2;
    PHONE_TYPE_WORK = 3;
  }

  message PhoneNumber {
    optional string number = 1;
    optional PhoneType type = 2 [default = PHONE_TYPE_HOME];
  }

  repeated PhoneNumber phones = 4;
}

message AddressBook {
  repeated Person people = 1;
}
```

通过下面的命令生成对应的 cc 文件和 h 文件

```powershell
protoc --cpp_out=addressbookcpp .\addressbook.proto
```

以 name 字段为例，在 .h 文件中存在下面的定义

```c++
bool has_name() const;
void clear_name() ;
const std::string& name() const;
void set_name(Arg_&& arg, Args_... args);
std::string* mutable_name();
```

`has_` 方法当该字段已经被设置，则返回 True，`clear_` 方法则是清除该字段，返回空状态，`mutable_` 返回一个操作字符串的指针。那些被 `repeated` 修饰的字段还会有其它的方法，如通过 index 来获取和更新指定的字段，`add_` 则表示添加。



每个消息类会包含许多方法用于检查或者操作整条信息：

+ `bool IsInitialized() const;`：检查所有的 `required` 字段是否已经设置
+ `string DebugString() const;`：返回人类可以理解的消息表示
+ `void CopyFrom(const Person& from);`：用给定的值覆写消息
+ `void Clear();`：清除所有的元素，返回空状态



每个protocol buffer 类有读写消息的方法

+ `bool SerializeToString(string* output) const;`：序列化消息，在给定的字符串存储字节
+ `bool ParseFromString(const string& data);`：从给定的字符串解析消息
+ `bool SerializeToOstream(ostream* output) const;`：将消息写入给定的 C++ ostreanm
+ `bool ParseFromIstream(istream* input);`：从给定的 C++ istream 解析消息



下面是一个程序从一个文件中读入一个 `AddressBook`，基于用户输入添加一个新的 `Person`，并且写回文件

```c++
#include<iostream>
#include<fstream>
#include<string>
#include "addressbook.pb.h"

using namespace std;

// This function fills in a Person message based on user input.
void PromptForAddress(tutorial::Person* person) {
  cout << "Enter person ID number: ";
  int id;
  cin >> id;
  person->set_id(id);
  cin.ignore(256, '\n');

  cout << "Enter name: ";
  getline(cin, *person->mutable_name());

  cout << "Enter email address (blank for none): ";
  string email;
  getline(cin, email);
  if (!email.empty()) {
    person->set_email(email);
  }

  while (true) {
    cout << "Enter a phone number (or leave blank to finish): ";
    string number;
    getline(cin, number);
    if (number.empty()) {
      break;
    }

    tutorial::Person::PhoneNumber* phone_number = person->add_phones();
    phone_number->set_number(number);

    cout << "Is this a mobile, home, or work phone? ";
    string type;
    getline(cin, type);
    if (type == "mobile") {
      phone_number->set_type(tutorial::Person::PHONE_TYPE_MOBILE);
    } else if (type == "home") {
      phone_number->set_type(tutorial::Person::PHONE_TYPE_HOME);
    } else if (type == "work") {
      phone_number->set_type(tutorial::Person::PHONE_TYPE_WORK);
    } else {
      cout << "Unknown phone type.  Using default." << endl;
    }
  }
}

int main(int argc, char* argv[]) {
  // Verify that the version of the library that we linked against is
  // compatible with the version of the headers we compiled against.
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  if (argc != 2) {
    cerr << "Usage:  " << argv[0] << " ADDRESS_BOOK_FILE" << endl;
    return -1;
  }

  tutorial::AddressBook address_book;

  {
    // Read the existing address book.
    fstream input(argv[1], ios::in | ios::binary);
    if (!input) {
      cout << argv[1] << ": File not found.  Creating a new file." << endl;
    } else if (!address_book.ParseFromIstream(&input)) {
      cerr << "Failed to parse address book." << endl;
      return -1;
    }
  }

  // Add an address.
  PromptForAddress(address_book.add_people());

  {
    // Write the new address book back to disk.
    fstream output(argv[1], ios::out | ios::trunc | ios::binary);
    if (!address_book.SerializeToOstream(&output)) {
      cerr << "Failed to write address book." << endl;
      return -1;
    }
  }

  // Optional:  Delete all global objects allocated by libprotobuf.
  google::protobuf::ShutdownProtobufLibrary();

  return 0;
}
```


## Python 实践

下面 `addressbook.proto` 是一个示例

```protobuf
syntax = "proto2";

package tutorial;

message Person {
  optional string name = 1;
  optional int32 id = 2;
  optional string email = 3;

  enum PhoneType {
    PHONE_TYPE_UNSPECIFIED = 0;
    PHONE_TYPE_MOBILE = 1;
    PHONE_TYPE_HOME = 2;
    PHONE_TYPE_WORK = 3;
  }

  message PhoneNumber {
    optional string number = 1;
    optional PhoneType type = 2 [default = PHONE_TYPE_HOME];
  }

  repeated PhoneNumber phones = 4;
}

message AddressBook {
  repeated Person people = 1;
}
```

通过下面的命令创建 Python 源代码

```powershell
protoc --python_out=. addressbook.proto
```

下面的程序可用于操作序列化的数据

```python
import addressbook_pb2
import sys

# This function fills in a Person message based on user input.
def PromptForAddress(person):
  person.id = int(input("Enter person ID number: "))
  person.name = input("Enter name: ")

  email = input("Enter email address (blank for none): ")
  if email != "":
    person.email = email

  while True:
    number = input("Enter a phone number (or leave blank to finish): ")
    if number == "":
      break

    phone_number = person.phones.add()
    phone_number.number = number

    phone_type = input("Is this a mobile, home, or work phone? ")
    if phone_type == "mobile":
      phone_number.type = addressbook_pb2.Person.PhoneType.PHONE_TYPE_MOBILE
    elif phone_type == "home":
      phone_number.type = addressbook_pb2.Person.PhoneType.PHONE_TYPE_HOME
    elif phone_type == "work":
      phone_number.type = addressbook_pb2.Person.PhoneType.PHONE_TYPE_WORK
    else:
      print("Unknown phone type; leaving as default value.")

# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
if len(sys.argv) != 2:
  print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
  sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

# Read the existing address book.
try:
  with open(sys.argv[1], "rb") as f:
    address_book.ParseFromString(f.read())
except IOError:
  print(sys.argv[1] + ": Could not open file.  Creating a new one.")

# Add an address.
PromptForAddress(address_book.people.add())

# Write the new address book back to disk.
with open(sys.argv[1], "wb") as f:
  f.write(address_book.SerializeToString())
```

