@echo off
echo 🏦 MoMo Data Analysis Dashboard
echo ========================================
echo.

echo 🔄 Installing Python dependencies...
cd backend
pip install -r requirements.txt

echo.
echo 🔄 Processing XML data and populating database...
python data_processor.py

echo.
echo 🚀 Starting Flask API server...
echo 📊 Dashboard will be available at: http://localhost:5000
echo 🌐 Open frontend/index.html in your browser to view the dashboard
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo.

python api.py

pause