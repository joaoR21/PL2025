import re
import sys


def to_HTML(text):
    # cabeçalhos
    text = re.sub(r'### (.+)', r'<h3>\1</h3>', text)
    text = re.sub(r'## (.+)', r'<h2>\1</h2>', text)
    text = re.sub(r'# (.+)', r'<h1>\1</h1>', text)

    # negrito
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # itálico
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)

    # lista numerada
    linhas = text.split("\n")
    dentro_lista = False
    html = []

    for linha in linhas:
        match = re.match(r'(\d+)\. (.+)', linha)
        if match:
            if not dentro_lista:
                html.append("<ol>")
                dentro_lista = True
            html.append(f"<li>{match.group(2)}</li>")
        else:
            if dentro_lista:
                html.append("</ol>")
                dentro_lista = False
            html.append(linha)

    if dentro_lista:
        html.append("</ol>")

    text = "\n".join(html)

    # links
    text = re.sub(r'(?<!!)\[(.+?)]\((.+?)\)', r'<a href="\2">\1</a>', text)

    # imagens
    text = re.sub(r'!\[(.+?)]\((.+?)\)', r'<img src="\2" alt="\1"/>', text)

    return text


def main():
    filename = sys.argv[1]

    with open(filename,"r",encoding="utf-8") as f:
        data = f.read()

    text_HTML = to_HTML(data)

    filename_HTML = filename.replace(".md", ".html")

    with open(filename_HTML,"w",encoding="utf-8") as f:
        f.write(text_HTML)

    print(f"O ficheiro foi convertido e guardado como '{filename_HTML}'.")


if __name__ == "__main__":
    main()
