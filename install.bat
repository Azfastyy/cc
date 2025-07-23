@echo off
echo Installation des dépendances Python...
python -m pip install --upgrade pip
pip install PyQt6 psutil requests
echo.
echo ✅ Installation terminée.
pause
