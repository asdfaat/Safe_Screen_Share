import sys
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import json
import os

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'settings.json')

BLUR_OPTIONS = [
    ("이메일", "email"),
    ("신용카드 번호", "credit_card"),
    ("로그인 필드", "login_field"),
    ("카카오톡 팝업", "kakao_popup"),
    ("바탕화면 진입 시 전체 블러", "desktop_entry"),
    ("사용자 이름", "username"),
    ("ML 기반 로그인 필드 탐지", "use_ml_ui_detector"),
    ("OpenAI API 의미 탐지", "use_openai_api"),
]

def load_settings():
    with open(SETTINGS_PATH, encoding='utf-8') as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

def show_settings_window():
    settings = load_settings()
    app = tb.Window(themename="superhero")
    app.title("Safe Screen Share - 옵션 선택")
    app.geometry("490x450")

    closed = {"flag": False}
    def on_close():
        closed["flag"] = True
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)

    vars = {}
    row = 0
    for label, key in BLUR_OPTIONS:
        var = tb.BooleanVar(value=(key in settings.get("targets", []) or settings.get(key, False)))
        chk = tb.Checkbutton(app, text=label, variable=var, bootstyle="success")
        chk.grid(row=row, column=0, sticky="w", padx=20, pady=5)
        vars[key] = var
        row += 1

    # OpenAI API Key 입력(테스트할 때만 하드코딩, 배포할 때는 제거)
    api_label = tb.Label(app, text="OpenAI API Key:")
    api_label.grid(row=row, column=0, sticky="w", padx=20, pady=5)
    api_var = tb.StringVar(value=settings.get("openai_api_key", ""))
    api_entry = tb.Entry(app, textvariable=api_var, width=40)
    api_entry.grid(row=row+1, column=0, padx=20, pady=5)
    row += 2

    def save_and_close():
        # targets는 체크된 주요 항목만
        targets = [k for k in ["email", "credit_card", "login_field", "kakao_popup", "desktop_entry", "username"] if vars[k].get()]
        settings["targets"] = targets
        # 기타 옵션
        settings["use_ml_ui_detector"] = vars["use_ml_ui_detector"].get()
        settings["use_openai_api"] = vars["use_openai_api"].get()
        settings["openai_api_key"] = api_var.get()
        save_settings(settings)
        app.destroy()

    btn = tb.Button(app, text="저장 후 시작", bootstyle="primary", command=save_and_close)
    btn.grid(row=row, column=0, pady=20)
    app.mainloop()
    return closed["flag"]