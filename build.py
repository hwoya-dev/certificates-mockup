"""Build the certificate mockup from its single source file.

    certificate-flow.src.html   the only file to edit
    assets/front.jpg, logo.png  embedded as data URIs

Outputs:
    index.html                  full standalone page, the one GitHub Pages serves
    certificate-flow.html       same content without the document wrapper (Claude artifact)

Run:  python build.py
"""
import base64
import pathlib

here = pathlib.Path(__file__).parent


def data_uri(name, mime):
    raw = (here / "assets" / name).read_bytes()
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


src = (here / "certificate-flow.src.html").read_text(encoding="utf-8")
src = src.replace("__FRONT__", data_uri("front.jpg", "image/jpeg"))
src = src.replace("__LOGO__", data_uri("logo.png", "image/png"))

(here / "certificate-flow.html").write_text(src, encoding="utf-8", newline="\n")

head, body = src.split("<!--BODY-->", 1)
page = (
    "<!DOCTYPE html>\n"
    '<html lang="ru">\n'
    "<head>\n"
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<meta name="theme-color" content="#171a21">\n'
    "<style>html{color-scheme:dark}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
    + head
    + "</head>\n<body>\n"
    + body
    + "\n</body>\n</html>\n"
)
(here / "index.html").write_text(page, encoding="utf-8", newline="\n")

print("built index.html (%d KB) and certificate-flow.html" % (len(page.encode("utf-8")) // 1024))
