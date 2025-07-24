# obs/obs_controller.py
# 06.22

from obsws_python import ReqClient

host = "localhost"
port = 4455
password = ""

ws = ReqClient(host=host, port=port, password=password)

# OBS 버전 가져오기
version_response = ws.send("GetVersion", {})
print("OBS WebSocket Version:", version_response.obs_web_socket_version)

# 현재 프로그램 장면 이름 가져오기
scene_response = ws.send("GetCurrentProgramScene", {})
scene_name = scene_response.current_program_scene_name
print("현재 장면:", scene_name)

# 텍스트 소스 생성
input_settings = {
    "sceneName": scene_name,
    "inputName": "HelloText",
    "inputKind": "text_ft2_source_v2",
    "inputSettings": {"text": "Hello, OBS!"},
    "sceneItemEnabled": True
}

ws.send("CreateInput", input_settings)
print("텍스트 소스 추가 완료") 
