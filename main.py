from api.api import create_api

app = create_api()

if __name__ == '__main__':\
    app.run(debug=True, port=os.getos.environ.get("PORT", default=5000))

