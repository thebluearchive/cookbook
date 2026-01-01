import tiktoken

# ---------- Config ----------
input_md = "book.md"
chunk_size = 50  # lines per LLM call
model = "gpt-4"  # GPT-4 pricing
price_per_1k_prompt = 0.03    # USD per 1000 prompt tokens
price_per_1k_completion = 0.06  # USD per 1000 completion tokens

# ---------- Load Markdown ----------
with open(input_md, "r", encoding="utf-8") as f:
    text = f.read()

# ---------- Token counting ----------
encoding = tiktoken.encoding_for_model(model)
tokens = len(encoding.encode(text))
print(f"Estimated total tokens in Markdown: {tokens}")

# ---------- Total cost estimate ----------
# Assuming roughly equal prompt + completion tokens
total_cost = (tokens / 1000) * (price_per_1k_prompt + price_per_1k_completion)
print(f"Estimated total cost for GPT-4: ${total_cost:.2f}")

# ---------- Chunk-based estimate ----------
lines = text.split("\n")
num_chunks = (len(lines) + chunk_size - 1) // chunk_size
tokens_per_line = tokens / len(lines)
tokens_per_chunk = tokens_per_line * chunk_size
cost_per_chunk = (tokens_per_chunk / 1000) * (price_per_1k_prompt + price_per_1k_completion)

print(f"\nNumber of {chunk_size}-line chunks: {num_chunks}")
print(f"Estimated tokens per chunk: {tokens_per_chunk:.0f}")
print(f"Estimated cost per chunk: ${cost_per_chunk:.2f}")

