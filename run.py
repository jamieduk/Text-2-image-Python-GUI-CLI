#!/usr/bin/python3
# (c) J~Net 2026
# https://github.com/jamieduk/Text-2-image-Python-GUI-CLI
#
# python3 run.py \
#--text "Hello world" \
#--split 200 \
#--out ./output \
#--font-color "#ffffff" \
#--bg "#000000" \
#--font-size 28 \
#--padding 30
#
# Normal Open GUI Mode use 1 of the following...
#
# ./start.sh
# python run.py
#
import os
import sys
import textwrap
import argparse
import tkinter as tk
from tkinter import ttk,filedialog,colorchooser,messagebox
from PIL import Image,ImageDraw,ImageFont

MAX_TEXT_CHARS=2000

# ================= DEFAULTS =================

DEFAULTS={
    "font_size":28,
    "padding":30,
    "wrap_width":80,
    "split_limit":500,
    "border_size":5,
    "border_style":"solid",
    "font_color":"#ffffff",
    "bg_color":"#000000",
    "border_color":"#00ffff"
}

# ================= FONT SCANNER =================

def get_system_fonts():
    fonts=[]

    if sys.platform.startswith("linux"):
        search_dirs=[
            "/usr/share/fonts/truetype",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.fonts")
        ]
    elif sys.platform=="win32":
        search_dirs=[
            r"C:\Windows\Fonts"
        ]
    else:
        search_dirs=[]

    for font_dir in search_dirs:
        if not os.path.isdir(font_dir):
            continue

        for root,dirs,files in os.walk(font_dir):
            for file in files:
                if file.lower().endswith(".ttf"):
                    full=os.path.join(root,file)
                    name=os.path.splitext(file)[0]
                    fonts.append({"name":name,"path":full})

    return sorted(fonts,key=lambda x:x["name"].lower())

# ================= TEXT SPLIT =================

def split_text(text,limit):
    parts=[]
    while text:
        chunk=text[:limit]
        if len(text)>limit:
            sp=chunk.rfind(" ")
            if sp>50:
                chunk=chunk[:sp]
        parts.append(chunk.strip())
        text=text[len(chunk):].strip()
    return parts

# ================= IMAGE RENDER =================

def create_image(
    text,outfile,font_path,font_size,
    padding,wrap_width,border_size,
    border_style,border_color,
    bg,font_color,transparent,
    index,total,bg_image=None
):

    try:
        font=ImageFont.truetype(font_path,font_size) if font_path else ImageFont.load_default()
    except:
        font=ImageFont.load_default()

    lines=[]
    for l in text.splitlines():
        lines.extend(textwrap.wrap(l,width=wrap_width) or [" "])

    dummy=Image.new("RGBA",(10,10))
    d=ImageDraw.Draw(dummy)

    widths=[]
    heights=[]

    for l in lines:
        b=d.textbbox((0,0),l,font=font)
        widths.append(b[2]-b[0])
        heights.append(b[3]-b[1])

    w=max(widths) if widths else 200
    h=sum(heights)+len(heights)*6

    W=w+padding*2+border_size*2
    H=h+padding*2+border_size*2

    img=Image.new("RGBA",(W,H),(0,0,0,0) if transparent else bg)

    if bg_image:
        bgim=Image.open(bg_image).convert("RGBA").resize((W,H))
        img.paste(bgim,(0,0))

    draw=ImageDraw.Draw(img)

    if border_size>0:
        if border_style=="solid":
            for i in range(border_size):
                draw.rectangle([i,i,W-1-i,H-1-i],outline=border_color)

        elif border_style=="double":
            draw.rectangle([0,0,W-1,H-1],outline=border_color,width=max(1,border_size//2))
            o=border_size*2
            draw.rectangle([o,o,W-1-o,H-1-o],outline=border_color,width=max(1,border_size//2))

        elif border_style=="dashed":
            dash=12
            for x in range(0,W,dash*2):
                draw.line([(x,0),(x,dash)],fill=border_color,width=border_size)
                draw.line([(x,H),(x,H-dash)],fill=border_color,width=border_size)

        elif border_style=="dotted":
            step=border_size*3
            for x in range(0,W,step):
                draw.ellipse([x,0,x+border_size,border_size],fill=border_color)
                draw.ellipse([x,H-border_size,x+border_size,H],fill=border_color)

    y=padding+border_size

    for l in lines:
        draw.text((padding+border_size,y),l,fill=font_color,font=font)
        b=draw.textbbox((0,0),l,font=font)
        y+=(b[3]-b[1])+6

    draw.text((W-140,H-25),f"{index}/{total}",fill=font_color,font=font)

    img.save(outfile)

# ================= GUI =================

class GUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Text To Image Splitter v3.1")
        self.root.geometry("900x750")

        self.font_file=""
        self.bg_image_file=""

        self.system_fonts=get_system_fonts()
        self.font_map={f["name"]:f["path"] for f in self.system_fonts}
        self.selected_font=tk.StringVar()

        self.load_defaults()
        self.build_ui()

        self.root.protocol("WM_DELETE_WINDOW",self.close)

    def load_defaults(self):
        self.font_size=tk.IntVar(value=DEFAULTS["font_size"])
        self.padding=tk.IntVar(value=DEFAULTS["padding"])
        self.wrap_width=tk.IntVar(value=DEFAULTS["wrap_width"])
        self.split_limit=tk.IntVar(value=DEFAULTS["split_limit"])
        self.border_size=tk.IntVar(value=DEFAULTS["border_size"])
        self.border_style=tk.StringVar(value=DEFAULTS["border_style"])

        self.font_color=DEFAULTS["font_color"]
        self.bg_color=DEFAULTS["bg_color"]
        self.border_color=DEFAULTS["border_color"]

        self.transparent=tk.BooleanVar(value=False)

    def reset(self):
        self.load_defaults()
        self.status.set("Reset to defaults")

    def about(self):
        messagebox.showinfo(
            "About",
            "Text To Image Splitter v3.1\nMade by jnetai.com"
        )

    def close(self):
        self.root.destroy()
        sys.exit(0)

    # ================= FONT PREVIEW =================
    def update_font_preview(self):
        try:
            if not self.font_file or not os.path.isfile(self.font_file):
                return

            img=Image.new("RGB",(850,110),"#202020")
            draw=ImageDraw.Draw(img)

            font=ImageFont.truetype(self.font_file,28)

            draw.text(
                (10,30),
                "The quick brown fox jumps over the lazy dog 1234567890",
                fill="#ffffff",
                font=font
            )

            preview_path=os.path.join(os.getcwd(),"font_preview.png")
            img.save(preview_path)

            if hasattr(self,"preview_img"):
                self.preview_img.destroy()

            tk_img=tk.PhotoImage(file=preview_path)

            self.preview_img=tk.Label(self.root,image=tk_img)
            self.preview_img.image=tk_img
            self.preview_img.pack(pady=5)

        except Exception as e:
            self.status.set(f"Preview error: {e}")

    # ================= FONT SELECT =================
    def font_selected(self,event=None):
        name=self.selected_font.get()

        if name in self.font_map:
            self.font_file=self.font_map[name]
            self.status.set(f"Font: {name}")
            self.update_font_preview()

    def select_font(self):
        f=filedialog.askopenfilename(filetypes=[("Fonts","*.ttf *.otf")])
        if f:
            self.font_file=f

    def select_bg_image(self):
        f=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.webp *.bmp")])
        if f:
            self.bg_image_file=f

    # ================= COLOURS =================
    def pick_font_colour(self):
        c=colorchooser.askcolor()[1]
        if c:
            self.font_color=c

    def pick_bg_colour(self):
        c=colorchooser.askcolor()[1]
        if c:
            self.bg_color=c

    def pick_border_colour(self):
        c=colorchooser.askcolor()[1]
        if c:
            self.border_color=c

    # ================= COUNTER =================
    def update_count(self,event=None):
        count=len(self.text.get("1.0","end-1c"))
        self.char_var.set(f"{count} / {MAX_TEXT_CHARS}")
        if count>MAX_TEXT_CHARS:
            self.text.delete(f"1.0+{MAX_TEXT_CHARS}c","end")

    # ================= GENERATE =================
    def generate(self):
        text=self.text.get("1.0","end-1c").strip()

        if not text:
            messagebox.showerror("Error","No text entered")
            return

        outdir=filedialog.askdirectory()
        if not outdir:
            return

        chunks=split_text(text,max(1,self.split_limit.get()))
        total=len(chunks)

        for i,c in enumerate(chunks,1):
            create_image(
                c,
                os.path.join(outdir,f"image_{i:03d}.png"),
                self.font_file,
                self.font_size.get(),
                self.padding.get(),
                self.wrap_width.get(),
                self.border_size.get(),
                self.border_style.get(),
                self.border_color,
                self.bg_color,
                self.font_color,
                self.transparent.get(),
                i,
                total,
                self.bg_image_file
            )

        self.status.set(f"Created {total} images")

    # ================= UI =================
    def build_ui(self):
        main=ttk.Frame(self.root,padding=10)
        main.pack(fill="both",expand=True)

        ttk.Label(main,text=f"Text (Max {MAX_TEXT_CHARS} chars)").pack(anchor="w")

        self.char_var=tk.StringVar(value="0 / 2000")

        self.text=tk.Text(main,height=12)
        self.text.pack(fill="x")
        self.text.bind("<KeyRelease>",self.update_count)

        ttk.Label(main,textvariable=self.char_var).pack(anchor="e")

        opts=ttk.Frame(main)
        opts.pack(fill="x",pady=5)

        ttk.Label(opts,text="Font Size").grid(row=0,column=0)
        ttk.Entry(opts,textvariable=self.font_size,width=8).grid(row=0,column=1)

        ttk.Label(opts,text="Padding").grid(row=0,column=2)
        ttk.Entry(opts,textvariable=self.padding,width=8).grid(row=0,column=3)

        ttk.Label(opts,text="Wrap").grid(row=0,column=4)
        ttk.Entry(opts,textvariable=self.wrap_width,width=8).grid(row=0,column=5)

        ttk.Label(opts,text="Split").grid(row=1,column=0)
        ttk.Entry(opts,textvariable=self.split_limit,width=8).grid(row=1,column=1)

        ttk.Label(opts,text="Border").grid(row=1,column=2)
        ttk.Entry(opts,textvariable=self.border_size,width=8).grid(row=1,column=3)

        ttk.Label(opts,text="Style").grid(row=1,column=4)
        ttk.Combobox(opts,textvariable=self.border_style,
            values=["solid","dashed","dotted","double"],
            state="readonly",width=10).grid(row=1,column=5)

        # ================= FONT AREA =================
        fonts=ttk.LabelFrame(main,text="Fonts")
        fonts.pack(fill="x",pady=5)

        ttk.Button(fonts,text="Browse Font File",command=self.select_font).pack(side="left",padx=5)

        ttk.Label(fonts,text="System Fonts:").pack(side="left",padx=5)

        self.font_combo=ttk.Combobox(
            fonts,
            textvariable=self.selected_font,
            values=[f["name"] for f in self.system_fonts],
            state="readonly",
            width=40
        )
        self.font_combo.pack(side="left",padx=5)
        self.font_combo.bind("<<ComboboxSelected>>",self.font_selected)

        # ================= COLOURS =================
        colors=ttk.LabelFrame(main,text="Colours")
        colors.pack(fill="x",pady=5)

        ttk.Button(colors,text="Font Colour",command=self.pick_font_colour).pack(side="left",padx=5)
        ttk.Button(colors,text="Background Colour",command=self.pick_bg_colour).pack(side="left",padx=5)
        ttk.Button(colors,text="Border Colour",command=self.pick_border_colour).pack(side="left",padx=5)

        # ================= FILES =================
        files=ttk.LabelFrame(main,text="Files")
        files.pack(fill="x",pady=5)

        ttk.Button(files,text="Background Image",command=self.select_bg_image).pack(side="left",padx=5)

        ttk.Checkbutton(main,text="Transparent Background",variable=self.transparent).pack(anchor="w")

        ttk.Button(main,text="Generate Images",command=self.generate).pack(fill="x",pady=10)

        bottom=ttk.Frame(main)
        bottom.pack(fill="x",pady=10)

        ttk.Button(bottom,text="Reset",command=self.reset).pack(side="left",padx=5)
        ttk.Button(bottom,text="About",command=self.about).pack(side="left",padx=5)
        ttk.Button(bottom,text="Close",command=self.close).pack(side="right",padx=5)

        self.status=tk.StringVar(value="Ready")
        ttk.Label(main,textvariable=self.status).pack(anchor="w")

def cli(args):
    print("CLI MODE START")

    if not args.text:
        print("ERROR: --text required")
        sys.exit(1)

    text=args.text[:MAX_TEXT_CHARS]
    chunks=split_text(text,max(1,args.split))

    os.makedirs(args.out,exist_ok=True)

    print(f"Output: {args.out}")
    print(f"Chunks: {len(chunks)}")

    for i,c in enumerate(chunks,1):
        out=os.path.join(args.out,f"image_{i:03d}.png")
        print(f"Creating {out}")

        create_image(
            c,
            out,
            args.font,
            args.font_size,
            args.padding,
            args.wrap,
            args.border,
            args.border_style,
            args.border_color,
            args.bg,
            args.font_color,
            args.transparent,
            i,
            len(chunks)
        )

    print("DONE")


def main():
    p=argparse.ArgumentParser()

    p.add_argument("--text")
    p.add_argument("--split",type=int,default=500)
    p.add_argument("--out",default="./out")

    p.add_argument("--font")
    p.add_argument("--font-size",type=int,default=28)
    p.add_argument("--padding",type=int,default=30)
    p.add_argument("--wrap",type=int,default=80)
    p.add_argument("--border",type=int,default=5)

    p.add_argument("--bg",default="#000000")
    p.add_argument("--font-color",default="#ffffff")
    p.add_argument("--border-color",default="#00ffff")
    p.add_argument("--border-style",default="solid")

    p.add_argument("--transparent",action="store_true")

    args=p.parse_args()

    try:
        if args.text:
            cli(args)
        else:
            GUI().root.mainloop()

    except Exception as e:
        print("FATAL ERROR:",e)
        sys.exit(1)



if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
