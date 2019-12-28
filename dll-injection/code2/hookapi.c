#pragma warning(disable:4996)
#include "windows.h"  
#include "stdio.h"  

LPVOID g_pfWriteFile = NULL;//WriteFile函数地址
CREATE_PROCESS_DEBUG_INFO g_cpdi;//int 3指令的机器码
BYTE g_chINT3 = 0xCC, g_chOrgByte = 0;//存放原来被覆盖掉的一字节
//被调试进程启动时函数发生作用
BOOL OnCreateProcessDebugEvent(LPDEBUG_EVENT pde)
{
	// get WriteFile() API address  
	g_pfWriteFile = GetProcAddress(GetModuleHandleA("kernel32.dll"), "WriteFile");

	// API Hook - WriteFile()  
	// change first byte to 0xCC(INT 3)
	//将WriteFile入口处第一字节保存后，用CC断点替换它，以后每次执行此函数将会发生调试中断
	memcpy(&g_cpdi, &pde->u.CreateProcessInfo, sizeof(CREATE_PROCESS_DEBUG_INFO));
	ReadProcessMemory(g_cpdi.hProcess, g_pfWriteFile,
		&g_chOrgByte, sizeof(BYTE), NULL);
	WriteProcessMemory(g_cpdi.hProcess, g_pfWriteFile,
		&g_chINT3, sizeof(BYTE), NULL);

	return TRUE;
}
//当发生异常启动时会执行此函数
BOOL OnExceptionDebugEvent(LPDEBUG_EVENT pde)
{
	CONTEXT ctx;
	PBYTE lpBuffer = NULL;
	DWORD dwNumOfBytesToWrite, dwAddrOfBuffer, i;
	PEXCEPTION_RECORD per = &pde->u.Exception.ExceptionRecord;

	// BreakPoint exception (INT 3)   
	if (EXCEPTION_BREAKPOINT == per->ExceptionCode)//判断中断类型是不是Int3中断
	{
		// BP at WriteFile() API  
		if (g_pfWriteFile == per->ExceptionAddress) //判断发生中断的地址是不是WriteFile函数入口
		{
			// #1. Unhook 
			//恢复原程序内容，即恢复第一字节，这样WriteFile函数才能正常执行，因为后面会用到该函数
			// restore 0xCC to original byte   
			WriteProcessMemory(g_cpdi.hProcess, g_pfWriteFile,
				&g_chOrgByte, sizeof(BYTE), NULL);
			// #2. Get Thread Context   
			//获取线程上下文，其实就是各个寄存器的值
			//获得进程上下文之后就可以获得进程中函数得各个参数值
			ctx.ContextFlags = CONTEXT_CONTROL;
			GetThreadContext(g_cpdi.hThread, &ctx);
			// #3. Get WriteFile() param 2, 3  
			//获取堆栈内容，即WriteFile的第二个和第三个参数，注意由于这里已经调用了函数，堆栈压入了函数返回地址，减了4字节
			//   param 2 : ESP + 0x8 writeFile（）的字符缓冲区地址 
			//   param 3 : ESP + 0xC WriteFile（）的字符缓冲区大小
			//这两个参数经过调试验证没问题
			ReadProcessMemory(g_cpdi.hProcess, (LPVOID)(ctx.Esp + 0x8),
				&dwAddrOfBuffer, sizeof(DWORD), NULL);
			ReadProcessMemory(g_cpdi.hProcess, (LPVOID)(ctx.Esp + 0xC),
				&dwNumOfBytesToWrite, sizeof(DWORD), NULL);
			// #4. Allocates temp buf  分配缓冲区，用来存放字符串
			lpBuffer = (PBYTE)malloc(dwNumOfBytesToWrite + 1);
			//将新分配的缓冲区的内容清零，以便存放内容
			memset(lpBuffer, 0, dwNumOfBytesToWrite + 1);
			// #5. Copy WriteFile() buf to temp buf  将新分配的缓冲区的内容清零，以便存放内容
			//将第二个参数所指地址，原字符串拷贝到新建的缓冲区中
			ReadProcessMemory(g_cpdi.hProcess, (LPVOID)dwAddrOfBuffer,
				lpBuffer, dwNumOfBytesToWrite, NULL);
			//#6.比对文件内容，根据设定进行转换
			printf("\n### original string ###\n%s\n", lpBuffer);
			if (strcmp(lpBuffer,"hahaha")==0)
			{
				//printf("内容需转换\n");
				strcpy(lpBuffer ,"hehehe");
				//printf("内容转换完毕！");
				//lpBuffer = "呵呵呵";
			}
			else
			{
				printf("内容不符合要求，不转换");
			}
	

			printf("\n### converted string ###\n%s\n", lpBuffer);

			// #7. Copy to WriteFile() buf  
			//将转换后的内容写会原缓冲区
			WriteProcessMemory(g_cpdi.hProcess, (LPVOID)dwAddrOfBuffer,lpBuffer, dwNumOfBytesToWrite, NULL);

			// #8. release temp buf  释放临时缓冲区
			free(lpBuffer);

			// #9. Change EIP to WriteFile() address  
			//将EIP指针地址改回WriteFile的入口地址，因为执行int3指令，地址已经向后移了一位
			ctx.Eip = (DWORD)g_pfWriteFile;
			SetThreadContext(g_cpdi.hThread, &ctx);

			// #10. Run Debuggee process  
			//成功处理异常，程序继续执行
			ContinueDebugEvent(pde->dwProcessId, pde->dwThreadId, DBG_CONTINUE);
			Sleep(0);
			//用于释放本进程资源，使被调试进程得以执行到writeFileAddress所指示地址之后，否则下一句立即执行可能导致死循环
			// #11. API Hook  再次写入API钩子
			WriteProcessMemory(g_cpdi.hProcess, g_pfWriteFile,
				&g_chINT3, sizeof(BYTE), NULL);

			return TRUE;
		}
	}

	return FALSE;
}
//调试循环，循环等待调试事件，直到进程退出
void DebugLoop()
{
	DEBUG_EVENT de;
	DWORD dwContinueStatus;

	// Waiting for the event occurred by debuggee  
	while (WaitForDebugEvent(&de, INFINITE))
	{
		dwContinueStatus = DBG_CONTINUE;
		//当创建调试时执行钩取
		// Debuggee process generates or attaches event  
		if (CREATE_PROCESS_DEBUG_EVENT == de.dwDebugEventCode)
		{
			OnCreateProcessDebugEvent(&de);
		}
		// Exception event  //当发生异常调试事件时转到
		else if (EXCEPTION_DEBUG_EVENT == de.dwDebugEventCode)
		{
			if (OnExceptionDebugEvent(&de))
				continue;
		}
		// Debuggee process terminates event  //当被调试进程退出时执行
		else if (EXIT_PROCESS_DEBUG_EVENT == de.dwDebugEventCode)
		{
			// debuggee stop -> debugger stop  被调试进程终止
			break;
		}

		// Run the debuggee again  应该设置为DBG_EXCEPTION_NOT_HANDLED再交由SEH处理的
		ContinueDebugEvent(de.dwProcessId, de.dwThreadId, dwContinueStatus);
	}
}

int main(int argc, char* argv[])
{
	DWORD dwPID;

	if (argc != 2)
	{
		printf("\nUSAGE : hookdbg.exe <pid>\n");
		return 1;
	}

	// Attach Process  //开始调试
	dwPID = atoi(argv[1]);
	if (!DebugActiveProcess(dwPID))
	{
		printf("DebugActiveProcess(%d) failed!!!\n"
			"Error Code = %d\n", dwPID, GetLastError());
		return 1;
	}

	// debugger loops  //开始循环钩取
	DebugLoop();

	return 0;
}