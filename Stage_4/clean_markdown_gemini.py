import os
import time
import argparse
from google import genai
from google.genai import errors

# ---------------- Configuration ----------------
INPUT_MD = "book.md"
OUTPUT_MD = "book_cleaned.md"
CHUNK_SIZE = 50  # lines per chunk
MODEL_NAME = "gemini-3-flash-preview"
client = genai.Client()
MAX_RETRIES = 5  # max retry attempts per chunk

# ---------------- Helper functions ----------------
def chunks(lst, n):
    """Yield successive n-sized chunks from list"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def create_prompt(chunk_lines):
    """Create a cleaning prompt for the LLM"""
    text_block = "\n".join(chunk_lines)
    prompt = (
        "The following Markdown file was created automatically by scanning a book and "
        "processing the PDF using OCR. As a result, it may contain artifacts, formatting "
        "issues, or extra line breaks. Clean up the Markdown while preserving headings, "
        "lists, and paragraph structure. Keep the text content intact and readable.\n\n"
        f"Markdown chunk:\n{text_block}\n\nCleaned Markdown:"
    )
    return prompt

# ---------------- Main script ----------------
def main(resume_chunk=1):
    print("Loading Markdown file...")
    with open(INPUT_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"Loaded {len(lines)} lines from {INPUT_MD}")

    total_chunks = (len(lines) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(f"Total chunks to process: {total_chunks}")

    # Open output file in append mode
    with open(OUTPUT_MD, "a", encoding="utf-8") as out_file:
        for idx, chunk in enumerate(chunks(lines, CHUNK_SIZE), start=1):
            if idx < resume_chunk:
                continue  # skip already processed chunks

            print(f"\nProcessing chunk {idx}/{total_chunks} ({len(chunk)} lines)...")
            prompt = create_prompt(chunk)
            retries = 0

            while retries < MAX_RETRIES:
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt
                    )
                    cleaned_text = response.text
                    cleaned_lines = cleaned_text.split("\n")

                    # Append cleaned chunk immediately
                    for line in cleaned_lines:
                        out_file.write(line + "\n")
                    out_file.write("\n")

                    print(f"Chunk {idx} processed and written to {OUTPUT_MD} (lines after: {len(cleaned_lines)})")
                    time.sleep(0.5)  # optional: avoid rate limits
                    break  # exit retry loop on success

                except errors.ClientError as e:
                    if e.status == "RESOURCE_EXHAUSTED":
                        retry_delay = getattr(e, "retryDelay", 60)
                        print(f"Quota exceeded. Waiting {retry_delay} seconds before retrying...")
                        time.sleep(retry_delay)
                        continue  # retry the same chunk
                    else:
                        print(f"Error processing chunk {idx}: {e}")
                        break
            else:
                print(f"Chunk {idx} failed after {MAX_RETRIES} retries. Skipping.")

    print(f"\nAll chunks processed (or attempted). Final cleaned Markdown saved to {OUTPUT_MD}")

# ---------------- Argument parser ----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Markdown using Gemini with retry and resume support")
    parser.add_argument("--resume", type=int, default=1, help="Chunk number to resume from (1-based)")
    args = parser.parse_args()

    main(resume_chunk=args.resume)

