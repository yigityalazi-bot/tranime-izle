@echo off
chcp 65001 > nul
title TRAnime Sunucusunu Durdur

echo [*] TRAnime sunucusu (Port 5000) kontrol ediliyor...
set found=0

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo [*] PID: %%a sonlandiriliyor...
    taskkill /F /PID %%a > nul 2>&1
    set found=1
)

if %found%==1 (
    echo [✓] TRAnime Flask sunucusu basariyla durduruldu.
) else (
    echo [i] Calisan bir TRAnime sunucusu bulunamadi.
)

timeout /t 3 > nul

