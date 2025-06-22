#!/usr/bin/env python3
"""
clipcat.py: Merge multiple text files and copy the combined content to the macOS clipboard.

Usage:
    python3 clipcat.py file1.txt file2.txt [file3.txt ...]
"""
import argparse
import subprocess
import sys
import os
import platform
import shutil

DEFAULT_PROMPT_FILE = "/tmp/prompt.txt"

def merge_files(file_paths):
    """
    Read and concatenate the contents of the given files.
    If a file has a .py, .js, .rs, .html, .htm, .ts, or .tsx extension, wrap its content in triple backticks.

    :param file_paths: List of file paths to merge
    :return: Merged string of all file contents
    """
    merged_content = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading {path}: {e}", file=sys.stderr)
            sys.exit(1)

        ext = os.path.splitext(path)[1].lower().lstrip('.')
        if ext in ('py', 'js', 'rs', 'html', 'htm', 'ts', 'tsx'):
            file_name = os.path.basename(path)
            # use '//' for JS/TS/Rust, '#' otherwise
            comment_str = '//' if ext in ('js','rs','ts','tsx') else "#"
            content = (
                f"```\n"
                f"{comment_str} file name: {file_name} {comment_str}\n"
                f"{content}\n"
                f"```"
            )
        merged_content.append(content)

    return "\n".join(merged_content)

def copy_to_clipboard(text):
    """
    Copy the given text to the macOS/Linux clipboard using pbcopy/xclip.

    :param text: String to copy
    """
    system = platform.system()
    if system == 'Darwin':
        cmd = ['pbcopy']
    elif system == 'Linux':
        if shutil.which('xclip'):
            cmd = ['xclip', '-selection', 'clipboard']
        else:
            print("Error: xclip was not found.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Unsupported OS: {system}", file=sys.stderr)
        sys.exit(1)

    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        proc.communicate(text.encode('utf-8'))
    except FileNotFoundError:
        # This shouldn't happen if we checked with shutil.which, but just in case:
        print(f"Error: '{cmd[0]}' not found. Clipboard copy failed.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error copying to clipboard: {e}", file=sys.stderr)
        sys.exit(1)
def main():
    parser = argparse.ArgumentParser(
        description="Merge one or more text files and copy the result to the macOS clipboard."
    )
    parser.add_argument(
        'files', nargs='+', metavar='FILE',
        help='Paths to files to merge'
    )
    args = parser.parse_args()

    if os.path.isfile(DEFAULT_PROMPT_FILE):
        input_files = [DEFAULT_PROMPT_FILE, *args.files]
    else:
        input_files = args.files

    merged = merge_files(input_files)
    copy_to_clipboard(merged)
    print(f"Merged content of {input_files} copied to clipboard.")

if __name__ == '__main__':
    main()
