from Signal import Signal
from pathlib import Path
from tqdm import tqdm
from Chunk import Chunk
import random

def batch_load(input_dir="data/spec_chunks", n_load=100):
    input_path = Path(input_dir) 
    files = list(input_path.rglob("*.png"))
    chunks = []

    for file in random.sample(files, n_load):
        chunk = Chunk()
        chunk.load_chunk_from_path(str(file))
        chunks.append(chunk)

    return chunks



def batch_convert_signal(input_dir="data/audioFiles", output_dir="data/spec_chunks2"):
    input_path = Path(input_dir) 
    files = list(input_path.rglob('*'))


    signals = []

    processed = 0
    failed = 0
    for path in tqdm(files, desc="Processing Signals"):
        rel_path = path.relative_to(input_dir)
        out_path = output_dir / rel_path.parent

        if process_signal(path, out_path):
            processed += 1
        else:
            failed += 1
    
    print(f"\nProcessing complete!")
    print(f"Successfully processed: {processed}")
    print(f"Failed: {failed}")
    if processed > 0:
        print(f"Spectrograms saved to {output_dir}")

    return signals

def process_signal(input_path, output_path):
    sig = Signal(str(input_path))
    sig.chunk_up_the_wav(1)
    sig.chunks_to_specs()
    sig.save_chunks(str(output_path))
    
    return sig
    


if __name__ == "__main__":
    # batch_load()
    batch_convert_signal()