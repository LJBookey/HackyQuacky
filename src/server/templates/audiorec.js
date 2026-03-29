const recordingButton = document.getElementById("recordingBttn");

const selectElement = document.getElementById('choices');

let mediaRecorder;
let audioChunks = [];
let duck = "englishDuck";
console.log("JavaLoaded");
let startRecording = false;

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
                console.log("YO");
                uploadBlob(audioBlob);
                audioChunks = [];
                console.log("hahaha");
            };

            recordingButton.addEventListener('click', function () {
                if (startRecording == false) {
                    startRecording = true;
                    audioChunks = [];
                    mediaRecorder.start();
                    var thinkDuck = duck + "Thinking";
                    var thinkGif = thinkDuck + ".gif";
                    document.getElementById('duckImg').src=thinkGif;
                    recordingButton.querySelector("img").src = 'startRecording.png';
                }

                else {
                    mediaRecorder.stop();
                    startRecording = false;
                    var speakDuck = duck + "Speaking"
                    var speakGif = speakDuck + ".gif";
                    document.getElementById('duckImg').src=speakGif;
                    recordingButton.querySelector("img").src = 'stopRecording.png';
                }
            });

        })
        .catch(function (error) {
            console.error("Error accessing the microphone: " + error);
        });
    
    } else {
        console.error("Browser doesn't support audio recording");
    };

async function uploadBlob(audioBlob) {
    
    const formData = new FormData();
    formData.append('audio_data', audioBlob, 'audio.webm');
    
    const apiUrl = "http://127.0.0.1:5000/upload/audio"
    
    try {
        const res = await fetch(apiUrl, {
            
            method: 'POST',
            body: formData
        });
        console.log("hello");
        if (!res.ok) {
            throw new Error("Server error");
        }

        
        const data = await res.json();
        
        console.log(data.response);
        document.getElementsByClassName("translate")[0].textContent=data.response;
        console.log("Upload success:", data);

    } catch (err) {
        console.error("Upload failed:", err);
    }
};

// window.addEventListener('beforeunload', (event) => {
//   // Cancel the event as stated by the standard.
//   event.preventDefault();
//   // Chrome requires returnValue to be set.
//   //event.returnValue = '';
// });

selectElement.addEventListener('change', function() {
    var value = selectElement.value;
    console.log(value);
    duck = value + "Duck";
    var gifDuck = duck + ".gif";
    document.getElementById('duckImg').src=gifDuck;
});
