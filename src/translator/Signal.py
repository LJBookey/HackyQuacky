import librosa as lb
import librosa.display as lbdis
import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, path):
        self.audio_path = path
        self.waveform = None
        self.sample_rate = None
        self.duration = None
        self.chunks = []
        self.spec_chunks = []
    
    
    def load_audio(self):
        self.waveform, self.sample_rate = lb.load(self.audio_path, sr=None)
        self.duration = lb.get_duration(y=self.waveform, sr=self.sample_rate)

        #gatta be done
    def chunk_up_the_wav(self, chunk_size_seconds):

        if self.waveform == None:
            self.load_audio()

        #calculates the length of a chunk
        chunk_length = self.sample_rate * chunk_size_seconds

        num_chunks = int(np.ceil(len(self.waveform) / chunk_length))
        
        for i in range(num_chunks):
            t = self.waveform[i * chunk_length: (i + 1) * chunk_length]
            self.chunks.append(np.array(t))
        

    def chunks_to_specs(self):
        for chunk in self.chunks:
            self.spec_chunks.append(self.generate_spectrogram(chunk))

    def save_chunks(self, folder="data/spec_chunks"):
        name = self.audio_path[self.audio_path.rindex("\\"):self.audio_path.index(".")]

        # path = f"{folder}/{name}_{1}"
        # self.save_spectrogram(self.spec_chunks[0], path)

        for i, chunk in enumerate(self.spec_chunks):
            path = f"{folder}/{name}_{i}"
            self.save_spectrogram(chunk, path)


    def generate_spectrogram(self, chunk):  
        # orignal 1024, 512
        spec = lb.stft(chunk, n_fft=4096, hop_length=512)
        spec = abs(spec) ** 2

        return spec
        
    def save_spectrogram(self, spec, image_path):
        #plt.figure(figsize=(14, 5))
        
        plt.figure()

        lbdis.specshow(spec, sr=self.sample_rate, x_axis='time', y_axis='log')

        plt.axis('off')
        plt.tight_layout()
        plt.savefig(image_path, bbox_inches="tight", pad_inches=0.0)

        plt.close()

if __name__ == "__main__":
    sig = Signal("data\\audioFiles\\XC196999 - Mallard - Anas platyrhynchos.mp3")
    sig.chunk_up_the_wav(2)
    sig.chunks_to_specs()
    sig.save_chunks()
    
