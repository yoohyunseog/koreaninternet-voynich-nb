@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0\.."

echo.
echo ===================================
echo   Voynich Manuscript Analysis
echo ===================================
echo.

REM Check if Python virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found. Please run setup first.
    pause
    exit /b 1
)

echo [Step 1] Generating English n/b metrics...
.\.venv\Scripts\python.exe src\english_nb_words_to_json.py
if errorlevel 1 (
    echo ERROR: Failed to generate English n/b metrics.
    pause
    exit /b 1
)
echo [✓] English n/b metrics generated successfully.
echo.

echo [Step 2] Matching Voynich to English and translating with GPT...
.\.venv\Scripts\python.exe src\english_sentence_from_nb_json.py
if errorlevel 1 (
    echo ERROR: Failed to match and translate.
    pause
    exit /b 1
)
echo [✓] Voynich-English matching and GPT translation completed.
echo.

echo [Step 3] Generating HTML interpretation...
.\.venv\Scripts\python.exe src\voynich_html_generator.py
if errorlevel 1 (
    echo ERROR: Failed to generate HTML.
    pause
    exit /b 1
)
echo [✓] HTML interpretation generated successfully.
echo.

echo ===================================
echo   Pipeline Completed Successfully!
echo ===================================
echo.
echo Output files:
echo   - outputs\english_nb_words.json
echo   - outputs\voynich_to_english_sentence.txt
echo   - voynich_interpretation.html (NEW)
echo   - index.html
echo.
echo Open voynich_interpretation.html or index.html in your browser.
echo.
pause
