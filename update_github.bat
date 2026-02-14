@echo off
chcp 65001 > nul
echo ================================================================================
echo 보이니치 프로젝트 GitHub 업데이트
echo ================================================================================
echo.

cd /d "E:\Ai project\보이니치"

REM 변경사항 확인
echo [1/4] 변경된 파일 확인...
git status
echo.

REM 사용자에게 계속 진행 여부 확인
set /p continue="위 파일들을 커밋하시겠습니까? (Y/N): "
if /i not "%continue%"=="Y" (
    echo 업로드 취소됨
    pause
    exit /b
)
echo.

REM 커밋 메시지 입력
set /p commit_msg="커밋 메시지를 입력하세요: "
if "%commit_msg%"=="" (
    set commit_msg=업데이트: 보이니치 분석 시스템 개선
)
echo.

REM 모든 변경사항 추가
echo [2/4] 변경사항 추가 중...
git add .
echo.

REM 커밋
echo [3/4] 커밋 생성 중...
git commit -m "%commit_msg%"
echo.

REM 푸시
echo [4/4] GitHub에 푸시 중...
git push origin main
echo.

echo ================================================================================
echo ✅ GitHub 업로드 완료!
echo ================================================================================
echo.
echo 저장소 주소: https://github.com/yoohyunseog/koreaninternet-voynich-nb
echo.
pause
