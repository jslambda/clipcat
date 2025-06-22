# 📋 clipcat.py

**clipcat** is a lightweight Python script that merges the content of one or more text/code files and copies the result to your system clipboard. It's especially handy for preparing prompts for AI models like ChatGPT or sharing snippets with context.

Works on **macOS** and **Linux** (with `xclip`).

---

## 🚀 Features

* ✅ Concatenates multiple text or code files
* ✅ Wraps source code in language-appropriate code blocks
* ✅ Adds filename headers as comments inside code blocks
* ✅ Copies the final result directly to your clipboard
* ✅ Optionally prepends content from `/tmp/prompt.txt` if it exists

---

## 🛠 Usage

```bash
python3 clipcat.py file1.txt file2.py file3.rs
```

This will:

* Read all specified files
* Format code files (e.g. `.py`, `.js`, `.rs`, `.html`, `.ts`, `.tsx`) into Markdown-style code blocks with filename headers
* Copy the final result to your system clipboard

If a file `/tmp/prompt.txt` exists, it will automatically be prepended.

