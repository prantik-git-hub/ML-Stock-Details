Setup Instructions 
1. Install Python 3.10 or above. 
2. Create and activate a virtual environment. 
3. Install dependencies using: ```pip install -r requirements.txt ```

Project Structure
```
finance/app_config.py 
finance/requirements.txt 
finance/run.py 
finance/app/analyze.py 
finance/app/forms.py 
finance/app/models.py 
finance/app/routes.py 
finance/app/utils.py 
finance/app/views.py 
finance/app/ init .py 
finance/app/templates/analysis.html 
finance/app/templates/index.html
finance/app/templates/results.html 
finance/app/  pycache  /analyze.cpython-313.pyc 
finance/app/  pycache  /fetch_data.cpython-313.pyc 
finance/app/  pycache  /forms.cpython-313.pyc 
finance/app/  pycache  /models.cpython-313.pyc 
finance/app/  pycache  /routes.cpython-313.pyc 
finance/app/  pycache  /utils.cpython-313.pyc 
finance/app/  pycache  /views.cpython-313.pyc 
finance/app/  pycache  / init  .cpython-313.pyc 
finance/scripts/db_utils.py 
finance/scripts/fetch_data.py 
finance/scripts/ml_analysis.py 
finance/uploads/test.json 
finance/  pycache  /app_config.cpython-313.pyc 
finance/  pycache  /config.cpython-313.pyc 
```
Running the Application 
Use the command: 
```
python run.py
``` 
This will start the Flask development server. Access the app via ``` http://127.0.0.1:5000/ ``` in your browser. 
6. Usage Guide 
1. Navigate to the homepage. 
2. Enter financial data or select a stock for analysis. 
3. Click 'Analyze' to trigger backend logic. 
4. Results will be displayed in a results template. 
6. Troubleshooting - If dependencies fail, ensure pip and Python are up to date. - If app fails to start, verify Flask is installed and `run.py` has correct imports. - Check logs printed in the console for specific errors. 
