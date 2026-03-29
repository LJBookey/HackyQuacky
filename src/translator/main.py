from pathlib import Path
import shutil
import librosa
import glob, os
import numpy as np


def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, title[0:title.index(" ")] + ext))

def training_split(input_dir="data/clusterings2", output_dir="data/validation"):
    input_path = Path(input_dir)

    classes = list(input_path.rglob("*"))
    
    for class_ in classes:
        pic_path = Path(class_)
        pics = list(pic_path.rglob("*"))
        offset = int(np.ceil((len(pics)*(80/100))))
        for i in range(int(np.floor(len(pics)*(20/100)))):
            file = str(pics[i + offset].parent.name)+ "/" + str(pics[i + offset].name)
            print(output_dir + "/" + file)

            path = Path(output_dir + "/" + file)
            if not path.parent.exists():
                print("hiya")
                path.parent.mkdir()
            shutil.move(str(pics[i + offset]), str(path))
            

if __name__ == '__main__':
    # rename("data\\audioFiles", "XC*", "%s")
    training_split()
