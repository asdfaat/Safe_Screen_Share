import cv2
import numpy as np
import os

def detect_ui_elements(img, settings):
    regions = []
    if "kakao_popup" in settings["targets"]:
        template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icons', 'kakao_popup.png')
        if os.path.exists(template_path):
            template = cv2.imread(template_path, 0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                regions.append((pt[0], pt[1], template.shape[1], template.shape[0]))
    # login_field 등 추가 템플릿 매칭 가능
    return regions