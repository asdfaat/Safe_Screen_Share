import pytesseract
import re
import openai

def detect_sensitive_data(img, settings):
    regions = []
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='eng+kor')
    n_boxes = len(data['level'])
    texts_with_bbox = []
    for i in range(n_boxes):
        text = data['text'][i]
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        if not text.strip():
            continue
        texts_with_bbox.append((text, (x, y, w, h)))
        # 1. 정규표현식 기반 탐지
        if "email" in settings["targets"]:
            if re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text):
                regions.append((x, y, w, h))
        if "credit_card" in settings["targets"]:
            if re.search(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", text):
                regions.append((x, y, w, h))
        if "username" in settings["targets"]:
            if re.search(r"[A-Za-z가-힣]{3,20}", text):
                regions.append((x, y, w, h))

    # 2. OpenAI API 기반 의미적 탐지 (옵션)
    if settings.get("use_openai_api"):
        openai.api_key = settings.get("openai_api_key")
        for text, bbox in texts_with_bbox:
            prompt = f"다음 텍스트가 개인정보(이름, 계좌, 전화번호, 이메일, 주소 등)인지 한글로 '예' 또는 '아니오'로만 답하세요:\n{text}"
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1,
                    temperature=0
                )
                answer = response.choices[0].message.content.strip()
                if answer.startswith("예"):
                    regions.append(bbox)
            except Exception as e:
                pass  # API 오류 무시

    return regions
