@echo off
chcp 65001 > nul
echo ====================================
echo 보이니치 문서 분석 시스템 실행
echo ====================================
echo.

REM 프로젝트 경로 설정
set "PROJECT_DIR=%~dp0.."
for %%I in ("%PROJECT_DIR%") do set "PROJECT_DIR=%%~fI"

REM 가상환경 활성화 (있을 때만)
echo [1/2] 가상환경 활성화 중...
if exist "%PROJECT_DIR%\.venv\Scripts\activate.bat" (
	call "%PROJECT_DIR%\.venv\Scripts\activate.bat"
) else (
	echo .venv가 없어 시스템 Python으로 실행합니다.
)

REM 작업 디렉토리 변경
cd /d "%PROJECT_DIR%"

REM 프로그램 실행
echo [2/2] 보이니치 분석 프로그램 실행...
echo.
python "%PROJECT_DIR%\src\voynich_analyzer.py"

echo.
echo ====================================
echo 실행 완료!
echo ====================================
pause
