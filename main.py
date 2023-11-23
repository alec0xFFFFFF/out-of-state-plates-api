from api.api import create_api

api = create_api()
routes.init_app(api)

if __name__ == '__main__':\
    api.run(debug=True, port=os.getos.environ.get("PORT", default=5000))

