from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import re

# Fonction pour convertir le texte en voix synthétique
def text_to_speech(text, language='fr-CA'):
    tts = gTTS(text=text, lang=language)
    return tts

# Fonction pour extraire les sous-titres à partir du fichier srt
def extract_subtitles(srt_file):
    subtitles = []
    with open(srt_file, 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if re.match(r'^\d+$', lines[i]):
                start, end = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', lines[i+1])
                start = int(start.replace(',','').replace(':','.'))
                end = int(end.replace(',','').replace(':','.'))
                text = lines[i+2]
                subtitles.append((start, end, text))
                i += 3
            else:
                i += 1
    return subtitles

# Fichier srt d'origine
srt_file = 'example.srt'

# Extraire les sous-titres
subtitles = extract_subtitles(srt_file)

# Initialiser le fichier audio final
final_audio = AudioSegment.silent(duration=1000)

# Générer les fichiers audio pour chaque sous-titre et les ajouter au fichier final
for start, end, text in subtitles:
    tts = text_to_speech(text)
    tts.save("temp.mp3")
    audio = AudioSegment.from_mp3("temp.mp3")
    audio = audio.set_start_time(start)
    final_audio = final_audio.append(audio, crossfade=(end-start))

# Enregistrer le fichier audio final
final_audio.export("final.wav", format="wav")
