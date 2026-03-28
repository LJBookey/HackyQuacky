const recordingButton = document.getElementById("recordingBttn");
const audioList = document.getElementById("audioList");
const audioPlayer = document.getElementById("audioPlayer");

let mediaRecorder;
let audioChunks = [];

console.log("JavaLoaded")
startRecording = false;

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ audio: true})

        .then(function (stream) {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = function () {
                const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType });
                uploadBlob(audioBlob);
                const audioURL = URL.createObjectURL(audioBlob);
                const listItem = document.createElement('li');
                const audioLink = document.createElement('a');
                audioLink.href = audioURL;
                audioLink.download = 'audio.wav';
                audioLink.textContent = 'Download Audio';
                listItem.appendChild(audioLink);
                audioList.appendChild(listItem);
                audioPlayer.src = audioURL;
                audioChunks = [];

                
            };

            recordingButton.addEventListener('click', function () {
                if (startRecording == false) {
                    startRecording = true;
                    audioChunks = [];
                    mediaRecorder.start();
                    document.getElementById('duckImg').src='duckThinking.gif'
                    recordingButton.src='startRecording.png'
                }

                else {
                    mediaRecorder.stop();
                    startRecording = false;
                    document.getElementById('duckImg').src='duckSpeaking.gif'
                    recordingButton.src='stopRecording.png'
                }
            });

        })
        .catch(function (error) {
            console.error("Error accessing the microphone: " + error);
        });
    
    } else {
        console.error("Browser doesn't support audio recording");
    }



async function uploadBlob(audioBlob) {
    const formData = new FormData();
    formData.append('audio_data', audioBlob, 'audio.webm');

    const apiUrl = "http://127.0.0.1:5000/upload/audio"

    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            throw new Error("Server error");
        }

        const data = await res.json();
        console.log("Upload success:", data);

    } catch (err) {
        console.error("Upload failed:", err);
    }
}