import os
import glob

# Combine all .txt files in the 'texts' directory into a single 'transcripts.txt' file
def combine_texts(input_dir: str = "texts", output_file: str = "transcripts.txt"):
    pattern = os.path.join(input_dir, "*.txt")
    txt_files = glob.glob(pattern)

    if not txt_files:
        print(f"No .txt files found in `{input_dir}`")
        return
    
    with open(output_file, "w", encoding="utf-8") as out:
        for i, fname in enumerate(txt_files, 1):
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read().strip()
                out.write(content)

    print(f"✅ Combined {len(txt_files)} files into `{output_file}`")

if __name__ == "__main__":
    combine_texts()