# ☕ Emotional Card Builder (감성 카드 빌더)

이미지와 배경음악을 선택하여 나만의 감성적인 HTML 웹 브라우저 카드를 손쉽게 제작할 수 있도록 도와주는 프로그램입니다.

## ✨ 주요 기능
- **직관적인 UI**: 파이썬 등의 복잡한 코드 수정 없이, 화면에서 바로 이미지와 MP3 파일만 선택하면 카드가 생성됩니다.
- **문구 커스터마이징**: 메인 문구, 영어 서브타이틀, 하단 감성 문구를 마음대로 수정하여 세상에 하나뿐인 카드를 제작할 수 있습니다.
- **아름다운 시각 및 청각 효과**:
  - 선택한 사진이 서서히 줌인(Zoom-in) 되는 애니메이션이 적용됩니다.
  - HTML Canvas를 활용해 창가에 빗물이 흘러내리는 듯한 감성 스크린 효과를 보여줍니다.
  - 음악 재생 시 볼륨과 높낮이에 실시간으로 반응하는 멋진 오디오 스펙트럼(Visualizer) 바가 작동합니다.
- **자동 테마 색상 지정**: Python의 Pillow 라이브러리가 선택한 이미지의 주요 색상(Color)을 분석해 배경 및 테마를 이미지 분위기에 맞게 자동 매칭합니다.
- **단일 HTML 내보내기**: 모든 사진과 배경음악을 Base64 텍스트로 인코딩하여 HTML 내부에 알아서 포함시켜 냅니다. 따라서 복잡하게 파일을 여러 개 공유할 필요 없이, 최종 만들어진 `.html` 파일 하나만 카톡이나 이메일로 전달해도 상대방이 완벽하게 감상할 수 있습니다.

---

## 🚀 설치 및 사용법

### 1. 필수 라이브러리 설치
이 프로젝트는 Python 3 이상이 설치된 환경에서 동작합니다. 터미널을 열고 먼저 패키지를 설치해 주세요.
```bash
pip install -r requirements.txt
```

### 2. 빌더(GUI) 실행
코드를 직접 실행해 빌더 창을 띄울 수 있습니다.
```bash
python card_builder.py
```

### 3. .exe 실행 파일 만들기 (선택 사항)
파이썬을 모르는 사람에게 이 프로그램 자체를 공유하거나, 단독 실행 파일로 묶어 편하게 쓰고 싶다면 `PyInstaller`를 사용해 패키징할 수 있습니다.
```bash
pyinstaller --onefile --windowed card_builder.py
```
성공적으로 빌드가 완료되면 `dist/` 폴더에 `card_builder.exe` 파일이 생성됩니다. 이 파일만 있으면 어떤 윈도우 PC에서든 더블 클릭으로 실행할 수 있습니다.

---

## 🛠️ 기술 스택 (Tech Stack)
- **Python 3.x**
  - Tkinter: 애플리케이션 데스크탑 GUI 구축
  - Pillow(PIL): 이미지 리사이징 및 평균 색상(Average Color) 분석
- **HTML5 / CSS3 / Vanilla JS**
  - Audio Visualizer 및 Raindrop Canvas 애니메이션

## 📄 라이선스 (License)
This project is licensed under the MIT License.
