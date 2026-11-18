from pathlib import Path

folder = Path("static/materials")
folder.mkdir(parents=True, exist_ok=True)

lines = [
    "WEB TECHNOLOGY - STUDY NOTES",
    "",
    "1. INTRODUCTION TO WEB TECHNOLOGY",
    "Web technology includes tools and languages used to create websites.",
    "Examples: HTML, CSS, JavaScript and web servers.",
    "",
    "2. INTERNET AND WORLD WIDE WEB",
    "Internet is a global network of connected computers.",
    "WWW is a collection of linked web pages accessed through the Internet.",
    "",
    "3. HTML",
    "HTML stands for HyperText Markup Language.",
    "It defines the structure of a web page.",
    "Common tags: html, head, title, body, h1, p, a, img and table.",
    "",
    "4. CSS",
    "CSS stands for Cascading Style Sheets.",
    "It controls colours, fonts, spacing and webpage layouts.",
    "",
    "5. JAVASCRIPT",
    "JavaScript makes web pages interactive.",
    "It handles button clicks, form validation and dynamic content.",
    "",
    "6. CLIENT-SERVER ARCHITECTURE",
    "The browser sends a request to a server.",
    "The server processes the request and sends a response.",
    "",
    "7. HTTP AND HTTPS",
    "HTTP is used for communication between browsers and servers.",
    "HTTPS provides encrypted and secure communication.",
    "",
    "8. STATIC AND DYNAMIC WEBSITES",
    "Static websites display mostly fixed content.",
    "Dynamic websites can change content based on user input.",
    "",
    "9. WEB HOSTING AND DOMAIN",
    "Web hosting stores website files on a server.",
    "A domain name is the address used to access a website.",
    "",
    "10. RESPONSIVE WEB DESIGN",
    "Responsive design adjusts websites to different screen sizes.",
    "It supports mobile phones, tablets and desktop computers.",
    "",
    "REVISION QUESTIONS",
    "1. Define web technology.",
    "2. What is HTML?",
    "3. Explain the uses of CSS.",
    "4. What is JavaScript?",
    "5. Differentiate HTTP and HTTPS.",
    "6. Explain client-server architecture.",
]

def pdf_escape(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

commands = ["BT", "/F1 10 Tf", "50 790 Td", "15 TL"]

for index, line in enumerate(lines):
    if index:
        commands.append("T*")
    commands.append(f"({pdf_escape(line)}) Tj")

commands.append("ET")
stream = "\n".join(commands).encode("latin-1")

objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
]

pdf = bytearray(b"%PDF-1.4\n")
offsets = [0]

for number, obj in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf.extend(f"{number} 0 obj\n".encode())
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")

xref = len(pdf)
pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
pdf.extend(b"0000000000 65535 f \n")

for offset in offsets[1:]:
    pdf.extend(f"{offset:010d} 00000 n \n".encode())

pdf.extend(
    f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode()
)

output = folder / "Web_Technology_Notes.pdf"
output.write_bytes(pdf)

print("Web Technology PDF created successfully!")
print(output)