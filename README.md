Setup Instructions 
1. Install Python 3.10 or above. 
2. Create and activate a virtual environment. 
3. Install dependencies using: ```pip install -r requirements.txt ```

Project Structure
```
finance/
├── app_config.py
├── requirements.txt
├── run.py
├── uploads/
│   └── test.json
├── scripts/
│   ├── db_utils.py
│   ├── fetch_data.py
│   └── ml_analysis.py
├── app/
│   ├── __init__.py
│   ├── analyze.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   ├── views.py
│   ├── templates/
│   │   ├── analysis.html
│   │   ├── index.html
│   │   └── results.html
│   └── __pycache__/
│       ├── analyze.cpython-313.pyc
│       ├── fetch_data.cpython-313.pyc
│       ├── forms.cpython-313.pyc
│       ├── models.cpython-313.pyc
│       ├── routes.cpython-313.pyc
│       ├── utils.cpython-313.pyc
│       ├── views.cpython-313.pyc
│       └── __init__.cpython-313.pyc
├── __pycache__/
│   ├── app_config.cpython-313.pyc
│   └── config.cpython-313.pyc

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
