from pathlib import Path
import shutil
import librosa
import glob, os


def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, title[0:title.index(" ")] + ext))


if __name__ == '__main__':
    rename("data\\audioFiles", "XC*", "%s")
