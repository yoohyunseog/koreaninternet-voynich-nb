@echo off
chcp 65001 > nul
echo ================================================================================
echo 보이니치 프로젝트 GitHub 업데이트
echo ================================================================================
echo.

set "PROJECT_DIR=%~dp0.."
for %%I in ("%PROJECT_DIR%") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"

REM 가상환경 활성화
call .venv\Scripts\activate.bat

REM Python 자동화 스크립트 실행
echo [1/6] GPT 이야기 풀이 생성 중...
python src\create_gpt_story.py
if errorlevel 1 (
    echo ⚠️ GPT 이야기 생성 실패 (진행)
) else (
    echo ✓ GPT 이야기 풀이 생성 완료
)
echo.

echo [2/6] 보이니치 원문 섹션 추가 중...
python src\update_voynich_text.py
if errorlevel 1 (
    echo ⚠️ 보이니치 원문 섹션 추가 실패 (진행)
) else (
    echo ✓ 보이니치 원문 섹션 추가 완료
)
echo.

REM 변경사항 확인
echo [3/6] 변경된 파일 확인...
git status
echo.

REM 커밋 메시지 설정 (자동)
set commit_msg=보이니치 분석: GPT 이야기 및 원문 섹션 업데이트
echo.

REM 모든 변경사항 추가
echo [4/6] 변경사항 추가 중...
git add .
echo.

REM 커밋
echo [5/6] 커밋 생성 중...
git commit -m "%commit_msg%"
echo.

REM 푸시
echo [6/6] GitHub에 푸시 중...
git push origin main
echo.

echo ================================================================================
echo ✅ GitHub 업로드 완료!
echo ================================================================================
echo.
echo 저장소 주소: https://github.com/yoohyunseog/koreaninternet-voynich-nb
echo.
pause
