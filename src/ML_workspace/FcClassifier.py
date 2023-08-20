from enum import Enum
from keras.models import load_model 
import librosa
import librosa.display
import numpy as np
from PIL import Image
class Predictions(Enum):
    HFC = "HFC"
    LFC = "LFC"

class fcClassifier(object):
    Model = load_model(rf"src\ML_workspace\models\model.h5")
    def __init__(self, FileID: str) -> None:
        self.File = FileID
        self.PATH = rf"../FILES/audio/{self.File}"

    def Predict(self):
        try:
            frequecy = self.predict(self.PATH)
            return {
                "predictions": frequecy
            }
        except Exception as e:
            print('Exception:', e)
            return {"error" : e}

    
    def scale_melspec(mel_spec):
        target_size = (90, 200)  # Target size for mel spectrograms
        # Scale mel spectrogram using PIL
        scaled_mel_spec = librosa.util.normalize(mel_spec)  # Normalize mel spectrogram
        scaled_mel_spec = (scaled_mel_spec * 255).astype(np.uint8)  # Convert to uint8
        scaled_mel_spec = Image.fromarray(scaled_mel_spec)  # Convert to PIL image
        scaled_mel_spec = scaled_mel_spec.resize(target_size, Image.ANTIALIAS)  # Resize
        scaled_mel_spec = np.array(scaled_mel_spec)
        print(scaled_mel_spec.shape)

        return scaled_mel_spec
    
    def predict(WAV):
        scale,sr=librosa.load(WAV)
        mel_spec=librosa.feature.melspectrogram(y=scale,sr=sr,n_fft=2048,hop_length=512,n_mels=90)
        mel_spec=fcClassifier.scale_melspec(mel_spec)
        #print(mel_spec.shape)
        log_mel_spectrogram=librosa.power_to_db(mel_spec)
        log_mel_spectrogram=np.repeat(log_mel_spectrogram[...,np.newaxis],3,axis=-1)
        log_mel_spectrogram = np.expand_dims(log_mel_spectrogram, axis=0)
        #print(log_mel_spectrogram.shape)

        prediction=(fcClassifier.Model.predict(log_mel_spectrogram))
        if prediction[0]>0.5:
            return Predictions.HFC
        return Predictions.LFC
    def __repr__(self) -> str:
        return "True"
