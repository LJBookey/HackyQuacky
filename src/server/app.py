from flask import *  
from flask_cors import CORS
import os
from pydub import AudioSegment
import csv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "/tmp/duck_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

data = {
    1: {"english": "Hello"},
    2: {"english": "World"}
}

@app.route('/')  
def main():  
    return render_template("translate.html")  

@app.route('/upload/audio', methods = ['POST'])  
def uploadAudio():
  audio_file = request.files.get('audio_data')
  target_path = os.path.join(UPLOAD_FOLDER, "myAudioFile.webm")
  audio_file.save(target_path)

  convertFromWebmToWav(target_path)

  print("Ducky say: The problem is in the code")
  response = numbersToMessage([1,2], "english")
  return jsonify(response)

def convertFromWebmToWav(target_path):
  sound = AudioSegment.from_file(target_path)
  sound.export(os.path.join(UPLOAD_FOLDER, "Audio.wav"), format="wav")

def numbersToMessage(clusters, language="english"):
  results = []
  for num in clusters:
    if num in data:
      phrase = data[num].get(language, data[num]["english"])
      results.append(phrase)
    else:
      results.append("Quack? (Message not found)")
  return {
      "status": "ok",
      "response": " ".join(results)
  }

def load_translations(filename="server/translations.csv"):
    translations = {}
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            translations[i] = row
    return translations

if __name__ == '__main__':  
    app.run(debug=True, use_reloader=False)