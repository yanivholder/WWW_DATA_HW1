    import socket
import os
import hw1_utils

# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
HOME_PAGE = "http://" + SERVER_HOST + f":{SERVER_PORT}/"

web_img_addr = 'data:image/jpeg;base64,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'
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
    elif request[1] != "/" and not os.path.isfile('pdfs' + request[1]):
        conn.sendall("HTTP/1.1 404 FILE_NOT_EXISTS".encode())
        return False
    # TODO: fix to check the right thing
    elif request[1] != "/" and not request[1].endswith(".pdf"):
        conn.sendall("HTTP/1.1 404 NOT_PDF".encode())
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
    # TODO: here and everywhere else remove the .pdf from the http request
    res = "<ul>\n"
    for file in filenames:
        file = file.replace("\\", "/")
        res += f"<li> <button onclick=\"window.location.href=\'{file}\';\">{file}</button> </li>\n"
    res += "\n</ul>"
    return res


def main():
    # TODO: replace with socket per request
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
                else:
                    file_name = os.path.basename(request[1]) + ".pdf"
                    photo_name = file_name.replace('pdf', 'png')
                    photo_path = "images/" + photo_name
                    file_data = pdf_to_text('pdfs' + request[1]).lower()
                    file_data = remove_stopwords(file_data)
                    hw1_utils.generate_wordcloud_to_file(text=file_data, filename=photo_path)

                    html_page = f"<!DOCTYPE HTML>\n<html>\n<body>\n<h1>{file_name}</h1>\n"
                    # import pathlib
                    # my_path = pathlib.Path(__file__).parent.resolve()
                    # print(f"<img src=\'{my_path}\\{photo_name}\'>")
                    # html_page += f"<img src=\'{my_path}/{photo_name}\'>"
                    # TODO: replace the next line with photo name (actual word cloud)
                    html_page += f"<img src=\'{photo_name}\'>"
                    html_page += f"<button onclick=\"window.location.href=\'{HOME_PAGE}\';\">Home page</button>"
                    response = "HTTP/1.1 200 OK\n\n" + html_page
                    conn.sendall(response.encode())


if __name__ == "__main__":
    main()

