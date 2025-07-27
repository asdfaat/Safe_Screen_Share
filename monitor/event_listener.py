# event_listener.py

import win32gui
import time

def monitor_window_state(settings, on_blur):
    """창 전환 및 바탕화면/창 상태 모니터링 및 블러 처리"""
    prev_hwnd = None
    prev_title = None
    while True:
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        # 바탕화면 진입 시 전체 블러
        if "desktop_entry" in settings["targets"] and window_title == "":
            on_blur("desktop_entry")
        # 창 전환(바탕화면 제외) 시 전체 블러
        elif (
            "window_switch" in settings["targets"]
            and prev_hwnd is not None
            and hwnd != prev_hwnd
            and window_title != "" and prev_title != ""
        ):
            on_blur("window_switch")
        prev_hwnd = hwnd
        prev_title = window_title
        time.sleep(0.03)  # 실시간성 위해 최소화
