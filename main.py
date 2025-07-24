import threading
import time
import sys
from monitor.screen_capture import capture_screen, save_blurred_screen
from monitor.event_listener import monitor_window_state
from core.ocr_blur import detect_and_blur_sensitive_data
from core.template_match import detect_ui_elements
from ui.region_selector import select_region_for_blurring
from utils.settings import load_settings
from ui.main_window import show_settings_window

# OBS 자동 연동 추가
from obs.obs_controller import add_or_update_image_source

def main():
    # 1. GUI로 옵션 선택
    closed = show_settings_window()
    if closed:
        sys.exit(0)
    settings = load_settings()

    # 2. 창 상태 감지 (바탕화면, 창 전환 등)
    threading.Thread(target=monitor_window_state, args=(settings,), daemon=True).start()

    # 3. 마우스 드래그 영역 블러
    blur_regions_list = []
    if settings.get("enable_region_blur"):
        region = select_region_for_blurring()
        if region:
            blur_regions_list.append(region)

    # 4. OBS에 이미지 소스 자동 추가 (최초 1회)
    add_or_update_image_source(
        image_path="blurred_sensitive_data.png",
        source_name="BlurredImage",
        host="localhost",
        port=4455,
        password=""  # 필요시 obs-websocket 비밀번호 입력
    )

    # 5. 실시간 화면 감지 및 블러
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

        # 마우스 드래그 영역 블러
        regions_to_blur += blur_regions_list

        # 블러 처리 및 저장
        save_blurred_screen(screen, regions_to_blur)

        # OBS 이미지 소스 파일 갱신 (매 루프마다)
        add_or_update_image_source(
            image_path="blurred_sensitive_data.png",
            source_name="BlurredImage",
            host="localhost",
            port=4455,
            password=""
        )

        time.sleep(1.0 / settings.get("fps", 20))

if __name__ == "__main__":
    main()