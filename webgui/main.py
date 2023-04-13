from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
from zscaller.caller import ZSession, MissingEnvironmentVariable
import os
import io
from werkzeug.utils import secure_filename

# Define allowed files
ALLOWED_EXTENSIONS = {'csv','xlsx','.xls'}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def url_categories():
    if request.method == 'POST':
    # upload file flask
        f = request.files.get('file')
        # validate the file type.
        if f.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(f.stream.read())
        elif f.content_type == 'text/csv':
            df = pd.read_csv(f.stream)
        else:
            return Response(f"{f.content_type} is not an accepted file format",status=415, mimetype='application/json')
        # API creds MUST be set to the View README.MD 
        try:
            zs = ZSession()
        # raise error if api creds are not set in the flask environment.
        except MissingEnvironmentVariable as e:
            raise Response(f"ZSession API creds not set to the environment. Refer to README.MD",status=500, mimetype='application/json')
        # check to see if url header is in file.
        df.columns = [i.lower() for i in df.columns]
        if 'url' not in df.columns:
            raise Response(f"'url' header was not found in {f.filename}. Refer to README.MD",status=500, mimetype='application/json')
        urls = df['url'].drop_duplicates().to_list()
        
            
        result = zs.url_lookup(urls)
        data=io.StringIO()
        pd.DataFrame(result).to_csv(data,index=False)
        output = make_response(data.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=urlLookup.csv"
        output.headers["Content-type"] = "text/csv"
        # render_template("main.html",message='Parse Complete!')
        return output
        
    return render_template(
        "main.html"
        ,message='Choose file of URLs to lookup. The file MUST contain a column of URLs with header name "url".'
        )


# @app.route('/show_data')
# def showData():
#     # Uploaded File Path
#     data_file_path = session.get('uploaded_data_file_path', None)
#     # read csv
#     uploaded_df = pd.read_csv(data_file_path,
#                             encoding='unicode_escape')
#     # Converting to html Table
#     uploaded_df_html = uploaded_df.to_html()
#     return render_template('show_csv_data.html',
#                         data_var=uploaded_df_html)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0",debug=False)
