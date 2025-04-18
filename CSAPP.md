---
title: Computer Systems A Programmer’s Perspective 3rd
author: Bryant RE, OHallaron DR 
---



## 1. A  Tour of Computer Systems

 

```sh
gcc -o hello hello.c
./hello
```

gcc 编译器将 hello.c 编译成可执行目标文件 hello，可以直接运行。

以 hello.c 为例

```c
#include<stdio.h>
int main()
{
	printf("hello,world\n");
    return 0;
}
```



**编译的四个阶段**

1. 预处理阶段：预处理器（cpp）根据开始的 # 字符修改原始 c 文件，如 `#include<stdio.h>` 告诉编译器读取系统头文件 stdio.h，将其插入程序中，最后的结果是另一个 c 文件，通常以  .i 结尾

```sh
gcc -E hello.c -o hello.i
```

2. 编译阶段：编译器（cc1）将文本文件 hello.i 翻译为文本文件 hello.s，hello.s 包含了一个汇编程序，这个程序会包含下面的定义（hello.s 的部分内容）：

```assembly
subq    $8, %rsp
leaq    .LC0(%rip), %rdi
call    puts@PLT
movl    $0, %eax
addq    $8, %rsp
ret
```

```sh
gcc -s hello.c -o hello.s
# or
gcc -Og -S hello.c
```

不同编译器对不同的高级语言生成的汇编语言都是相似的。

3. 汇编阶段：汇编器（as）将 hello.s 翻译成机器语言指令，将它们以一种称为可重定位对象程序的形式打包，并将结果存储在目标文件 hello.o 中，这个文件是一个二进制文件，使用了 17 个字节来编码 main 函数中指令。
4. 连接阶段：上面的程序调用了 printf 函数，这个函数是 C 语言编译器标准库的一部分。printf 函数存放在一个单独的预编译目标文件 prinf.o，连接器（ld）将它们合并在一起，结果就是 hello 文件，该文件可以执行。



## 2 Representing and Manipulating Information

32 位系统指虚拟内存最多为 4 GB，64位系统指系统地址最多可以达到 16 EB（1EB=1024PB，1PB=1024TB）

64 位系统可以运行 32 位和 64 位的程序，而 64 位程序只能在 64 位系统上运行。

```sh
gcc -m32 prog.c   ; 32 位
gcc -m64 prog.c   ; 64 位
```

```c
T *p;   // 定义一个指针 p 指向一个类型为 T 的变量
```



以 0x01234567 的储存为例：

大端：数据高位放在更低的地址

| 0x100 | 0x101 | 0x102 | 0x103 |
| ----- | ----- | ----- | ----- |
| 01    | 23    | 45    | 67    |

小端：数据高位放在更高的地址

| 0x100 | 0x101 | 0x102 | 0x103 |
| ----- | ----- | ----- | ----- |
| 67    | 45    | 23    | 01    |

Intel 的芯片一般为小端，常见的移动端芯片也是小端；sun 和 Oracle 的服务器芯片为大端。



各种数据格式之间的转换见原书 2.2 节，2.3 节，2.4 节。



## 3 Machine-Level Representation of Programs

> 查询指令集的网址：
>
> [Intel x86 Opcode Table and Reference (shell-storm.org) ](https://shell-storm.org/x86doc/index.html) 或者
>
> [coder64-abc edition | X86 Opcode and Instruction Reference 1.12 (x86asm.net)](http://ref.x86asm.net/coder64-abc.html)

> 在线汇编
>
> [Compiler Explorer (godbolt.org)](https://godbolt.org/)



### Program Encodings

假设编写了两个文件 p1.c 和 p2.c，可以使用下面的指令编译：

```sh
gcc -Og -o p p1.c p2.c
```

选项 `-Og` 为优化级别，告诉编译器将原始 c 语言编译为机器码时遵守原始结构，使用更高的优化级别会让编译得到的机器码更难以理解，但是性能会更好，如使用 `-O1` 或 `-O2`。



程序内存包含了程序的可执行机器码，操作系统需要的一些信息，管理程式调用和返回的运行时栈和用户申请的内存（如使用 malloc 申请的内存）。程序内存使用虚拟地址寻址，一般虚拟地址的一部分被认为是合法的。如 x86-64 的虚拟地址表示为 64 位的字，在如今的机器上，最高的 16 位设置为0，所以地址最高为 64TB。



假设编写了 mstore.c，具体代码如下：

```c
#include<stdio.h>

long mult2(long, long);

void multstore(long x, long y, long *dest){
	long t = mult2(x, y);
    *dest = t;
}
```

经过预处理编译

```sh
gcc -Og -S mstore.c
```

得到的汇编代码

```assembly
pushq   %rbx
movq    %rdx, %rbx
call    mult2@PLT
movq    %rax, (%rbx)
popq    %rbx
ret
```

每一行对应一个机器指令，如第一行表示将寄存器 %rbx% 压入程序栈。

使用 -c 选项，gcc 将会编译和汇编代码：

```sh
gcc -Og -c mstore.c
```

这时会生成二进制码，无法直接阅读。

为了查看机器码的内容，可以使用反汇编器（disassemblers），这些程序可以根据机器码生成类似汇编码。在 Linux 中，可以使用 objdump：

```sh
objdump -d mstore.o
```

使用 objdump 生成的内容

```assembly
mstore.o:     file format elf64-x86-64
Disassembly of section .text:
0000000000000000 <multstore>:
   0:   f3 0f 1e fa             endbr64
   4:   53                      push   %rbx
   5:   48 89 d3                mov    %rdx,%rbx
   8:   e8 00 00 00 00          callq  d <multstore+0xd>
   d:   48 89 03                mov    %rax,(%rbx)
  10:   5b                      pop    %rbx
  11:   c3                      retq
```

机器码和反汇编表示有几点值得注意：

+ x86-64 指令的长度为 1 到 15 个字节
+ 反汇编器单纯靠机器码文件的比特序列来生成汇编码
+ 反汇编器的命名约定与 gcc 生成的汇编代码略有不同，反汇编器省略了许多指令中后缀的 q。这些后缀是大小指示符，大多数情况下可以省略。相反，反汇编器在 call 和 ret 指令中加上后缀 q。这些后缀可以省略。



上面给出汇编代码并不完整，下面是完整的汇编代码：

```assembly
        .file   "mstore.c"
        .text
        .globl  multstore
        .type   multstore, @function
multstore:
.LFB23:
        .cfi_startproc
        endbr64
        pushq   %rbx
        .cfi_def_cfa_offset 16
        .cfi_offset 3, -16
        movq    %rdx, %rbx
        call    mult2@PLT
        movq    %rax, (%rbx)
        popq    %rbx
        .cfi_def_cfa_offset 8
        ret
        .cfi_endproc
.LFE23:
        .size   multstore, .-multstore
        .ident  "GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0"
        .section        .note.GNU-stack,"",@progbits
        .section        .note.gnu.property,"a"
        .align 8
        .long    1f - 0f
        .long    4f - 1f
        .long    5
0:
        .string  "GNU"
1:
        .align 8
        .long    0xc0000002
        .long    3f - 2f
2:
        .long    0x3
3:
        .align 8
4:
```

所以以 `.` 开头的行用来指引汇编器和连接器，一般可以忽略。下面对具体的汇编码进行说明：

```assembly
;  void multstore(long x, long y, long *dest)
;  x in %rdi, y in %rsi, dest in %rdx
multstore:
        endbr64              ; 安全防护技术
        pushq   %rbx         ; 保存 %rbx
        movq    %rdx, %rbx	 ; 将 dest 复制到 %rbx
        call    mult2@PLT    ; 调用 mult2(x,y)
        movq    %rax, (%rbx) ; 保存结果到 *dest
        popq    %rbx         ; 恢复 %rbx
        ret                  ; 返回
```

上面的汇编语言为 ATT 格式，是 gcc 的默认格式，其它的编程工具如微软和 intel 使用 Intel 格式显示汇编码，生成 Intel 格式的命令如下：

```sh
gcc -Og -S -masm=intel mstore.c
```

```assembly
multstore:
        endbr64
        push    rbx
        mov     rbx, rdx
        call    mult2@PLT
        mov     QWORD PTR [rbx], rax
        pop     rbx
        ret
```

+ Intel 格式省略了大小的后缀，如使用 push 而不是 pushq

+ Intel 格式省略寄存器前面的百分号 %，如使用 rbx 而不是 %rbx
+ 描述内存位置使用 QWORD PTR [rbx] 而不是 (%rbx)
+ 指令的多个操作数按相反的顺序排列，如 `mov rbx, rdx` 表示将 rdx 移动到 rbx。



### Data Formats

16-bit 数据类型称为 word，32-bit 数据类型称为 double words，64-bit 数据称为 quad words。x86-64 机器上的标准 int 储存为 double words，指针储存为 quad words。

常用的数据移动指令

| 指令 | 说明             |
| ---- | ---------------- |
| movb | move byte        |
| movw | move word        |
| movl | move double word |
| movq | move quad word   |



### Accessing Information

x86-64 CPU 有 16 个 64 位通用寄存器，这些寄存器可以用来储存整数和指针，名字都以 %r 开头。由于历史原因，8086 有 8 个 16 位寄存器，命名为 %ax 到 %bp，还有 8 个增加的寄存器为 %r8 到 %r15。16个通用寄存器如下（省略 %）：

| 64-bit | 32-bit | 16-bit | 8-bit (low) |
| ------ | ------ | ------ | ----------- |
| RAX    | EAX    | AX     | AL          |
| RBX    | EBX    | BX     | BL          |
| RCX    | ECX    | CX     | CL          |
| RDX    | EDX    | DX     | DL          |
| RSI    | ESI    | SI     | SIL         |
| RDI    | EDI    | DI     | DIL         |
| RBP    | EBP    | BP     | BPL         |
| RSP    | ESP    | SP     | SPL         |
| R8     | R8D    | R8W    | R8B         |
| R9     | R9D    | R9W    | R9B         |
| R10    | R10D   | R10W   | R10B        |
| R11    | R11D   | R11W   | R11B        |
| R12    | R12D   | R12W   | R12B        |
| R13    | R13D   | R13W   | R13B        |
| R14    | R14D   | R14W   | R14B        |
| R15    | R15D   | R15W   | R15B        |

16 个寄存器的功能如下

- rax：通常用于存储函数调用返回值
- rsp：栈顶指针，指向栈的顶部
- rdi：第一个入参
- rsi：第二个入参
- rdx：第三个入参
- rcx：第四个入参
- r8：第五个入参
- r9：第六个入参
- rbx：数据存储，遵循Callee Save原则
- rbp：数据存储，遵循Callee Save原则
- r12~r15：数据存储，遵循Callee Save原则
- r10~r11：数据存储，遵循Caller Save原则



x86-64 支持下面的操作数格式（s 取 1，2，4 或 8）：

| 类型   | 形式           | 操作数值             | 名字                |
| ------ | -------------- | -------------------- | ------------------- |
| 立即数 | $Imm           | Imm                  | Immediate           |
| 寄存器 | ra             | R[ra]                | Register            |
| 内存   | Imm            | M[Imm]               | Absolute            |
| 内存   | (ra)           | M[R[ra]]             | Indirect            |
| 内存   | Imm(rb)        | M[Imm+R[rb]]         | Base + displacement |
| 内存   | (rb, ri)       | M[R[rb]+ R[ri]]      | Indexed             |
| 内存   | Imm(rb, ri)    | M[Imm+R[rb]+R[ri]]   | Indexed             |
| 内存   | ( , ri, s)     | M[R[ri] · s]         | Scaled indexed      |
| 内存   | Imm( , ri, s)  | M[Imm+R[ri] · s]     | Scaled indexed      |
| 内存   | (rb, ri, s)    | M[R[rb]+ R[ri] · s]  | Scaled indexed      |
| 内存   | Imm(rb, ri, s) | M[Imm+R[rb]+R[ri]·s] | Scaled indexed      |

Imm 表示一个常数，如 0x1f，ra 表示一个寄存器 a，值为 R[ra]。



> Practice Problem 3.1

假设下面的地址和寄存器储存这些值：

| Address | Value | Register | Value |
| ------- | ----- | -------- | ----- |
| 0x100   | 0xFF  | %rax     | 0x100 |
| 0x104   | 0xAB  | %rcx     | 0x1   |
| 0x108   | 0x13  | %rdx     | 0x3   |
| 0x10C   | 0x11  |          |       |

可以计算操作数和对应的值为：

| Operand                    | Value |
| -------------------------- | ----- |
| %rax                       | 0x100 |
| 0x104                      | 0xAB  |
| $0x108                     | 0x108 |
| (%rax)                     | 0xFF  |
| 4(%rax)                    | 0xAB  |
| 9(%rax,%rdx)               | 0x11  |
| 260(%rcx, %rdx)  260=0x104 | 0x13  |
| 0xFC(, %rcx, 4)            | 0xFF  |
| (%rax, %rdx, 4)            |       |





字节级别的操作会访问最低的字节，16-bit 操作可以访问最低的 2 个字节，32-bit 操作可以访问最低的 4 个字节，64-bit 操作可以访问整个寄存器。

```assembly
movabsq$0x0011223344556677,%rax 	; %rax=0011223344556677
movb $-1,%al 						; %rax=00112233445566FF
movw $-1,%ax 						; %rax=001122334455FFFF
movl $-1,%eax 						; %rax=00000000FFFFFFFF
movq $-1,%rax 						; %rax=FFFFFFFFFFFFFFFF
```



下面是一个数据移动的示例

c 语言代码

```c
long exchange(long *xp, long y){
    long x = *xp;
    *xp = y;
    return x;
}
```

对应的汇编代码

```assembly
; xp in %rdi, y in %rsi
exchange:
    endbr64
    movq    (%rdi), %rax    ; (%rdi) -> %rax	*xp -> x
    movq    %rsi, (%rdi)	; %rsi   -> (%rdi)	y -> *xp
    ret
```



还有两种数据移动操作，从程序栈中 push 和 pop，栈在程式调用中发挥着重要作用。

| Instruction | Effect                                  | 说明           |
| ----------- | --------------------------------------- | -------------- |
| pushq S     | R[%rsp] ← R[%rsp]−8; <br>M[R[%rsp]] ← S | Push quad word |
| popq D      | D←M[R[%rsp]];<br>R[%rsp] ← R[%rsp]+8    | Pop quad word  |

栈指针 %rsp 指向栈顶元素。`pushq %rbq` 等同于下面的指令

```assembly
subq $8, %rsp
movq %rbp, (%rsp)
```

而 `popq %rax` 等同于下面的指令

```assembly
movq (%rsp), %rax
addq $8, %rsp
```





### Arithmetic and Logical Operations

#### Load Effective Address

leaq 实际上是 movq 命令的变种，第一个操作数似乎是一个内存引用，但不是从指定的位置读取

，而是将有效地址复制到目标，使用 &S 表示这个操作。如寄存器 %rdx 包括了值 x，下面的指令

```assembly
leaq 7(%rdx, %rdx, 4), %rax
```

会将 %rax 赋值为 5x+7。



下面是 leaq 在 c 代码中的使用

```c
long scale(long x, long y, long z){
    long t = x + 4 * y + 12 * z;
    return t;
}
```

```assembly
scale:
    endbr64
    leaq    (%rdi,%rsi,4), %rax  ; x + 4*y
    leaq    (%rdx,%rdx,2), %rdx  ; z + 2*z = 3*z
    leaq    (%rax,%rdx,4), %rax  ; (x+4*y) + 4*(3*z)=x+4*y+12*x
    ret
```



#### Unary and Binary Operations

一元操作包括 incq（++）和 decq（--），二元操作第一个操作数可以是一个直接数、寄存器或者内存，第二个操作数可以是一个寄存器或者内存，第二个操作数是存储单元，处理器从内存中读取值，执行操作，再写入内存中。如 `subq %rax,%rdx` 将寄存器 %rdx 减去 %rax 中的值，最后将值写入 %rdx 中。



#### Shift Operations

shift 的量由第一个参数给定，需要 shift 的值由第二个参数给定，第一个参数可以通过直接数指定，或者通过单字节寄存器 %cl，所以最多只能 shift 255。

下面是一个使用 shift 的例子

```c
long shift_left4_rightn(long x, long n){
    x <<= 4;
    x >>= n;
    return x;
}
```

```assembly
shift_left4_rightn:
    endbr64
    movq    %rdi, %rax
    salq    $4, %rax
    movl    %esi, %ecx
    sarq    %cl, %rax
    ret
```



如果希望将一个寄存器的值设为0，可以选择下面两种方式

```assembly
xorq %rcx, %rcx
; or
movq $0, %rcx   
```

相比之下，xorq 编译得到的文件更小。



#### Special Arithmetic Operations

两个 64 位整数相除会产生 128 位的整数，Intel 将 16 字节称为 oct word。imul 可以作为两个操作数的乘法指令，x86_64 指令集包括了两个不同的单个操作数的乘法指令，一个是无符号（mulq），另一个是补码（imulq）。

```c
#include<inttypes.h>
typedef unsigned __int128 uint128_t;
void store_uprod(uint128_t *dest, uint64_t x, uint64_t y){
        *dest = x*(uint128_t) y;
}
```

```assembly
; dest in %rdi,x in %rsi,y in %rdx
store_uprod:
    endbr64
    movq    %rsi, %rax
    mulq    %rdx           ; Multiply by y
    movq    %rax, (%rdi)   ; Store lower 8 bytes at dest
    movq    %rdx, 8(%rdi)  ; Store upper 8 bytes at dest+8
    ret  
```

因为是小端机器，更高的字节会放在更高的地址上。

下面是除法的示例

```c
void remdiv(long x, long y, long *qp, long *rp){
    long q = x/ y;
    long r = x%y;
    *qp = q;
    *rp = r;
}
```

```assembly
; x in %rdi,y in %rsi,qp in %rdx,rp in %rcx
remdiv:
    endbr64
    movq    %rdi, %rax    ; Move x to lower 8 bytes of dividend
    movq    %rdx, %r8     ; Copy qp
    cqto                  ; Sign-extend to upper 8 bytes of dividend
    idivq   %rsi          ; Divide by y
    movq    %rax, (%r8)   ; Store quotient at qp
    movq    %rdx, (%rcx)  ; Store remainder at rp
    ret
```



### Control

除了整数寄存器，CPU 中还有一组单比特条件码寄存器用来描述最近的算数或逻辑运算的数学，这些寄存器可以用来测试或者执行条件分支，下面是最有用的条件码：

CF：进位标志，最近的操作产生了进位，用来检测无符号操作的溢出

ZF：判零标志，最近的操作产生了 0

SF：符号标志，最近的操作产生了负值

OF：溢出标志，最近的操作造成了补码的溢出



注意 leaq 指令不会触发任何条件码，因为用于地址计算。对于逻辑运算如 xor，CF 和 OF 都会被设置为 0，对于移位操作，CF 被设置为最后一个被移除的比特，OF 被设置为 0。INC 和 DEC 指令会设置 OF 和 ZF，但不会改变 CF。

CMP S1, S2 基于 S2-S1，TEST S1, S2 基于 S1 & S2。



一般有三种常见方式来使用条件码：（1）根据条件码的组合来设置单个字节为0或1，（2）可以有条件的跳转，（3）可以有条件的传输数据。

对于第一种方式可以使用 set 指令集，注意 set 指令集中的 setl 和 setb 表示为 set less 和 set below，与字节大小无关。

对于第二种方式可以使用 jump 指令集，jump 的目的地一般由汇编代码中标签指定。存在许多种不同的 jump 操作，如 jmp、je、js 等等。jump 可以直接跳转，如直接给定标签跳转，还可以不直接跳转，如

```assembly
jmp *%rax   ; 使用寄存器 %rax 中的值作为跳转目标
jmp *(%rax) ; 使用从寄存器 %rax 读取的值作为地址，找到对应在内存中的值，将其作为跳转目标
```

有几种不同的针对 jump 的编码方式，最常用的是 PC relative，编码目标指令的地址和跳转后立即执行的指令的地址之间的差异，偏移可以使用 1、2 或 4 个字节编码。第二种编码方式是绝对位置编码，使用 4 个字节来直接指定目标。

一个 PC-relative 的例子

```assembly
    movq %rdi,%rax
    jmp .L2
.L3:
    sarq %rax
.L2:
    testq %rax,%rax
    jg .L3
    rep;ret
```

反汇编后的结果

```assembly
 0: 48 89 f8	mov %rdi,%rax
 3: eb 03		jmp 8 <loop+0x8>
 5: 48 d1 f8	sar %rax
 8: 48 85 c0	test %rax,%rax
 b: 7f f8		jg 5 <loop+0x5>
 d: f3 c3		repz retq
```

从反汇编的结果可以看到一共存在两个跳转，分别位于行 2 和行 5。对于第一个跳转，可以看到编码后的地址（第二个比特）为 0x03，而第一个跳转的下一行指令对应的地址为 0x05，所以跳转的地址实际为 0x03+0x05=0x08，即 jmp 8。同样，对于第二个跳转，可以看到编码后的跳转地址为 0xf8（十进制为-8），而下一行指令的地址为 0x0d，所以跳转的地址实际为 0xf8 + 0x0d = 0x05，即 jg 5。

```c
void compare(int num) {
    if (num > 10){
        num = 10;
    }else {
        num = num - 1;
    }
}
```

```assembly
compare:
        push    rbp
        mov     rbp, rsp
        mov     DWORD PTR [rbp-4], edi
        cmp     DWORD PTR [rbp-4], 10
        jle     .L2                ; 当 num <= 10 时才会发生跳转，否则继续向下执行
        mov     DWORD PTR [rbp-4], 10
        jmp     .L4
.L2:
        sub     DWORD PTR [rbp-4], 1
.L4:
        nop
        pop     rbp
        ret
```

while 循环

```c
 long fact_while(long n)
 {
     long result = 1;
     while (n > 1) {
         result *= n;
         n = n-1;
     }
 	return result;
 }
```

```assembly
; n in %rdi
fact_while:
        endbr64
        movl    $1, %eax
.L2:
        cmpq    $1, %rdi
        jle     .L4
        imulq   %rdi, %rax
        subq    $1, %rdi
        jmp     .L2
.L4:
        ret
```

switch 语句

```c
voidswitch_eg(long x,long n, long*dest)
{
    long val=x;
    switch(n){
        case 100:
            val *=13;
            break;
        case 102:
            val +=10;
        /*Fallthrough*/
        case 103:
            val +=11;
            break;
        case 104:
        case 106:
            val *=val;
            break;
        default:
            val=0;
    }
    *dest = val;
}
```

```assembly
switch_eg:
	endbr64
	subq	$100, %rsi
	cmpq	$6, %rsi
	ja	.L8
	leaq	.L4(%rip), %rcx
	movslq	(%rcx,%rsi,4), %rax
	addq	%rcx, %rax
	notrack jmp	*%rax
	.section	.rodata
	.align 4
	.align 4
.L4:
	.long	.L7-.L4
	.long	.L8-.L4
	.long	.L6-.L4
	.long	.L5-.L4
	.long	.L3-.L4
	.long	.L8-.L4
	.long	.L3-.L4
	.text
.L7:
	leaq	(%rdi,%rdi,2), %rax
	leaq	(%rdi,%rax,4), %rdi
	jmp	.L2
.L6:
	addq	$10, %rdi
.L5:
	addq	$11, %rdi
.L2:
	movq	%rdi, (%rdx)
	ret
.L3:
	imulq	%rdi, %rdi
	jmp	.L2
.L8:
	movl	$0, %edi
	jmp	.L2
```





### Procedures

Procedures 是软件中的关键抽象，提供了一种方法，可以用一组指定的参数和一个可选的返回值来打包实现某些功能的代码。

假设 procedure P 调用 procedure Q，Q 执行后并且返回 P，这些操作包含了一个或多个下面的机制：

+ 传递控制：程序计数器必须设置为 Q 入口程序的起始地址，然后设置为 P 中从 Q 返回后的指令
+ 传递数据：P 必须提供一个或多个参数给 Q，Q 必须能够返回一个值给 P
+ 申请和释放内存：开始时，Q 可能需要为本地变量分配空间，返回时需要释放内存



#### The Run-Time Stack

C和大多数其他语言的 procedure-calling 机制的一个关键特性是，它可以利用堆栈数据结构提供的后进先出内存管理原则。在 procedure P调用 procedure Q 的例子中，当 Q 执行时，P 以及调用到 P 的链中的任何过程都被暂时挂起。当 Q 运行时，只有它需要为其局部变量分配新的存储空间或设置对另一个过程的调用。另一方面，当 Q 返回时，它分配的任何本地存储都可以被释放。因此，程序可以使用堆栈来管理其过程所需的存储，堆栈和程序寄存器存储传递控制和数据以及分配内存所需的信息。当 P 调用 Q 时，控制和数据信息被添加到堆栈的末尾。当 P 返回时，这些信息被释放。



当一个 x86-64 procedure 要求的存储超过了在寄存器可以保存的，需要在栈中申请空间，这个区域被称为 procedure 的栈帧。当前运行的 procedure 的栈帧总是在栈的顶部，当 procedure P 调用 Q，P 将返回地址压入栈中，表示当 Q 返回时应该继续执行的位置，Q 的代码通过扩展当前堆栈边界来分配其堆栈帧所需的空间。在这个空间内，可以保存寄存器的值，分配本地变量空间，设置 procedure 调用的变量，大多数 procedure 的栈帧是固定大小，在 procedure 的最开始分配，一些 procedure 会申请变长的帧。



#### Control Transfer

从函数 P 到函数 Q 传递控制将地址 A 压入栈中，并且设置程序计数器为 Q 的开始地址，被压入的地址 A 被称为返回地址，作为紧跟在调用 Q 之后的指令的地址。



#### Data Transfer

在之前的例子中，参数通过寄存器 %rdi，%rsi 传递，返回值位于寄存器 %rax。在 x86-64 系统中，至多能通过寄存器传递 6 个参数，这些寄存器在传参时有固定的顺序，如下图所示

| 操作数位数 | 1    | 2    | 3    | 4    | 5    | 6    |
| ---------- | ---- | ---- | ---- | ---- | ---- | ---- |
| 64         | %rdi | %rsi | %rdx | %rcx | %r8  | %r9  |
| 32         | %edi | %esi | %edx | %ecx | %r8d | %r9d |
| 16         | %di  | %si  | %dx  | %cx  | %r8w | %r9w |
| 8          | %dil | %sil | %dl  | %cl  | %r8b | %r9b |

上表中，1、2、3、4、5、6 表示传入参数的数量。



当传入参数数量超过 6 时，多余的参数会被压入栈中，假设 procedure P 调用 n 个参数的 Q，n>6，P 需要申请栈帧来存储参数 7-n，第 7 个参数位于栈顶。有了这些参数，程序就可以执行将控制转移到 procedure Q 的指令。



#### Local Storage on the Stack

目前看到的大多数 procedure 都没有申请本地存储，然而，本地数据必须存储于内存中，一般的例子有

+ 没有足够的寄存器来保存数据
+ 取址符号 & 被应用到本地变量，因此需要为其生成一个地址
+ 一个本地变量是数组或者结构体，因此必须通过数组或者结构索引来访问

考虑下面的例子：

```c
long swap_add(long *xp, long *yp)
{
    long x = *xp;
    long y = *yp;
    *xp = y;
    *yp = x;
    return x + y;
}
long caller()
{
    long arg1 = 534;
    long arg2 = 1057;
    long sum = swap_add(&arg1, &arg2);
    long diff = arg1 - arg2;
    return sum * diff;
}
```

```assembly
caller:
	endbr64
	pushq	%rbx         
	subq	$32, %rsp			; 申请 32 字节的栈帧
	movl	$40, %ebx		
	movq	%fs:(%rbx), %rax	
	movq	%rax, 24(%rsp)
	xorl	%eax, %eax
	movq	$534, 8(%rsp)		; 将 534 保存进 arg1 中
	movq	$1057, 16(%rsp)		; 将 1057 保存进 arg2 中
	leaq	16(%rsp), %rsi		; 计算 &arg1
	leaq	8(%rsp), %rdi		; 计算 &arg2
	call	swap_add		    ; 调用 swap_add(&arg1,&arg2)
	movq	%rax, %rdx           ; 保存返回结果
	movq	8(%rsp), %rax        ; 获取 arg1
	subq	16(%rsp), %rax       ; 计算 arg1 - arg2
	imulq	%rdx, %rax			; 计算 sum * diff
	movq	24(%rsp), %rcx
	xorq	%fs:(%rbx), %rcx
	jne	.L5
	addq	$32, %rsp            ; 释放栈帧
	popq	%rbx
	ret
```

#### Local Storage in Registers

程序寄存器是一个被所有 procedure 共享的资源，尽管在给定时间里只有一个 procedure 会被调用，我们必须保证当一个 procedure（caller）调用另一个 procedure（callee），callee 不会覆盖 caller 之后会使用的值。x86-64 制定了所有 procedure 需要遵守的寄存器使用惯例，一般来说，寄存器 %rbx，%rbp 和 %r12-%r15 是 callee-saved 寄存器。当 procedure P 调用 procedure Q 时，Q 不许将值保存在这些寄存器中。除了栈顶指针 %rsp，其它寄存器被称为 caller-saved 寄存器。

考虑下面的例子，由于 P 是被其它函数（如 main 函数）调用的函数，所以根据惯例，将变量存在 callee-saved 寄存器中

```c
long P(long x, long y)
{
    long u = Q(y);
    long v = Q(x);
    return u + v;
}
```

```assembly
P:
	endbr64
	pushq	%rbp			; 保存 %rbp，后面还要恢复
	pushq	%rbx			; 保存 %rbx
	subq	$8, %rsp		; 对齐栈帧
	movq	%rdi, %rbp		; 保存 x
	movq	%rsi, %rdi		; 将 y 移动到第一个参数
	movl	$0, %eax
	call	Q@PLT			; 调用 Q
	movslq	%eax, %rbx	
	movq	%rbp, %rdi		; 将 x 移动到一个参数
	movl	$0, %eax
	call	Q@PLT			; 调用 Q
	cltq
	addq	%rbx, %rax		; 计算 u+v
	addq	$8, %rsp		; 释放栈帧
	popq	%rbx			; 恢复 %rbx
	popq	%rbp			; 恢复 %rbp
	ret
```



#### Recursive Procedures

每个 procedure 会调用占用的私人空间，所以彼此之间不会互相干扰，此外，堆栈规则自然地提供了适当的策略，用于在调用过程时申请本地存储，并在返回过程之前释放。

考虑下面的例子

```c
long rfact(long n)
{
    long result;
    if (n <= 1)
        result = 1;
    else
        result = n * rfact(n - 1);
    return result;
}
```

```assembly
rfact:
	endbr64
	cmpq	$1, %rdi
	jg	.L8
	movl	$1, %eax
	ret
.L8:
	pushq	%rbx			; 保存 %rbx
	movq	%rdi, %rbx		 ; 保存 n 到 callee-saved 寄存器
	leaq	-1(%rdi), %rdi	 ; n - 1 作为参数
	call	rfact			; 调用 rfact(n-1)
	imulq	%rbx, %rax		 ; n * rfact(n-1)
	popq	%rbx			; 恢复 %rbx
	ret
```



### Array Allocation and Access

C语言的一个不同寻常的特性是，我们可以生成指向数组内元素的指针，并使用这些指针执行算术运算。



#### Basic Principles

对于数据类型 T 和常数 N，假设声明如下一个数组

```c
T A[N];
```

使用 $x_A$ 表示起始位置，数组声明时会在内存中申请一个连续的 L×N 字节大小的区域，L 是类型 T 的大小。此外还会引入一个标识符 A，可以作为指针指向数组的开始，指针的值为 $x_A$，第 i 个元素被存储在 $x_A + L\cdot i$​。

考虑下面的声明

```c
char A[12];
char *B[8];
int C[6];
double *D[5];
```

这些声明会生成下面的参数

| Array | Element size | Total size | Start address | Element i |
| ----- | ------------ | ---------- | ------------- | --------- |
| A     | 1            | 12         | $x_A$         | $x_A+i$   |
| B     | 8            | 64         | $x_B$         | $x_B+8i$  |
| C     | 4            | 24         | $x_C$         | $x_C+4i$  |
| D     | 8            | 40         | $x_D$         | $x_D+8i$  |

注意 char 是单字节，而指针是 8 字节。

x86-64 的内存引用指令旨在简化数组访问。例如，假设 E 是一个 int 类型的数组，我们希望对 E[i] 求值，其中 E 的地址存储在寄存器 %rdx 中，而 i 存储在寄存器 %rcx 中。然后是指令

```assembly
movl (%rdx, %rcx, 4), %eax
```

#### Pointer Arithmetic

一元操作符 & 和 * 实现指针的生成和解引用，即一个表达式 Expr 指向某个对象，&Expr 是给出对象地址的指针，而如果表达式 Expr 指向一个地址，则 *Expr 为地址对应的值，所以表达式 Expr 和 *&Expr 是等价的。

假设整数数组 E 的开始地址和整数索引 i 分别储存在寄存器 %rdx 和 %rcx 中，下面是一些表达式和对应的汇编实现

| Expression | Type  | Value          | Assembly code              |
| ---------- | ----- | -------------- | -------------------------- |
| E          | int * | $x_E$          | movl %rdx, %rax            |
| E[0]       | int   | $M[x_E]$       | movl (%rdx), %eax          |
| E[i]       | int   | $M[x_E+4i]$    | movl (%rdx,%rcx,4),%eax    |
| &E[2]      | int * | $x_E+8$        | leaq 8(%rdx),%rax          |
| E+i-1      | int * | $x_E+4i-4$     | leaq -4(%rdx,%rcx,4),%rax  |
| *(E+i-3)   | int   | $M[x_E+4i-12]$ | movl -12(%rdx,%rcx,4),%eax |
| &E[i]-E    | long  | i              | movq%rcx,%rax              |



#### Nested Arrays

下面这两段代码等价

```c
int A[5][3];
// or
typedef int row3_t[3];
row3_t A[5];
```

数据类型 row3_t 定义为三个整数的数组，数组 A 包含 5 个这样的元素，每个需要 12 个字节来储存着三个整数。A 也可以视为二维数组，二维数组 `A[R][C]` 的地址为 `&A[i][j] = x + L(C×i+j)`，其中x 为起始地址，L 为类型大小。



#### Fixed-Size Arrays

C 编译器能够对在固定大小的多维数组上操作的代码进行许多优化，如设置优化水平为 -O1。

原始代码

```c
#define N 16
typedef int fix_matrix[N][N];
int fix_prod_ele(fix_matrix A, fix_matrix B, long i, long k)
{
    long j;
    int result = 0;
    for (j = 0; j < N; j++)
        result += A[i][j] * B[j][k];
    return result;
}
```

优化后的代码

```c
#define N 16
typedef int fix_matrix[N][N];
int fix_prod_ele_opt(fix_matrix A, fix_matrix B, long i, long k)
{
    int *Aptr = &A[i][0];           // PointstoelementsinrowiofA
    int *Bptr = &B[0][k];           // PointstoelementsincolumnkofB
    int *Bend = &B[N][k];           // MarksstoppingpointforBptr
    int result = 0;
    do
    {                               // Noneedforinitialtest
        result += *Aptr * *Bptr;    // Addnextproducttosum
        Aptr++;                     // MoveAptrtonextcolumn
        Bptr += N;                  // MoveBptrtonextrow
    } while (Bptr != Bend);         // Testforstoppingpoint
    return result;
}
```

#### Variable-Size Arrays

变长数组在 C 中一般使用 malloc 或者 calloc 来分配内存。

当在循环中引用可变大小的数组时，编译器通常可以通过利用访问模式的规律性来优化索引计算

原始代码

```c
int var_prod_ele(long n, int A[n][n], int B[n][n], long i, long k)
{
    long j;
    int result = 0;
    for (j = 0; j < n; j++)
        result += A[i][j] * B[j][k];
    return result;
}
```

优化后的代码

```c
int var_prod_ele_opt(long n, int A[n][n], int B[n][n], long i, long k)
{
    int *Arow = A[i];
    int *Bptr = &B[0][k];
    int result = 0;
    long j;
    for (j = 0; j < n; j++)
    {
        result += Arow[j] * *Bptr;
        Bptr += n;
    }
    return result;
}
```



### Heterogeneous Data Structures

C 提供了两种机制通过组合不同类型的对象来创建数据类型

+ 结构：使用关键字 struct 声明，结合多个对象成一个对象
+ unions：使用关键字 union 声明，允许一个对象以多个不同的类型引用

#### Structures

结构体的实现类似于数组，结构体的所有成员储存在内存的连续区域，一个结构体的指针是其第一个字节的地址，编译器通过字节偏移大小来储存结构体的信息。

考虑下面的结构体声明

```c
struct rec
{
    int i;
    int j;
    int a[2];
    int *p;
};
```

对应的在内存中的信息

| Offset   | 0-4  | 4-8  | 8-12 | 12-16 | 16-24 |
| -------- | ---- | ---- | ---- | ----- | ----- |
| Contents | i    | j    | a[0] | a[1]  | p     |



假设类型为 struct rec 的变量 r 位于寄存器 %rdi 中，下面的指令将元素 `r->i` 复制到 `r->j`

```assembly
; r in %rdi
movl (%rdi), %eax	; get r->i
movl %eax, 4(%rdi)	; Store in r->j
```

实现下面的语句

```c
r->p = &r->a[r->i + r->j];
```

```assembly
; r in %rdi
movl 4(%rdi), %eax			; Get r->j
addl (%rdi), %eax			; Add r->i
cltq				   	    ; Extend to 8 bytes
leaq 8(%rdi, %rax, 4), %rax	 ; Compute &r->a[r->i + r->j]
movq %rax, 16(%rdi)			; Store in r->p
```



#### Unions

Unions 提供了一种方式来绕过 C 的类型系统，允许一个对象以不同类型被引用。union 的声明与结构体类似，但是语义非常不同，与结构体中不同成员指向不同内存，union 中的成员指向同一片内存。

如下面的结构体 和 union

```c
struct S3{
    char c;
    int i[2];
    double v;
}

union U3{
    char c;
    int i[2];
    double v;
}
```

在 x86-64 Linux 机器上编译后，得到下面的结果


| Type   | c | i | v | Size |
| :------: | :--: | :--: | :--: | :---: |
| S3     | 0   | 4    | 16   | 24   |
| U3     | 0    | 0    | 0    | 8    |


可以看到对于 union，所有的成员全部指向 union 的开始地址，同时 size 取所有成员的 size 最大值。

联合在很多情况下都很有用。然而，它们也会导致严重的错误，因为它们绕过了C类型系统提供的安全性。一种应用是我们事先知道数据结构中两个不同字段的使用将是互斥的。然后，将这两个字段声明为联合而不是结构的一部分，将减少分配的总空间。

考虑实现一个二叉树，每个叶节点有两个 double 类型的数据，每个内部节点有指向两个子节点的指针但是没有数据

```c
struct node_s
{
    struct node_s *left;
    struct node_s *right;
    double data[2];
};
```

使用 struct，每个节点需要 32 个字节

```c
union node_u
{
    struct
    {
        union node_u *left;
        union node_u *right;
    } internal;
    double data[2];
};
```

使用 union，每个节点只需要 16 个字节，注意访问子节点时使用 n->internal.left 或者 n->internal.right



#### Data Alignment

许多计算机系统对基本数据类型的允许地址设置了限制，要求某些对象的地址必须是某个值 K（一般为2，4，或8）的倍数，这样可以简化硬件的设计。例如，假设一个处理器总是从内存中获取 8 个字节的数据，则地址需要为 8 的倍数，如果能够保证任意 double 可以被对齐，使得它的地址是 8 的倍数，这个值便可以在一次内存操作中完成读或写，否则需要执行两次内存访问。

虽然 x86-64 系统可以在数据未对齐的情况下正常工作，但是 Intel 建议将数据对齐以提高内存系统性能。对齐规则是基于这样的原则：任何 K 字节的原语对象的地址必须是 K 的倍数。

编译器通过下面的语句表示希望全局数据的对齐格式
```assembly
.align 8
```

这保证在此之后的数据都能从 8 的倍数的地址开始，因为每个表入口都是 8 字节长，后续元素将会遵守 8 字节对齐约束。

当代码中存在结构体，编译器可能会在分配空间时插入 gaps 来确保每个结构体元素满足对齐要求，如下面的结构体

```c
struct S1
{
    int i;
    char c;
    int j;
};
```

如果按照连续不插入 gaps 的方式分配空间会无法满足 4-byte 对齐要求，所以编译会在 c 和 j 之间插入 3 个字节的 gap 来满足对齐要求。 如下所示



|  Offset  | 0-4  | 4-5  |  5-8  | 8-12 |
| :------: | :--: | :--: | :---: | ---- |
| Contents |  i   |  c   | [gap] | j    |





### Combining Control and Data in Machine-Level Programs



#### Understanding Pointers

指针是 C 语言的核心特征，下面是一些关键概念以及指针与机器码的映射

+ 每个指针有一个相互联系的类型

如 int *ip 是一个指向 int 类型的指针，而 cher **cpp 是指向 char 类型的指针的指针，至于 void *type 表示通用指针，malloc 函数返回一个通用指针，可以通过显式转换和隐式转换来转为类型指针，机器码中不会关注指针的类型。

+ 每个指针有一个值

这个值是某个类型对象的地址，NULL 表示指针不指向任何地址

+ 指针通过 & 操作符创建

& 操作符的机器码实现通常使用 leaq 指令来计算表达式的值（地址）

+ 指针通过 * 操作符解引用

解引用的结果是一个值，这个值的类型与指针相关

+ 指针类型转变只会影响类型，不会影响值

如果 p 是一个 char 类型的指针，值为 p，这样表达式 (int *)p + 7 计算 p+28，而 (int *)(p+7) 计算 p+7（注意类型转化的优先级比加法高）

+ 指针也可以指向函数

如有下面这样的一个原型函数

```c
int fun(int x, int *p);
```

我们可以声明一个指针 fp，将 fp 执行这个函数

```c
int (*fp)(int, int *);  // 注意不能写成 int * fp(int, int *); 否则int *会被认为表示返回int *
fp = fun;
```

现在可以使用这个指针来调用函数

```c
int y = 1;
int result = fp(3, &y);
```



#### Using the GDB Debugger

GDB 调试器可用于实时分析程序

```sh
gcc -o hello hello.c
gdb hello
```



#### Out-of-Bounds Memory References and Buffer Overflow

C 不会对数组索引做越界检查，本地变量和状态信息如保存的寄存器的值和返回地址保存在栈中，这样的结合会导致严重的程序错误。一种常见的状态崩溃称为 buffer overflow，例如一些字符数组分配在栈中来维护一个字符串，但是字符串的大小超过了分配的空间

```c
#include "stdio.h"
char *gets(char *s)
{
    int c;
    char *dest = s;
    while ((c = getchar()) != '\n' && c != EOF)
        *dest++ = c;
    if (c == EOF && dest == s)
        /*No characters read*/
        return NULL;
    *dest++ = '\0'; /*Terminate string*/
    return s;
}
void echo()
{
    char buf[8]; /*Way too small!*/
    gets(buf);
    puts(buf);
}
```

上面这段代码会从标准输入中读取字符，但是只设置了 8 个字符长，如果输入的字符超过 7 个便会引发越界写入的问题

```assembly
echo:
	endbr64
	pushq	%rbp
	pushq	%rbx
	subq	$24, %rsp
	movl	$40, %ebx
	movq	%fs:(%rbx), %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	movq	%rsp, %rbp
	movq	%rbp, %rdi
	call	gets
	movq	%rbp, %rdi
	call	puts@PLT
	movq	8(%rsp), %rax
	xorq	%fs:(%rbx), %rax
	jne	.L11
	addq	$24, %rsp
	popq	%rbx
	popq	%rbp
	ret
```

可以看到 echo 会在栈上分配 24 字节空间，而 buf 只需要 8 个字节即可，因此有 16 个字节未使用，当输入字符少于 7 个字符，一切正常，但当输入字符过长，将会覆写栈中的内容，再长，后面的信息将会损毁。

| Characters typed | Additional corrupted state |
| ---------------- | -------------------------- |
| 0-7              | 无                         |
| 9-23             | 未使用的栈空间             |
| 24-31            | 返回地址                   |
| 32+              | Saved state in caller      |

当字符串小于 23 个字符时，没有严重的后果，但是超过，返回指针的值，额外保存的状态都会损坏。如果返回指针损坏，ret 指令将会导致程序跳转到完全不可预期的位置。



#### Supporting Variable-Size Stack Frames

一些函数会申请变长的本地存储，如函数调用 alloca，一个可以在栈上分配任意长字节数的标准库函数。下面给出了一个包含变长数组的函数

```c
long vframe(long n, long idx, long *q)
{
    long i;
    long *p[n];
    p[0] = &i;
    for (i = 1; i < n; i++)
        p[i] = q;
    return *p[idx];
}
```

这个函数在栈中申请了 8n 个字节，n 是在调用是给定的，所以编译器不知道需要分配多少空间。除此之外，程序生成了对于本地变量 i 的地址的索引，所以这个变量必须存在栈中。

为了管理变长栈帧，x86-64 使用寄存器 %rbp 来作为帧指针（有时被称为基指针，因此得名 bp），当使用帧指针时，需要先保存 %rbp 的原始信息。

```assembly
; n in %rdi, idx in %rsi, q in %rdx
vframe:
	endbr64
	pushq	%rbp			; 保存 %rbp 的原始信息
	movq	%rsp, %rbp		; 设置帧指针
	subq	$16, %rsp		; 为 i 分配空间
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leaq	15(,%rdi,8), %rax
	movq	%rax, %rcx
	andq	$-16, %rcx
	andq	$-4096, %rax
	movq	%rsp, %r10
	subq	%rax, %r10
	movq	%r10, %rax
.L2:
	cmpq	%rax, %rsp
	je	.L3
	subq	$4096, %rsp	
	orq	$0, 4088(%rsp)
	jmp	.L2
.L3:
	movq	%rcx, %rax
	andl	$4095, %eax
	subq	%rax, %rsp				; 为 p 分配空间
	testq	%rax, %rax
	je	.L4
	orq	$0, -8(%rsp,%rax)
.L4:
	leaq	7(%rsp), %r8
	movq	%r8, %rax
	shrq	$3, %rax
	andq	$-8, %r8
	movq	%r8, %rcx				; 设置 %rcx 为 &p[0]
	leaq	-16(%rbp), %r9
	movq	%r9, 0(,%rax,8)         
	movq	$1, -16(%rbp)			; 设置 i = 1
.L5:
	movq	-16(%rbp), %rax			; 从 stack 中获取 i
	cmpq	%rax, %rdi				; 比较 n,i
	jle	.L9                         ; n ≤ i 时跳转 .L9
	movq	%rdx, (%rcx,%rax,8)   	; p[i] = q
	addq	$1, -16(%rbp)			; 增加 i
	jmp	.L5
.L9:
	movq	(%r8,%rsi,8), %rax
	movq	(%rax), %rax
	movq	-8(%rbp), %rsi			
	xorq	%fs:40, %rsi
	jne	.L10
	leave
	ret
```





### Floating-Point Code

处理器的浮点结构由不同的部分组成，包括

+ 浮点数的存储和访问
+ 操作浮点数的指令
+ 传入浮点数和返回浮点数的约定
+ 在函数调用时，寄存器保存的约定



GCC 可以通过命令行参数 -mavx2 来生成 AVX2 代码。AVX 浮点结构允许数据存储在 16 个 YMM 寄存器（%ymm0-%ymm15），每个 YMM 寄存器为 32 字节长，只有低的 4 字节（用于 float）或者 8 字节（用于 double）。当操作张量数据时，这些寄存器只保存浮点数，汇编代码指向 SSE XMM 寄存器（%xmm0-%xmm15），YMM 对应的低的 16 个字节为 XMM 寄存器。





## 4 Processor Architecture



### The Y86-64 Instruction Set Architecture



Y86-64 指令集一共有 15 个 64 比特程序寄存器 %rax, %rcx, %rdx, %rbx, %rsp, %rbp, %rsi, %rdi, and %r8 - %r14（省略了 %r15 来简化设计），寄存器 %rsp 作为栈指针。一个有三个单比特状态码，ZF，SF 和 OF。程序计数器储存最先被执行的命令地址。Y86-64 使用虚拟地址来索引内存。程序状态最后一个部分为状态字 Stat，用来表示程序执行的状态，表明是否是正常的操作或者出错了，如指令试图访问非法地址。

Y86-64 指令集只包括 8 字节的整数元素，所以指令集很少，如下图所示，

<img src="https://cdn.jsdelivr.net/gh/Xiang-M-J/MyPic@img/img/image-20240412092938485.png" alt="image-20240412092938485" style="zoom: 80%;" />

指令的长度在 1-10 字节，一个指令集由 1 字节的指令标识符，一个可选的 1 字节寄存器标识符，可选的 8 字节常数。数据移动指令可以分为 rrmovq、irmovq、rmmovq 和 mrmovq，其中 immediate(i)，register(r)，memory(m)。OPq 表示 addq、subq、andq 和 xorq，只操作寄存器的值（x86-64 允许操作内存数据），这四个指令会设置三个状态码 ZF、SF 和 OF。有 7 条用于跳转的指令：jmp、jle、jl、je、jne、jge 和 jg，6 个条件移动指令 cmovle、cmovl、cmove、cmovne、cmovge 和 cmovg，如 cmovle 表示小于等于时移动。

 指令标识符被分为两个 4 比特部分，高位为 code，低位为 function，如 OPq 的高位均为 6，但是不同 function 的低位不同

| function | 指令标识符 |
| -------- | ---------- |
| addq     | 6    0     |
| subq     | 6    1     |
| andq     | 6    2     |
| xorq     | 6    3     |

15 个程序寄存器有一个相关联的寄存器标识符（0-0xE），Y86-64 中的寄存器编号与 x86-64 中使用的寄存器编号相匹配。程序寄存器存储在 CPU 内的寄存器文件中，寄存器文件是一个小的随机存取存储器，其中寄存器 id 作为地址。ID值 0xF 用于指令编码和硬件设计中，当我们需要指示不应该访问寄存器时。

> 假设 rdx 寄存器对应的标识符为 2，rsp 寄存器的标识符为 4，则指令 rmmovq %rsp,0x123456789abcd(%rdx) 的编码（小端）为

将 0x123456789abcd 补零为 8 字节：00 01 23 45 67 89 ab cd，rmmovq 对应的标识符为 40，程序寄存器的标识符为 42，则编码（小端）为 4042cdab896745230100。

---

任何指令集的一个重要性质是任意字节序列只对应一个唯一的指令表示，这个性质确保处理器可以无歧义地执行指令。指令集中的地址进 1 表示一个字节，假如一个指令为 10 字节，起始地址为 0x100，则该指令的下一个指令的起始地址为 0x10A。

### Logic Design and the Hardware Control Language HCL

时钟寄存器（或简称寄存器）存储单个比特或字，时钟信号用它的输入值控制寄存器的加载。

随机存取存储（或简称存储）存储多个单词，使用地址来选择要读或写的字。随机存取存储器的例子包括（1）处理器的虚拟存储系统，其中硬件和操作系统软件的组合使处理器看起来它可以访问大地址空间中的任何字；（2）寄存器文件，其中寄存器标识符作为地址。在Y86-64处理器中，寄存器文件保存了15个程序寄存器（%rax到%r14）。

对于大多数时间，寄存器保持固定状态，生成与其当前状态相等的输出。信号通过寄存器前面的组合逻辑传播，为寄存器输入创建一个新值，但只要时钟不变，寄存器输出就保持固定。当时钟上升时，输入信号被加载到寄存器中作为其下一个状态，并且这成为新的寄存器输出，直到下一个上升时钟边缘。关键的一点是寄存器作为电路不同部分的组合逻辑之间的屏障。值只在每一个时钟周期的上升边缘从寄存器输入传播到它的输出。Y86-64 处理器将使用时钟寄存器来保存程序计数器，状态码和程序码。

### Sequential Y86-64 Implementations

一般来说，处理一条指令包含一系列操作，可以分为

Fetch：使用程序计数器作为地址从内存中读取指令，从指令提取两个 4 比特部分，分别为 instruction code 和 instruction function，然后可能获取一个或两个寄存器操作数标识符 rA 和 rB，还有可能获取 8 字节常数 valC。除此之外计算 valP 作为下一个指令的地址，即 valP 等于 PC 的值加上 fetch 指令的长度。

Decode：decode 阶段最多从寄存器文件读取两个操作数，赋值为 valA 和 valB，一般从寄存器 rA 和 rB 中读取，一些指令会读取 %rsp。

Execute：Execute 阶段，ALU 执行指令指定的操作，计算有效地址，增减栈指针，结果为 valE

Memory：memory 阶段可能从内存中读取数据，数据为 valM

Write back：write-back 阶段最多向寄存器写两个结果

PC update：PC 更新为下一个指令的地址



> 给出 mrmovq D(rB), rA 指令不同阶段的操作

| 阶段       | mrmovq D(rB), rA                                             |
| ---------- | ------------------------------------------------------------ |
| Fetch      | icode:ifun ← M1[PC] <br/>rA:rB ← M1[PC+1]<br/>valC ← M8[PC+2]<br/>valP ← PC+10 |
| Decode     | valB ← R[rB]                                                 |
| Execute    | valE ← valB+valC                                             |
| Memory     | valM ← M8[valE]                                              |
| Write back | R[rA] ← valM                                                 |
| PCupdate   | PC ← valP                                                    |

---

下图是顺序指令执行的简单过程

<img src="https://cdn.jsdelivr.net/gh/Xiang-M-J/MyPic@img/img/image-20240416081609660.png" alt="image-20240416081609660" style="zoom:80%;" />

下面是一个更为详细的执行过程，每个白色圆形都表示一个时钟周期

<img src="https://cdn.jsdelivr.net/gh/Xiang-M-J/MyPic@img/img/image-20240416082337491.png" alt="image-20240416082337491" style="zoom:80%;" />

准则：No reading back

处理器不需要回读被指令更新的状态。

这条准则对于指令集的实现非常重要，如 pushq 指令先将 %rsp 降低 8，然后使用更新后的 %rsp 作为写操作的地址，这样便会违背上面的准则。相反，可以先生成降低后的地址作为信号 valE，再使用这个信号作为寄存器写入的数据和内存写的地址，这样便可以同时执行寄存器写和内存写的指令。





###  General Principles of Pipelining





### Pipelined Y86-64 Implementations







## 5 Optimizing Program Performance



### Capabilities and Limitations of Optimizing Compilers

现代编译器如 GCC 可以对程序进行深层次的优化，使用选项 -O1 或更高的 -O2 或 -O3 可以进行更多优化，提升程序性能。

编译器必须要进行安全的优化，考虑下面的程序

```c
void twiddle1(long *xp,long *yp)
{ 
    *xp+=*yp;
    *xp+=*yp;
}
void twiddle2(long *xp,long *yp)
{
    *xp += 2* *yp;
}
```

一般情况下可以认为 twiddle2 的效率比 twiddle1 高，因为其只需要执行一次读 *xp、读 *yp 和写 *xp，而 twiddle1 则需要两次。但是当 yp = xp 时，我们会发现两者运行的结果不同

```c
void twiddle1(long *xp,long *xp)
{ 
    *xp+=*xp;
    *xp+=*xp;  // *xp = 4 * *xp
}
void twiddle2(long *xp,long *xp)
{
    *xp += 2* *xp; // *xp = 3 * *xp
}
```

两个指针指向同一片内存这种情况称为内存别名。

另一种情况是函数调用，如 func1 和 func2 看似相同，但是如果 f() 中更改了全局变量，那么便会出现问题

```c
long f();
long func1(){
    return f() + f() + f() + f();
}
long func2(){
    return 4 * f();
}
```



### Expressing Program Performance

计算机的性能指标常用 cycles per element （CPE，每元素指令数），一个 4GHz 的处理器每秒运行 4G 次循环。许多函数会在循环中迭代一些元素，下面的函数 psum1 和 psum2 的功能都是计算一个数组的和

```c
void psum1(float a[],float p[],long n)
{
    long i;
    p[0]=a[0];
    for(i=1;i<n;i++)
        p[i]=p[i-1]+a[i];
}
void psum2(float a[],float p[],long n)
{
    long i;
    p[0]=a[0];
    for(i=1;i<n-1;i+=2){
        float mid_val=p[i-1]+a[i];
        p[i] =mid_val;
        p[i+1] =mid_val +a[i+1];
    }
    /*For even n,finish remaining element*/
    if(i<n)
        p[i]=p[i-1]+a[i];
}
```

psum2 虽然看起来更加复杂，但是却需要更少的指令循环，效率更高。如果绘制两个函数指令循环数与集合数（n 的大小）的关系，可以得到 psum1 的指令循环数可以近似为 368 + 9n，而 psum2 则为 368 + 6n，可得 psum1 的 CPE 为 9，而 psum2 的 CPE 为 6。上面这种方法也被称为 loop unrolling

### Program Example



### Eliminating Loop Inefficiencies

如下面的两段程序

```c
void lower1(char*s)
{
    long i;
    for(i=0;i<strlen(s);i++)
        if(s[i]>='A'&&s[i]<='Z')
            s[i]-=('A'-'a');
}

void lower2(char*s)
{
    long i;
    long len= strlen(s);
    for(i=0;i<len;i++)
        if(s[i]>='A'&&s[i]<='Z')
            s[i]-=('A'-'a');
}
```

由于 lower2 避免了一些无谓的 strlen(s)，所以运行得更快。



## 6 The Memory Hierarchy



## 7 Linking

Link 是一个将不同部分代码和数据集合为单个文件，然后载入内存和执行。

### Compiler Drivers

大多数编译系统提供了一个编译器驱动程序，可以根据需要调用预处理器、编译器、汇编器和链接器。已知两个文件 main.c 和 sum.c

```c
// main.c
int sum(int *a, int n);
int array[2] = {1, 2};
int main(){
    int val = sum(array, 2);
    return val;
}
```

```c
// sum.c
int sum(int *a, int n){
    int i, s = 0;
    for (i = 0; i< n;i++){
        s += a[i];
    }
    return s;
}
```

调用 gcc 命令来进行编译

```sh
gcc -Og -o prog main.c sum.c
```

```mermaid
graph LR
main.c --> main.o
sum.c --> sum.o
main.o --> Linker
sum.o --> Linker
Linker --> prog
```

.c 文件到 .o 文件经过三步

```sh
cpp [other arguments] main.c main.i
cc1 main.i -Og [other arguments] -o main.s
as [other arguments] -o main.o main.s
```

连接器为 ld，将 main.o 和 sum.o 以及必要的系统文件结合起来，创建二进制文件 prog

```sh
ld -o prog [system object files and args] main.o sum.o
```



### Static Linking

静态链接器（如 Linux LD 程序）以可重定位目标文件和命令行参数的集合作为输入，并生成一个可以加载和运行的完全链接目标文件作为输出。输入可重定位的目标文件由各种代码和数据部分组成，其中每个部分都是一个连续的字节序列。指令在一节中，初始化的全局变量在另一节，未初始化的变量在另一节中。

1. 符号解析：目标文件定义和引用符号，其中每个符号对应于函数、全局变量或静态变量（即用静态属性声明的任何 C 变量）。符号解析的目的是将每个符号引用与正确的符号定义相关联。
2. 重新定位：编译器和汇编程序生成代码和数据部分。从地址 0 开始，链接器将这些部分与每个符号定义关联起来重新定位，然后修改对这些符号的所有引用，使它们指向这个内存位置。链接器盲目地使用汇编程序生成的详细指令执行这些重定位，称为重定位入口。

注意，目标文件是字节块的集合，连接器将这些块连接起来。



### Object Files

目标文件有三种形式：

*可重定位目标文件*：包含二进制代码和数据，可以在编译的时候与其它可重定位目标文件组合生成可执行目标文件

*可执行目标文件*：包含可以直接被载入内存和执行的二进制代码和数据

*共享目标文件*：特殊类型的可重定位目标文件，可以在加载时或者运行时动态载入内存和连接。

目标文件有特定格式，不同系统都不同。Linux 系统会使用 ELF 格式。


### Relocatable Object Files


下表展示了一个典型的 ELF 可重定位目标文件

| ELF header           |
| -------------------- |
| .text                |
| .rodata              |
| .data                |
| .bss                 |
| .symtab              |
| .rel.text            |
| .rel.data            |
| .debug               |
| .line                |
| .strtab              |
| Section header table |
ELF header 开头是 16 字节的序列，描述了字节大小和系统字节排列方式（大小端），剩下的 ELF header 包含了允许连接器解释和翻译目标文件的信息，即 ELF header 的大小，目标文件类型，机器类型（如 x86-64），section header table 的文件偏移，入口的大小和数量。section header table 中描述了不同部分的大小和位置，包含了目标文件中每个部分的定长入口。

.text 编译程序的机器码

.rodata 只读的数据，如 printf 的格式字符串和 switch 的跳转表

.data 初始化的全局和静态变量，本地变量保存在运行时栈中，不出现在 .data 或者 .bss 部分。

.bss 未初始化的全局和静态变量，以及任何初始化为零的全局或静态变量。这个部分不会占用目标文件中的实际空间，只是占位符，区分初始化和未初始化是为了空间效率。

.symtab 符号表包含了程序中定义和索引的函数和全局变量信息

.rel.text .text 部分的位置集合，这些位置在连接器结合其它文件时会被修改。一般来说，任意调用外部函数或者索引一个全局变量的指令会需要修改。而调用本地函数则不需要修改

.rel.data 由模块引用或定义的任何全局变量的重定位信息。通常，任何初始值为全局变量或外部定义函数地址的初始化全局变量都需要修改。

...


### Symbol Resolution



>c++ 中有函数重载的概念，在编译器中这些名字相同， 参数列表不同的函数会被编码成独一无二的名字，这个过程称为 mangling。


编译时，编译器将每个全局符号导出进汇编器，或强或弱，汇编程序在可重定位目标文件的符号表中隐含地对此信息进行编码。函数和初始化的全局变量获得强符号。未初始化的全局变量会得到弱符号。对于强符号和弱符号的概念，Linux 链接器使用以下规则来处理重复的符号名称：

+ 多个同名的强符号是不被允许的
+ 存在同名的一个强符号和多个弱符号，选择强符号
+ 存在多个同名弱符号，任意选择一个弱符号

第二条和第三条会导致一些隐藏的运行时 bug，特别是重复的符号定义为不同的类型，如 foo1.c 中定义了一个全局变量
```c
int x = 10;
int main(){
	f();
}
```

foo2.c 中定义了一个同名的全局变量（未初始化），但是类型为 double

```c
double x;
void f(){
	x = -0.0;
}
```

int 类型的 x 会覆盖 double 类型，从而在 f 中会引发错误。


目前，我们一直假设连接器读取可重定位目标文件集合，将它们连接起来输出为目标可执行文件。实际上，所有的编译系统提供了打包静态库单文件相关目标模块的机制。在构建可执行文件时，连接器只复制库中被应用程序引用的的目标模块。c 中有许多静态库，如 libc.a 中定义了标准 I/O，字符串处理等函数。

下面这个指令会将 libc.o 中所有的标准函数连接到可执行文件中

```sh
gcc main.c /usr/lib/libc.o
```

这样有一些不好的地方，如太占用空间，同时编译时间会很长，可以采取下面的方法

```sh
gcc main.c /usr/lib/printf.o /usr/lib/scanf.o
```

但是这种方法需要程序员清楚了解该连接哪些目标模块。

静态库可以用于解决上面这两种方法的缺点

```sh
gcc main.c /usr/lib/libm.a /usr/lib/libc.a
```

这样在连接时，连接器只会复制被引用的目标模块，减少可执行文件的体积，同时便于程序员处理。

为了创建静态库，可以使用 ar
```sh
gcc -c addvec.c multvec.c
ar rcs libvector.a addvec.o multvec.o
```

为了使用这个静态库
```sh
gcc -c main2.c
gcc -static -o prog2c main2.o ./libvector.a
```

>注意静态库需要放在 .c 文件后面（命令行的末尾）


### Relocation


### Dynamic Linking with Shared Libraries


虽然静态库可以解决很多问题，但是存在一些明显的缺陷。静态库和所有的软件一样需要维护和更新，如果程序员希望使用最新版本的库，那么可能需要重新连接。另一个问题是几乎所有的 C 程序都使用标准 I/O，每个运行进程的 text 段中这些函数的代码会重复，这样会产生浪费。

共享库可以解决静态库的确定，共享库是可以在运行时或者加载时载入内存并且连接内存中的程序的目标模块，这一过程也被称为动态链接。共享库在 Linux 中一般为 .so 文件，在 Windows 中为 .dll 文件。

创建共享库的命令

```sh
gcc -shared -fpic -o libvector.so addvec.c multvec.c
```

`-fpic` 选项告诉编译器生成位置独立的代码，`-shared` 选项告诉链接器创建共享库。使用共享库的命令如下
```sh
gcc -o prog2l main2.c ./libvector.so
```


...


## 8 Exceptional Control Flow

759



## 9 Virtual Memory

### Physical and Virtual Addressing

计算机系统的主存可以认为是一个 M 个连续的字节块，每个字节有着独特的物理地址（PA），第一个字节的地址为 0，下一个字节的地址为 1，以此类推。早期的电脑使用物理寻址，数字信号处理器、嵌入式微控制器和 Cray 超级计算机都沿用这一设计。但是现代处理器使用虚拟地址寻址，如下图所示

![image-20240429123857740](https://cdn.jsdelivr.net/gh/Xiang-M-J/MyPic@img/img/image-20240429123857740.png)

虚拟寻址时，CPU 会生成一个虚拟地址，然后转换为合适的物体地址送入内存，负责转换的硬件称为 MMU。


### Address Spaces

地址空间是一个非负整数地址的有序集合，n 位的 CPU 可以产生 $N=2^n$ 个虚拟地址，现代处理器 n 一般取 32 或 64。一个系统也会有一个物理地址空间对应于 M 个物理内存。


### VM as a Tool for Caching

硬盘上的数据会被分成块，作为硬盘和内存的传输单元，VM 系统通过将虚拟内存拆分成固定大小块（虚拟页）实现。每个虚拟页的大小为 $P=2^p$，类似地，物理内存被拆分为物理页，大小也为 P 字节，物理页也被称为页帧。

任何时间点，虚拟页的集合被分为三个不相交的子集

+ *未分配的*：虚拟机系统尚未分配(或创建)的页面。未分配的块没有与它们关联的任何数据，因此不占用磁盘上的任何空间。
+ *缓存*：当前缓存在物理内存中的已分配页面。
+ *不缓存*：未缓存在物理内存中的已分配页面


为了区分内存架构中的不同缓存，使用 SRAM 表示 L1，L2 和 L3，DRAM 表示缓存内存中的虚拟页的虚拟系统缓存。SRAM 比 DRAM 快十倍，而 DRAM 比硬盘快大约 100000 倍。因此，与SRAM缓存中的错误相比，DRAM缓存中的错误是非常耗时的，因为DRAM缓存错误是由硬盘提供的。

由于很大的丢失代价和访问第一个字节的开销，虚拟页面往往很大，通常为 4KB 到 2MB。由于很大的丢失代价，DRAM缓存是完全关联的；也就是说，任何虚拟页都可以放置在任何物理页中。对于错误的替换策略也更重要，因为替换错误的虚拟页面所带来的损失非常大。操作系统对 DRAM 缓存使用的替换算法比硬件对 SRAM 缓存使用的替换算法复杂得多。最后，由于硬盘的访问时间很长，DRAM缓存总是使用回写（延迟更新内存）而不是透写（同时更新缓存和内存）。

>DRAM 缓存丢失被称为 page fault



## 10 System-Level I/O


### Unix I/O

一个 Linux 文件是 m 个字节的序列，所有的 I/O 设备，如网络、硬盘和终端都被建模成文件，所有输入输出都以读写对应文件的方式执行。


### Files


*常规文件*：文本文件，二进制文件

*目录*：由一组链接组成的文件，每个链接指向一个文件的文件名

*socket*：通过网络与其它进程通信

其它还有管道、符号链接等。


### Opening and Closing Files


调用 open 函数来打开文件或者创建文件

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int open(char *filename, int flags, mode_t mode);  // -1 表示错误
```

例如，读取一个已经存在的文件

```c
fd = Open("foo.txt", O_RDONLY, 0);
```



## 11 Network Programming


### The Client-Server Programming Model

每个网络应用基于 client-server 模型，一个应用包含了一个服务器进程和若干个客户端进程，一个服务器管理一些资源，通过操作资源为它的客户端提供一些服务。



12 