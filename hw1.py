import socket
import os
import string
import hw1_utils
import pdfminer


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888


def http_basic_validation(request, conn):
    """Checks if thr request type is GET, if the file pdfs exists
    and if the url is the home page or a pdf file"""

    if request[0] != "GET":
        conn.sendall("HTTP/1.1 501 NOT_GET".encode())
        return False
    elif request[1] != "/" and not request[1].endswith(".pdf"):
        conn.sendall("HTTP/1.1 404 NOT_PDF".encode())
        return False
    elif not os.path.isdir("pdfs"):
        conn.sendall("HTTP/1.1 404 PDFS_NOT_EXISTS".encode())
        return False
    elif request[1] != "/" and not os.path.isfile('pdfs' + request[1]):
        conn.sendall("HTTP/1.1 404 FILE_NOT_EXISTS".encode())
        return False
    return True


def pdf_to_text(path):
    from io import StringIO
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfparser import PDFParser

    output_string = StringIO()
    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()


def remove_stopwords(file_data):
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read()
    wordlist = file_data.split()
    wordlist = [word for word in wordlist if word not in stopwords]
    return ' '.join(wordlist)


def create_file_list():
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk('.//pdfs') for f in filenames if
              os.path.splitext(f)[1] == '.pdf']
    filenames = []
    for r in result:
        filenames.append(r.removeprefix('.//pdfs\\'))
    return filenames


def create_html_links(filenames):
    res = "<ul>\n"
    for file in filenames:
        file = file.replace("\\", "/")
        res += f"<li> <button onclick=\"window.location.href=\'{file}\';\">{file}</button> </li>\n"
    res += "\n</ul>"
    return res


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)

        file_list_html = create_html_links(create_file_list())

        while True:
            # Connecting to a new client
            conn, addr = s.accept()
            print(f"\nConnected to {addr}")

            # Getting the client request
            with conn:
                data = conn.recv(4096)
                if not data:
                    # TODO: add error message
                    continue
                # conn.sendall(data)

                # Parsing the HTTP request
                http_dict = hw1_utils.decode_http(data)
                request = http_dict['Request'].split()
                print(request)

                # Checking if the request is legal
                if not http_basic_validation(request, conn):
                    continue

                if request[1] == "/":
                    # If the url is the home page:
                    with open('index.html') as f:
                        root_page = f.read()
                    response = "HTTP/1.1 200 OK\n\n" + root_page + file_list_html + "</body>\n</html>"
                    conn.sendall(response.encode())
                else:
                    file_data = pdf_to_text('pdfs' + request[1]).lower()
                    file_data = remove_stopwords(file_data)
                    html_page = f"<!DOCTYPE HTML>\n<html>\n<body>\n<h1>{os.path.basename(request[1])}</h1>\n"
                    # TODO: replace the next line with cloud word
                    html_page += f"<p>{file_data}</p>\n"
                    html_page += "<button onclick=\"window.location.href=\'http://127.0.0.1:8888/\';\">Home page</button>"
                    response = "HTTP/1.1 200 OK\n\n" + html_page
                    conn.sendall(response.encode())


if __name__ == "__main__":
    main()

