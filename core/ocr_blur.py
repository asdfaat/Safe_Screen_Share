import pytesseract
import re

# Tesseract 실행 파일 경로 직접 지정 (윈도우 기본 설치 경로)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_and_blur_sensitive_data(img, settings):
    regions = []
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng+kor')
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        text = data['text'][i]
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        if not text.strip():
            continue
        if "email" in settings["targets"]:
            if re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text):
                regions.append((x, y, w, h))
        if "credit_card" in settings["targets"]:
            if re.search(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", text):
                regions.append((x, y, w, h))
        if "username" in settings["targets"]:
            if re.search(r"[A-Za-z가-힣]{3,20}", text):
                regions.append((x, y, w, h))
    return regions