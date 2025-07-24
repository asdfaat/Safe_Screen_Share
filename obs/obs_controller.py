from obsws_python import ReqClient

def add_or_update_image_source(
    image_path,
    source_name="BlurredImage",
    scene_name=None,
    host="localhost",
    port=4455,
    password=""
):
    ws = ReqClient(host=host, port=port, password=password)

    # 현재 장면 이름 자동 감지
    if scene_name is None:
        scene_response = ws.send("GetCurrentProgramScene", {})
        scene_name = scene_response.current_program_scene_name

    # 이미지 소스가 이미 존재하는지 확인
    sources = ws.send("GetInputList", {})
    inputs = sources.inputs  # 여기는 속성 (리스트 of dict)

    exists = any(s["inputName"] == source_name for s in inputs)

    if not exists:
        # 이미지 소스 생성
        ws.send("CreateInput", {
            "sceneName": scene_name,
            "inputName": source_name,
            "inputKind": "image_source",
            "inputSettings": {"file": image_path},
            "sceneItemEnabled": True
        })
    else:
        # 이미지 소스가 이미 있으면 파일만 갱신
        ws.send("SetInputSettings", {
            "inputName": source_name,
            "inputSettings": {"file": image_path},
            "overlay": True
        })