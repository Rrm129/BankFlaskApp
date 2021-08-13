from website import create_app
from livereload import Server

app = create_app()

if __name__ == "__main__":
    server = Server(app.run(debug=True))
    server.serve()
