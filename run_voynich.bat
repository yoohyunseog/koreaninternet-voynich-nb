@echo off
chcp 65001 > nul
echo ====================================
echo 보이니치 문서 분석 시스템 실행
echo ====================================
echo.

REM 가상환경 활성화
echo [1/2] 가상환경 활성화 중...
call E:\python_env\Scripts\activate.bat

REM 작업 디렉토리 변경
cd /d "E:\Ai project\보이니치"

REM 프로그램 실행
echo [2/2] 보이니치 분석 프로그램 실행...
echo.
python voynich_analyzer.py

echo.
echo ====================================
echo 실행 완료!
echo ====================================
pause
