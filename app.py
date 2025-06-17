from flask import Flask, request, url_for, redirect, render_template, send_file
from dotenv import load_dotenv
import oracledb
import datetime
import pandas as pd
import io
import platform
import os


# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_dsn = os.getenv('DB_DSN')

# Database connection details
db_config = {
    #"user": "",
    #"password": "",
    #"password": "",
    #"dsn": ""
    #"dsn": ""
    #"dsn": ""    
}

# Function to get a database connection
def get_db_connection():
    oracledb.init_oracle_client(lib_dir=r"C:\Apps\instantclient-basic\instantclient_23_7")
    # connection = oracledb.connect(
    #     user=db_config["user"],
    #     password=db_config["password"],
    #     dsn=db_config["dsn"]
    connection = oracledb.connect(
        user=db_user,
        password=db_password,
        dsn=db_dsn
    )
    #cursor = connection.cursor()
    #cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")
    #cursor.close()
    return connection

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handle_action', methods=['POST'])
def handle_action():
    action = request.form['action']
    print(f'Received input - Date: {action}')
    #action = request.form.get('action')
    status_input = request.form.get('status_input')
    date_input = request.form.get('date_input')
    todate_input = request.form.get('todate_input')
    if action == 'payments':
        return redirect(url_for('indexdata', date_input=date_input, status_input=status_input, todate=todate_input))
    elif action == 'fileupload':
        return redirect(url_for('fileupload', date_input=date_input, todate=todate_input))
    elif action == 'cancel':
        return redirect(url_for('index'))



@app.route('/download', methods=['POST'])
def download_file():
    # Get the data from the request (assuming it's sent as JSON)
    data = request.json
    print(f'download input - Date: {data}')
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Create a BytesIO buffer to hold the Excel file
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer: 
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='data.xlsx')

@app.route('/fileupload', methods=['GET', 'POST'])
def fileupload():
    uploaddata = []
    noResult = ""
    #if request.method == 'POST':
    try:
            #status_input = request.args.get('status_input')
           #print(f'Received input - Status: {status_input}')
            
            #date_input = request.form.get('date_input')
            date_input = request.args.get('date_input')
            print(f'Received input - Date: {date_input}')
            print(type(date_input))

            todate_input =  request.args.get('todate')
            print(f'Received input - To Date: {todate_input}')
            print(type(todate_input))
            #x = datetime.date.fromisoformat(date_input)
            #dat = datetime.datetime.strftime(x,"%Y/%m/%d")
            #print(f'Received input - Date: {dat}')
            connection = get_db_connection()
            cursor = connection.cursor()
            query = """
           
            """
            
            print(f'query - query: {query}')
            print(f'Parameters - input_date: {date_input}, input_todate: {todate_input}')
            cursor.execute(query,  input_date=date_input , input_todate=todate_input)
            
            results = cursor.fetchall()
            print(type(results))
            # Convert the data to a list of dictionaries
            print(f'Query executed successfully, fetched {len(results)} results')
            for row in results:
                uploaddata.append({
                    "uploaddate": row[0],
                    "Time": row[1],
                    "fps": row[2],
                    "fps_sdmc": row[3],
                    "bacs": row[4],
                    "bacs_sdmc": row[5],
                    "chaps": row[6],
                    "sepact": row[7],
                    "international": row[8],
                    "igt": row[9]
                # Add more columns as needed
            })
            print(f'data - data: {uploaddata}')
           
            if len(results) == 0:
                noResult = "none"
            cursor.close()
            connection.close()
            print(f'noResult - data: {noResult}')
           
            return render_template('index.html', uploaddata=uploaddata, results=results, noResult=noResult, reportType='file_upload', toDateInput=todate_input, dateInput=date_input )
    except Exception as e:
            return str(e)
    return render_template('index.html')


@app.route('/indexdata')
def indexdata():
    dataComplete = []
    datePending = []
    noResult = ""
    if request.method == 'GET':
        try:
                #status_input = request.form.get('status_input')
                status_input = request.args.get('status_input')
                print(f'Received input - Status: {status_input}')
                
                #date_input = request.form.get('date_input')
                date_input = request.args.get('date_input')
                print(f'Received input - Date: {date_input}')
                print(type(date_input))

                todate_input =  request.args.get('todate')
                print(f'Received input - To Date: {todate_input}')
                print(type(todate_input))
                #x = datetime.date.fromisoformat(date_input)
                #dat = datetime.datetime.strftime(x,"%Y/%m/%d")
                #print(f'Received input - Date: {dat}')
                connection = get_db_connection()
                cursor = connection.cursor()
                if status_input == 'Completed':
                    query = """
                       
                    """
                    print(f'query - query: {query}')
                    print(f'Parameters - input_date: {date_input}, status_input: {status_input}')
                    cursor.execute(query,  input_date=date_input, input_todate=todate_input )
                    
                    results = cursor.fetchall()
                    
                    # Convert the data to a list of dictionaries
                    print(f'Query executed successfully, fetched {len(results)} results')

                    for row in results:
                        dataComplete.append({
                            "date": row[0],
                            "time": row[1],
                            "count": row[2],
                            "mop": row[3],
                            "sum": row[4],
                            "currency": row[5],
                            "status": row[6]
                        # Add more columns as needed
                    })
                    print(f'data - data: {dataComplete}')
                    if len(results) == 0:
                        noResult = "none"
                    cursor.close()
                    connection.close()
                    print(f'noResult - data: {noResult}')
                    return render_template('index.html', dataComplete=dataComplete, results=results, noResult=noResult, reportType='payment_completed', dateInput=date_input, statusInput=status_input, toDateInput=todate_input)
                elif status_input == 'APPROVAL_PENDING':
                    query = """
                        
                    """
                    print(f'query - query: {query}')
                    print(f'Parameters - input_date: {date_input}, status_input: {status_input}')
                    cursor.execute(query,  input_date=date_input, input_todate=todate_input ,input_status=status_input, )
                    
                    results = cursor.fetchall()
                    
                    # Convert the data to a list of dictionaries
                    print(f'Query executed successfully, fetched {len(results)} results')

                    for row in results:
                        dataPending.append({
                            "mop": row[0],
                            "status": row[1],
                            "datecreate": row[2],
                            "datedue": row[3],
                            "count": row[4]
                        # Add more columns as needed
                    })
                    print(f'data - data: {dataPending}')
                    if len(results) == 0:
                        noResult = "none"
                    cursor.close()
                    connection.close()
                    print(f'noResult - data: {noResult}')
                    return render_template('index.html', dataPending=dataPending, results=results, noResult=noResult, reportType='payment_completed', dateInput=date_input, statusInput=status_input, toDateInput=todate_input)
        except Exception as e:
            return str(e)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
