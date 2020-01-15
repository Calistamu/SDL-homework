#include<Windows.h>

// 函数定义在 IATHook.c 中
LONG IATHook(
    __in_opt void* pImageBase,
    __in_opt char* pszImportDllName,
    __in char* pszRoutineName,
    __in void* pFakeRoutine,
    __out HANDLE* phHook);

void* GetIATHookOrign(__in HANDLE hHook);

HANDLE g_hHook_WriteFile = NULL;
typedef BOOL(__stdcall * LPFN_WriteFile)(HANDLE hFile, LPCVOID lpBuffer, DWORD nNumberOfBytesToWrite,
    LPDWORD lpNumberOfBytesWritten, LPOVERLAPPED lpOverlapped);

BOOL __stdcall Fake_WriteFile(HANDLE hFile, LPCVOID lpBuffer, DWORD nNumberOfBytesToWrite,
    LPDWORD lpNumberOfBytesWritten, LPOVERLAPPED lpOverlapped)
{
    LPFN_WriteFile fnOrigin = (LPFN_WriteFile)GetIATHookOrign(g_hHook_WriteFile);

    if (strcmp(lpBuffer, "hahaha") == 0)
        lpBuffer = "hehehe";

    // 调用原始的 WriteFile 函数
    return fnOrigin(hFile, lpBuffer, nNumberOfBytesToWrite, lpNumberOfBytesWritten, lpOverlapped);
}

BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // handle to DLL module
    DWORD fdwReason,     // reason for calling function
    LPVOID lpReserved)  // reserved
{
    // Perform actions based on the reason for calling.
    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        // Initialize once for each new process.
        IATHook(
            GetModuleHandleW(NULL),
            "kernel32.dll",
            "WriteFile",
            Fake_WriteFile,
            &g_hHook_WriteFile
        );
        // Return FALSE to fail DLL load.
        break;
    }
    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}