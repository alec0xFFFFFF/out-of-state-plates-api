from api.api import create_api

if __name__ == '__main__':
    api = create_api()
    api.run(debug=True, port=os.getos.environ.get("PORT", default=5000))

