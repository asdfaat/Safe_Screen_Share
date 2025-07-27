# main2.py

import threading
import time
import sys
import cv2
import pyvirtualcam
from monitor.screen_capture import capture_screen, blur_regions
from monitor.event_listener import monitor_window_state
from core.ocr_blur import detect_and_blur_sensitive_data
from core.template_match import detect_ui_elements
from core.kakao_blur import detect_kakao_windows  
from ui.region_selector import select_region_for_blurring
from ui.main_window import show_settings_window
from utils.settings import load_settings

def main():
    # 1. GUI로 옵션 선택
    closed = show_settings_window()
    if closed:
        sys.exit(0)
    settings = load_settings()

    # 블러 콜백 함수 정의 
    global_blur_flag = {"do_blur": False}
    def on_blur(event_type):
        global_blur_flag["do_blur"] = True

    # 2. 창 상태 감지 (바탕화면, 창 전환 등)
    threading.Thread(target=monitor_window_state, args=(settings, on_blur), daemon=True).start()

    # 3. 마우스 드래그 영역 블러
    blur_regions_list = []
    if settings.get("enable_region_blur"):
        region = select_region_for_blurring()
        if region:
            blur_regions_list.append(region)

    # 4. 가상카메라 시작 (해상도 자동 감지)
    screen = capture_screen()
    height, width = screen.shape[:2]
    with pyvirtualcam.Camera(width=width, height=height, fps=settings.get("fps", 20), print_fps=False) as cam:
        print(f'가상카메라 시작: {cam.device}')
        while True:
            screen = capture_screen()
            regions_to_blur = []

            # 텍스트 기반 민감정보 감지
            if settings.get("blur_sensitive_text"):
                regions_to_blur += detect_and_blur_sensitive_data(screen, settings)

            # 템플릿/팝업 감지
            if settings.get("blur_ui_elements"):
                regions_to_blur += detect_ui_elements(screen, settings)

            # ML 기반 로그인 필드 탐지
            if settings.get("use_ml_ui_detector"):
                from core.ml_ui_detector import detect_login_fields
                regions_to_blur += detect_login_fields(screen, settings)
            
            # 카카오톡 창 감지 
            if settings.get("blur_kakao_windows"):
               regions_to_blur += detect_kakao_windows(screen, settings)    

            # 마우스 드래그 영역 블러
            regions_to_blur += blur_regions_list

            # 블러 처리
            blurred = blur_regions(screen, regions_to_blur)
            
            # 창 전환/바탕화면 진입 시 전체 블러 처리
            if global_blur_flag["do_blur"]:
                blurred = cv2.GaussianBlur(blurred, (51, 51), 0)
                global_blur_flag["do_blur"] = False

            rgb = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
            cam.send(rgb)
            cam.sleep_until_next_frame()

if __name__ == "__main__":
    main()
