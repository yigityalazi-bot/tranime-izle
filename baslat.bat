@echo off
chcp 65001 > nul
title TRAnime Flask Sunucusu
color 0C

echo ===================================================================
echo               TRAnime - Yerel Sunucu Baslatici
echo ===================================================================
echo.

:: 1. Calisma dizinine gec
cd /d "%~dp0"

:: 2. Gerekli Python kutuphanelerini yukle / kontrol et
echo [*] Gerekli kutuphaneler kontrol ediliyor (Flask, Flask-SQLAlchemy)...
python -m pip install Flask Flask-SQLAlchemy > nul 2>&1
if %errorlevel% neq 0 (
    py -m pip install Flask Flask-SQLAlchemy > nul 2>&1
)

:: 3. 2 saniye sonra tarayiciyi otomatik olarak ac
echo [*] Tarayici 127.0.0.1:5000 adresine yonlendiriliyor...
start "" "http://127.0.0.1:5000"

:: 4. Flask sunucusunu calistir
echo [*] Flask sunucusu baslatiliyor...
echo [!] Sunucuyu durdurmak icin bu pencereyi kapatabilirsiniz.
echo.
python app.py
if %errorlevel% neq 0 (
    echo.
    echo [*] 'python' komutu basarisiz oldu, 'py' ile tekrar deneniyor...
    py app.py
)

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Python calistirilamadi! Lutfen bilgisayarinizda Python'in kurulu oldugundan emin olun.
    pause
)
