#from distutils.log import debug
from fileinput import filename
from flask import *
from flask_cors import CORS
import os
from pydub import AudioSegment

import threading


import csv

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "../"

@app.route('/')  
def main():  
    print("asdasd")
    return render_template("translate.html")  



@app.route('/upload/audio', methods = ['POST'])  
def uploadAudio():

  audio_file = request.files.get('audio_data')
  filename = "myAudioFile.webm"

  target_path = os.path.join(UPLOAD_FOLDER, filename)  # Adjust the path as needed
  audio_file.save(target_path)
  

  # convertFromWebmToWav(target_path)

  # I think we can put the stuff for translating here 
  response = numbersToMessage([1,2], "English")

  print("Ducky say: The problem is in the code")
  return jsonify(response)

def convertFromWebmToWav(target_path):
  sound = AudioSegment.from_file(target_path)
  sound.export(os.path.join(UPLOAD_FOLDER, "Audio.wav"), format="wav")


#cluster = list of clusters 
#languge = the languge to tran
def numbersToMessage(clusters, language="English"):
  results = []
  
  for num in clusters:
    if num in data:
      phrase = data[num].get(language, data[num]["English"])
      results.append(phrase)
    else:
        results.append("Quack? (Message not found)")

  return {
      "status": "ok",
      "response": " ".join(results),
      "language": language
  }

#load in the csv of responses 
def load_translations(filename="src/server/translations.csv"):
    translations = {}
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            translations[i] = row
    return translations
  
#load the data 
data = load_translations()

if __name__ == '__main__':  
    app.run(use_reloader=False, debug=False, threaded=True)