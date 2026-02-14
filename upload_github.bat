@echo off
chcp 65001 > nul
echo ================================================================================
echo 보이니치 프로젝트 GitHub 업로드
echo ================================================================================
echo.

cd /d "E:\Ai project\보이니치"

REM Git 초기화 확인
if not exist ".git" (
    echo [1/5] Git 저장소 초기화...
    git init
    echo.
) else (
    echo [1/5] Git 저장소 이미 초기화됨
    echo.
)

REM 원격 저장소 설정
echo [2/5] 원격 저장소 설정...
git remote remove origin 2>nul
git remote add origin https://github.com/yoohyunseog/koreaninternet-voynich-nb.git
echo.

REM .gitignore 생성
echo [3/5] .gitignore 생성...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # Virtual Environment
echo .venv/
echo venv/
echo ENV/
echo env/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo desktop.ini
) > .gitignore
echo.

REM 파일 추가
echo [4/5] 파일 추가 중...
git add voynich_analyzer.py
git add advanced_nb_calculator.py
git add language_database.py
git add voynich_data.txt
git add README.md
git add run_voynich.bat
git add upload_github.bat
git add .gitignore
echo.

REM 커밋
echo [5/5] 커밋 생성...
git commit -m "보이니치 필사본 n/b 코드 분석 시스템 - 고급 알고리즘 버전

- JavaScript bitCalculation.v.0.2.js를 Python으로 완전 포팅
- BIT_MAX_NB, BIT_MIN_NB 고급 알고리즘 구현
- 코사인 유사도, Levenshtein 거리 통합
- 304개 다국어 단어 데이터베이스 (한국어, 영어, 라틴어)
- 보이니치 문장 번역 기능 (10단어 문장 완전 번역)
- 평균 유사도 87%% 달성
- 캐싱 최적화로 빠른 분석"
echo.

echo ================================================================================
echo GitHub 푸시 준비 완료!
echo ================================================================================
echo.
echo 다음 명령어를 실행하여 업로드하세요:
echo.
echo    git push -u origin main
echo.
echo 또는
echo.
echo    git push -u origin master
echo.
echo (저장소의 기본 브랜치에 따라 선택)
echo.
echo GitHub 인증이 필요할 수 있습니다.
echo Personal Access Token을 사용하는 것을 권장합니다.
echo.
echo ================================================================================
pause
