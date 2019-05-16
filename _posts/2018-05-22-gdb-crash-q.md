---
layout: post
title: "GDB 难以定位的 Crash - 越界访问"
date: 2018-05-22 23:16:34 +0800
categories: [cpp, GDB]
tags: [crash]
---

示例代码：

~~~cpp
#include <iostream>
#include <vector>
#include <map>

using namespace std;

void Funct() {
    map<int, int> iimap;

    iimap[1] = 1;
}


int main(int argc, char  **argv) {

    vector<int> ivec;
    ivec.reserve(10);

    ivec[11] = 10;

    Funct();

    cout << "end" << endl;

    return 0;
}
~~~

这段程序越界写入数组会导致 crash，但是 core 文件定位的时候并不好找，bt 打印的信息：

~~~bash
(gdb) bt
#0  0x00007fb5e6f581f7 in raise () from /lib64/libc.so.6
#1  0x00007fb5e6f598e8 in abort () from /lib64/libc.so.6
#2  0x00007fb5e6f97f47 in __libc_message () from /lib64/libc.so.6
#3  0x00007fb5e6f9f619 in _int_free () from /lib64/libc.so.6
#4  0x00000000004027c4 in __gnu_cxx::new_allocator<std::_Rb_tree_node<std::pair<int const, int> > >::deallocate (this=0x7ffe37e10140, __p=0xc52040) at /usr/include/c++/4.8.2/ext/new_allocator.h:110
#5  0x00000000004022ee in std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_put_node (
    this=0x7ffe37e10140, __p=0xc52040) at /usr/include/c++/4.8.2/bits/stl_tree.h:374
#6  0x00000000004019a4 in std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_destroy_node (
    this=0x7ffe37e10140, __p=0xc52040) at /usr/include/c++/4.8.2/bits/stl_tree.h:422
#7  0x00000000004012d5 in std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase (
    this=0x7ffe37e10140, __x=0xc52040) at /usr/include/c++/4.8.2/bits/stl_tree.h:1127
#8  0x0000000000400f46 in std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::~_Rb_tree (
    this=0x7ffe37e10140, __in_chrg=<optimized out>) at /usr/include/c++/4.8.2/bits/stl_tree.h:671
#9  0x0000000000400ee6 in std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > >::~map (this=0x7ffe37e10140, __in_chrg=<optimized out>)
    at /usr/include/c++/4.8.2/bits/stl_map.h:96
#10 0x0000000000400d9e in Funct () at main.cpp:10
#11 0x0000000000400e0a in main (argc=1, argv=0x7ffe37e102c8) at main.cpp:21

~~~

从这段栈信息中并不能直观的定位到出现问题的地方，因为出现问题的地方是之前的数组越界，但是这里的栈信息已经执行到 Funct 中的 map, 特别是在大项目中更是无法准确的定位出错的地方。
越界写坏内存，什么时候会 crash 取决于我们写坏的内存什么时候被用到，有时候会离犯罪现场特别远，因为真的有人会写出对一个 10 个元素的数组用 vec[50] = xxx 的代码。

使用 valgrind 进行越界检查。