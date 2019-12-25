# dll注入
## 实验一要求
- [x] 查文档，研究远程线程方式注入dll的实例代码的实现原理。
- [x]运行实例代码，向一个目标程序（比如notepad.exe)注入一个我们自行编写的dll，加载运行。
- [x]整合进程遍历的程序，使得攻击程序可以自己遍历进程得到目标程序的pid。
## 实验一完成
1. dll文件生成在上节课已完成，本次实验直接使用
2. 使用[dll注入代码来源](https://github.com/fdiskyou/injectAllTheThings)中的t_CreateRemoteThread.c并调用其中的函数
![](images/createremotethread.png)
3. 为了确保notepad是32位，打开'Winodws/SysWOW64'中的Notepadcmd中使用```tasklist```查看进程的Pid后更改。
4. 运行后看到确实有弹窗
![](images/dllinjection.png)
## 实验二要求

## 实验二完成
