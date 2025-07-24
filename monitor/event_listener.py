import win32gui
import time

def monitor_window_state(settings):
    """창 전환 및 바탕화면 상태 모니터링"""
    prev_hwnd = None
    while True:
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        if "desktop_entry" in settings["targets"] and window_title == "":
            # 바탕화면 진입 시 전체 블러 등 처리 (필요시 콜백 구현)
            pass
        prev_hwnd = hwnd
        time.sleep(0.1)
