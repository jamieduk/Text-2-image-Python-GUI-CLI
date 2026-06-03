# Text 2 Image

Convert text into one or more PNG images using either a GUI or CLI.

Supports:

- GUI mode
- CLI mode
- Automatic text splitting
- Custom fonts
- Font preview
- Background images
- Transparent backgrounds
- Multiple border styles
- Linux and Windows font detection
- Image numbering (1/5, 2/5, etc.)

Project:

:contentReference[oaicite:0]{index=0}

Website:

:contentReference[oaicite:1]{index=1}

---

# Prepare Files

```bash
sudo chmod +x *.sh
```

---

# Run Setup

```bash
./setup.sh
```

---

# Start GUI

```bash
./start.sh
```

---

# GUI Version

The GUI version launches automatically using:

```bash
./start.sh
```

Features include:

- Text editor
- Character counter
- Font selector
- Font preview
- Background image support
- Colour pickers
- Border styles
- Output folder picker
- Transparent PNG option

---

# CLI Version

The same `run.py` can operate entirely from the command line.

## Example 1

```bash
python3 run.py \
--text "Hello world" \
--split 200 \
--out ./output \
--font-color "#ffffff" \
--bg "#000000" \
--font-size 28 \
--padding 30
```

## Example 2

```bash
python3 run.py \
--text "Big text block here..." \
--split 250 \
--bg "#000000" \
--font-color "#ffffff" \
--border-color "#00ffff" \
--border 6 \
--out ./output
```

## Example 3

```bash
python3 run.py \
--text "Hello world" \
--split 200 \
--out ./output \
--font /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf \
--font-color "#ffffff" \
--bg "#000000"
```

---

# CLI Options

| Option | Description |
|----------|----------|
| --text | Text to convert |
| --split | Maximum characters per image |
| --out | Output folder |
| --font | Font file |
| --font-size | Font size |
| --padding | Text padding |
| --wrap | Wrap width |
| --border | Border thickness |
| --border-style | solid, dashed, dotted, double |
| --bg | Background colour |
| --font-color | Text colour |
| --border-color | Border colour |
| --transparent | Transparent PNG output |

---

# Example Output

Input:

```text
This is a very long block of text...
```

Output:

```text
image_001.png
image_002.png
image_003.png
```

---

# Font Detection

The application automatically detects installed fonts.

## Linux

Scans:

```text
/usr/share/fonts/truetype/
/usr/local/share/fonts/
~/.fonts/
```

## Windows

Scans:

```text
C:\Windows\Fonts
```

Fonts are displayed alphabetically.

---

# Finding Fonts On Linux

```bash
ls /usr/share/fonts/truetype/
```

Example:

```text
dejavu
droid
freefont
lato
liberation
libreoffice
lyx
msttcorefonts
noto
ubuntu
wqy
```

Example font path:

```text
/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
```

---

# Useful Links

## Image To Link

:contentReference[oaicite:2]{index=2}

## Convert Text To Image Online

:contentReference[oaicite:3]{index=3}

---

# Requirements

Python 3.10+

Libraries:

```text
Pillow
tkinter
```

---

# Install Dependencies

Ubuntu/Debian:

```bash
sudo apt -y update
sudo apt -y install python3 python3-pip python3-tk
pip3 install pillow
```

---

# Licence

Copyright (c) J~Net 2026

Website:

jnetai.com
















