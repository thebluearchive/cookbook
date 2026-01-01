import difflib

# ---------- Config ----------
original_file = "book.md"      # Original file
modified_file = "patch.md"     # File to compare
start_line = 100               # Start of range (1-based)
end_line = 150                 # End of range (inclusive)

# ---------- Load files ----------
with open(original_file, "r", encoding="utf-8") as f:
    orig_lines = f.readlines()

with open(modified_file, "r", encoding="utf-8") as f:
    mod_lines = f.readlines()

# ---------- Select line ranges ----------
# Convert 1-based to 0-based indexing
orig_range = orig_lines[start_line-1:end_line]
mod_range = mod_lines[start_line-1:end_line]

# ---------- Compute unified diff ----------
diff = difflib.unified_diff(
    orig_range,
    mod_range,
    fromfile=original_file,
    tofile=modified_file,
    lineterm=""
)

# ---------- Print diff ----------
print("\n".join(diff))

