import cv2
import numpy as np
import os

def detect_ui_elements(img, settings):
    regions = []
    if "kakao_popup" in settings["targets"]:

        template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'template', 'kakao_popup_template.png')
        mask_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'template', 'kakao_popup_mask.png')

        if os.path.exists(template_path) and os.path.exists(template_path):
            
            # 이미지 전처리
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

            template = cv2.imread(template_path)
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = clahe.apply(template)

            mask = cv2.imread(mask_path)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = clahe.apply(gray)

            # match
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED, mask=mask)

            threshold = 0.5
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                regions.append((pt[0], pt[1], template.shape[1], template.shape[0]))
    
    
    # login_field 등 추가 템플릿 매칭 가능
    return regions