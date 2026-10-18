@echo off
REM Phantom Storm v2.5 - Demo Script for Windows
REM This script helps you quickly test the tool

echo ========================================
echo   Phantom Storm v2.5 - Quick Demo
echo ========================================
echo.

echo This demo will test the tool against localhost
echo Make sure you have a web server running on port 8080
echo.

echo Press any key to continue or Ctrl+C to cancel...
pause > nul

echo.
echo Starting demo attack (20 threads, no spoofing for localhost)...
echo Press Ctrl+C to stop
echo.

python phantom_storm.py 127.0.0.1 8080 20 --no-spoof

echo.
echo Demo finished!
pause
