#from distutils.log import debug
from fileinput import filename
from flask import *  
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = "uploads"

@app.route('/')  
def main():  
    return render_template("translate.html")  

@app.route('/upload/audio', methods = ['POST'])  
def uploadAudio():

  audio_file = request.files.get('audio_data')
  filename = "myAudioFile.webm"
  
  target_path = os.path.join(UPLOAD_FOLDER, filename)
  audio_file.save(target_path)

  # I think we can put the stuff for translating here 
  print ("Ducky say: The problem is in the code")
  return jsonify({"status": "ok", "response": "Ducky say: The problem is in the code"})


if __name__ == '__main__':  
    app.run()