import win32gui
import win32process
import psutil
import numpy as np

class KakaoDetector:
    """카카오톡 창 감지 클래스"""
    def __init__(self):
        self.cached_windows = []
        self.found_kakao = False
        
    def find_kakao_windows(self):
        """실행 중인 카카오톡 창 찾기"""
        kakao_windows = []
        
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                
                # 방법 1: 창 제목으로 감지
                if '카카오톡' in window_title or 'KakaoTalk' in window_title:
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        'hwnd': hwnd,
                        'rect': rect,
                        'title': window_title,
                        'type': 'main_window',
                        'method': 'title'
                    })
                    
                # 방법 2: 프로세스 이름으로 감지
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    process_name = process.name().lower()
                    
                    if 'kakaotalk' in process_name:
                        rect = win32gui.GetWindowRect(hwnd)
                        # 중복 체크
                        if not any(w['hwnd'] == hwnd for w in windows):
                            windows.append({
                                'hwnd': hwnd,
                                'rect': rect,
                                'title': window_title or "카카오톡",
                                'type': 'main_window',
                                'method': 'process'
                            })
                except:
                    pass
                    
                # 방법 3: 카카오톡 알림창 감지
                if class_name in ["KakaoTalkEdgeWnd", "KakaoTalkShadowWnd"]:
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        'hwnd': hwnd,
                        'rect': rect,
                        'title': "카카오톡 알림",
                        'type': 'notification',
                        'method': 'class'
                    })
        
        win32gui.EnumWindows(enum_callback, kakao_windows)
        return kakao_windows
    
    def convert_to_regions(self, windows, screen_shape, settings):
        """윈도우 정보를 블러 영역으로 변환"""
        regions = []
        screen_height, screen_width = screen_shape[:2]
        
        for window in windows:
            # 알림창 필터링
            if window['type'] == 'notification' and not settings.get("blur_kakao_notifications", True):
                continue
                
            # 알림창만 블러하는 옵션
            if settings.get("blur_kakao_notifications_only", False) and window['type'] != 'notification':
                continue
            
            left, top, right, bottom = window['rect']
            
            # 화면 범위 체크
            left = max(0, left)
            top = max(0, top)
            right = min(screen_width, right)
            bottom = min(screen_height, bottom)
            
            # 유효한 영역인지 확인
            if left < right and top < bottom:
                regions.append({
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top,
                    'type': 'kakao_' + window['type'],
                    'title': window['title'],
                    'blur_strength': settings.get("kakao_blur_strength", 51)
                })
        
        return regions

# 전역 디텍터 인스턴스
_detector = KakaoDetector()

def detect_kakao_windows(screen, settings):
    """
    main2.py에서 호출할 메인 함수
    
    Args:
        screen: numpy array 형태의 화면 캡처
        settings: 설정 딕셔너리
        
    Returns:
        list: 블러할 영역 정보 리스트
    """
    # 카카오톡 창 찾기
    kakao_windows = _detector.find_kakao_windows()
    
    # 디버깅 정보 출력
    if settings.get("debug_mode", False):
        if kakao_windows and not _detector.found_kakao:
            print(f"\n[KakaoBlur] 카카오톡 창 {len(kakao_windows)}개 발견!")
            for window in kakao_windows:
                print(f"  - {window['title']} (방법: {window['method']}, 타입: {window['type']})")
            _detector.found_kakao = True
        elif not kakao_windows and _detector.found_kakao:
            print("[KakaoBlur] 카카오톡 창이 닫혔습니다.")
            _detector.found_kakao = False
    
    # 블러 영역으로 변환
    regions = _detector.convert_to_regions(kakao_windows, screen.shape, settings)
    
    return regions

# 유틸리티 함수들
def is_kakao_running():
    """카카오톡이 실행 중인지 확인"""
    for proc in psutil.process_iter(['name']):
        if 'kakaotalk' in proc.info['name'].lower():
            return True
    return False

def get_kakao_process_info():
    """카카오톡 프로세스 정보 반환 (디버깅용)"""
    kakao_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        if 'kakaotalk' in proc.info['name'].lower():
            kakao_processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory_mb': proc.info['memory_info'].rss / 1024 / 1024
            })
    return kakao_processes