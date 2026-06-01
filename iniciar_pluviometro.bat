@echo off
:: Inicia o Backend
start "Backend API" cmd /k "cd /d C:\Users\ResTIC55\pluviometro\backend-api && call venv\Scripts\activate && python main.py"

:: Inicia o Frontend
start "Frontend Web" cmd /k "cd /d C:\Users\ResTIC55\pluviometro\web-frontend\emj-react && npm run dev"

echo Ambos os servicos estao sendo iniciados...
pause