from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

contenido = {
    "/": open("home.html", "r", encoding="utf-8").read(),
    "/proyecto/1": open("1.html", "r", encoding="utf-8").read(),
    "/proyecto/2": "<h1>Proyecto: 2</h1>",
    "/proyecto/3": "<h1>Proyecto: 3</h1>",
}

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        path = self.url().path
        if path in contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(contenido[path].encode("utf-8"))
            # self.wfile.write(self.get_response().encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina no encontrada</h1>")

    def get_response(self):
        parsed_url = self.url()
        query = self.query_data()

        if parsed_url.path.startswith("/proyecto/"):
            proyecto = parsed_url.path.split("/")[2]
            autor = query.get("autor", "")
            return f"<h1>Proyecto: {proyecto} Autor: {autor}</h1>"
        
        return f"""
    <h1> Hola Web </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
"""


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
