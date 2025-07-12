# Installation Guide - MoMo Data Analysis Dashboard

## Quick Start (Windows)

### Option 1: Automated Setup (Recommended)
1. Double-click `run.bat` file
2. Wait for installation and data processing to complete
3. Open `frontend/index.html` in your browser when the server starts

### Option 2: Manual Setup

#### Step 1: Install Python Dependencies
```cmd
cd backend
pip install -r requirements.txt
```

#### Step 2: Process Data
```cmd
python data_processor.py
```

#### Step 3: Start API Server
```cmd
python api.py
```

#### Step 4: Open Dashboard
Open `frontend/index.html` in your web browser

## Detailed Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Chart.js CDN)

### Verification Steps

#### 1. Verify Python Installation
```cmd
python --version
```
Should show Python 3.8 or higher

#### 2. Verify Data Processing
After running the data processor, you should see:
- `momo_transactions.db` file created in backend folder
- Log message: "Processing complete: X transactions processed"

#### 3. Verify API Server
When API server starts, you should see:
```
* Running on http://127.0.0.1:5000
```

#### 4. Verify Dashboard
Open browser and navigate to the frontend folder, then open `index.html`
- Dashboard should load with statistics cards
- Charts should display transaction data
- Search and filter functions should work

### Troubleshooting

#### Common Issues

**Issue**: "Module not found" error
**Solution**: 
```cmd
cd backend
pip install -r requirements.txt
```

**Issue**: "No such file or directory" error
**Solution**: Make sure you're running commands from the correct directory

**Issue**: Dashboard shows "Loading..." indefinitely
**Solution**: 
1. Ensure API server is running on port 5000
2. Check browser console for errors
3. Verify database was created successfully

**Issue**: Charts not displaying
**Solution**: 
1. Check internet connection (Chart.js loads from CDN)
2. Ensure API is returning data
3. Check browser console for JavaScript errors

#### Port Conflicts
If port 5000 is already in use, modify `api.py`:
```python
app.run(debug=True, port=5001)  # Change to different port
```

Then update the API base URL in `frontend/script.js`:
```javascript
this.apiBase = 'http://localhost:5001/api';
```

### File Structure Verification
After installation, your project should look like:
```
momo-data-analysis/
├── backend/
│   ├── momo_transactions.db ✓ (created after data processing)
│   ├── data_processing.log ✓ (created after data processing)
│   └── unprocessed_messages.log ✓ (created after data processing)
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── data/
    └── sms_data_clean.xml
```

### Performance Expectations
- **Data Processing**: Should complete in under 10 seconds
- **API Startup**: Should start in under 5 seconds
- **Dashboard Loading**: Should load in under 3 seconds
- **Chart Rendering**: Should render in under 2 seconds

### Browser Compatibility
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### System Requirements
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 100MB available space
- **CPU**: Any modern processor
- **Network**: Internet connection for Chart.js CDN

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review log files in the backend directory
3. Check browser developer console for errors
4. Ensure all prerequisites are met

## Next Steps

After successful installation:
1. Explore the dashboard features
2. Try different search and filter combinations
3. Click on transactions to view detailed information
4. Review the generated charts and statistics

---

*For additional help, refer to the main README.md file or the project documentation.*