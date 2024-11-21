import sys
import os
import time
import random
import ctypes
from ctypes import windll, create_string_buffer

def check_debugger():
    """检查是否存在调试器"""
    return windll.kernel32.IsDebuggerPresent() != 0

def check_timing():
    """检测时间异常"""
    start = time.time()
    for i in range(1000):
        pass
    end = time.time()
    return (end - start) > 0.1

def check_sandbox():
    """检测沙箱环境"""
    username = os.getenv('USERNAME')
    computername = os.getenv('COMPUTERNAME')
    suspicious = ['sandbox', 'virtual', 'vm', 'test', 'sample', 'virus']
    return any(s in (username + computername).lower() for s in suspicious)

def perform_checks():
    """执行所有安全检查"""
    if check_debugger() or check_timing() or check_sandbox():
        # 如果检测到异常，随机退出或制造混乱
        actions = [
            lambda: sys.exit(random.randint(1, 999)),
            lambda: divmod(1, 0),
            lambda: os.abort(),
            lambda: windll.kernel32.TerminateProcess(windll.kernel32.GetCurrentProcess(), 1)
        ]
        random.choice(actions)()

# 定期执行检查
def start_monitoring():
    while True:
        try:
            perform_checks()
            time.sleep(random.uniform(10, 30))
        except:
            pass

# 启动监控线程
import threading
threading.Thread(target=start_monitoring, daemon=True).start() 