import web

url = (
    '/', 'controllers.index.Index'
)

app = web.application(url, globals())

if __name__ == "__main__":
    app.run()
