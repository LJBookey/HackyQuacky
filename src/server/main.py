from distutils.log import debug
from fileinput import filename
from flask import *  
import os


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

@app.route('/')  
def main():  
    return render_template("translate.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(filepath)  
        return render_template("translate.html", name = f.filename)

if __name__ == '__main__':  
    app.run(debug=True)