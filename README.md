# 최유찬 연구 홈페이지

촉각 센서와 웨어러블 로봇 연구를 소개하는 정적 홈페이지입니다. 배포 대상은 **[youchan0902/youchan0902.github.io](https://github.com/youchan0902/youchan0902.github.io)**이며, 게시 후 GitHub Pages 주소는 `https://youchan0902.github.io/`입니다.

## 수정 및 미리보기

Python 3 표준 라이브러리만 사용하므로 별도 패키지 설치가 필요하지 않습니다.

```sh
python scripts/build.py
python -m http.server 8000 --directory dist
```

브라우저에서 `http://localhost:8000`을 열어 확인합니다.

- `content/projects.json`: 연구별 설명, 수치, 이미지 및 캡션
- `content/cv.json`: 연구자 소개, 학력, 연구 경험 및 기술
- `src/`: 공통 스타일과 브라우저 동작
- `scripts/build.py`: 홈페이지, 연구 상세 페이지 및 CV 페이지 생성
- `dist/`: 배포할 HTML, CSS, JavaScript 및 이미지
- `dist/assets/`: 공개 페이지에 사용하는 선별 이미지
- `dist/media/fingertip-demo.mp4`: 1080p 손끝 센서 실험 영상 (약 11 MB)
- `dist/documents/CV_YouchanChoi.pdf`: 제공된 CV 원본; `cv.html`에서 보기 및 다운로드

설명과 화면 구성을 수정한 뒤 빌드를 다시 실행합니다. `dist/`에는 배포용 이미지 파일이 포함되어 있으므로 폴더 전체를 삭제하지 않습니다. 생성된 HTML을 직접 수정하면 다음 빌드에서 덮어쓰게 됩니다.

## GitHub Pages 설정

1. **youchan0902 계정**으로 로그인하고, 해당 계정 소유의 공개 저장소 `youchan0902.github.io`를 만듭니다. 새 저장소라면 README나 라이선스를 자동 추가하지 않은 빈 저장소로 시작합니다.
2. 이 프로젝트 파일을 저장소의 `main` 브랜치에 업로드합니다. `dist/assets/`와 `.github/workflows/pages.yml`도 포함합니다.
3. 저장소의 **Settings → Pages → Build and deployment → Source**에서 **GitHub Actions**를 직접 선택합니다. 워크플로만 추가해도 Pages가 자동 활성화되는 것은 아닙니다.
4. **Actions → Deploy research website to GitHub Pages → Run workflow**를 실행합니다. 이후 `main`에 변경 사항을 push하면 자동으로 빌드하고 배포합니다.

빌드 작업은 소스 읽기 권한만 사용하고, 배포 작업에만 Pages 쓰기 및 OIDC 권한을 부여합니다. 자세한 설정은 [GitHub Pages 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)를 참고하세요.

## 연구 이미지

연구 자료에서 선별한 사진과 도식을 사용합니다. 홈페이지 배경에 맞춘 사진 편집은 배경에 한정하며, 기존 연구 원본 파일은 수정하지 않습니다. CAD, 실물 사진, 시뮬레이션 결과와 측정 결과는 각 설명에서 구분합니다. 개인 문서와 작업용 자료를 저장소 전체에 추가하지 않고, 공개에 필요한 파일만 유지합니다.
