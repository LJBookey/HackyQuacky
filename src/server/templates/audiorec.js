const startRecordingButton = document.getElementById("startRecording");
const stopRecordingButton = document.getElementById("stopRecording");
const audioList = document.getElementById("audioList");
const audioPlayer = document.getElementById("audioPlayer");

let mediaRecorder;
let audioChunks = [];

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
                const audioBlob = new Blob(audioChunks, { 'type': 'audio/wav'});
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

        
        })
        .catch(function (error) {
            console.error("Error accessing the microphone: " + error);
        });
    
    } else {
        console.error("Browser doesn't support audio recording");
    }

startRecordingButton.addEventListener('click', function () {
    audioChunks = [];
    mediaRecorder.start();
    startRecordingButton.disabled = true;
    stopRecordingButton.disabled = false;
});

stopRecordingButton.addEventListener('click', function () {
    mediaRecorder.stop();
    startRecordingButton.disabled = false;
    stopRecordingButton.disabled = true;
})
