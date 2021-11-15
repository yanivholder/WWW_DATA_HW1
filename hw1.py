import socket
import os
import hw1_utils

# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
HOME_PAGE = "http://" + SERVER_HOST + f":{SERVER_PORT}/"

web_meme_addr = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7eDWXtuo6wveMnDscoh3h0Vet2q-VYV4-CQ&usqp=CAU'


def http_basic_validation(request, conn):
    """Checks if thr request type is GET, if the file pdfs exists
    and if the url is the home page or a pdf file"""

    if request[0] != "GET":
        conn.sendall("HTTP/1.1 501 NOT_GET".encode())
        return False
    elif not os.path.isdir("pdfs"):
        conn.sendall("HTTP/1.1 404 PDFS_NOT_EXISTS".encode())
        return False
    elif request[1] != "/" and not request[1].endswith(".png") and not os.path.isfile('pdfs' + request[1] + ".pdf"):
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
        filenames.append(r.replace('.//pdfs\\', ''))
    return filenames


def create_html_links(filenames):
    res = "<ul>\n"
    for file in filenames:
        file = file.replace("\\", "/")
        res += f"<li> <button onclick=\"window.location.href=\'{file[:-4]}\';\">{file}</button> </li>\n"
    res += "\n</ul>"
    return res


def main():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((SERVER_HOST, SERVER_PORT))
            s.listen(5)

            file_list_html = create_html_links(create_file_list())

            # Connecting to a new client
            conn, addr = s.accept()
            print(f"\nConnected to {addr}")

            # Getting the client request
            with conn:
                data = conn.recv(4096)
                if not data:
                    conn.sendall("HTTP/1.1 500 GENERAL_ERROR".encode())
                    continue

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
                    meme_add_on = f"<img src=\'{web_meme_addr}\'>"
                    response = "HTTP/1.1 200 OK\n\n" + root_page + file_list_html + meme_add_on + "</body>\n</html>"
                    conn.sendall(response.encode())
                elif request[1].endswith(".png"):
                    pass
                else:
                    file_name = os.path.basename(request[1]) + ".pdf"
                    photo_name = file_name.replace('pdf', 'png')
                    photo_path = "images/" + photo_name
                    file_data = pdf_to_text('pdfs' + request[1] + ".pdf").lower()
                    file_data = remove_stopwords(file_data)
                    hw1_utils.generate_wordcloud_to_file(text=file_data, filename=photo_path)

                    html_page = f"<!DOCTYPE HTML>\n<html>\n<body>\n<h1>{file_name}</h1>\n"
                    html_page += f"<img src=\'{photo_name}\'>"
                    html_page += f"<button onclick=\"window.location.href=\'{HOME_PAGE}\';\">Home page</button>"
                    response = "HTTP/1.1 200 OK\n\n" + html_page
                    conn.sendall(response.encode())


if __name__ == "__main__":
    main()

