from api.api import create_api
from api.routes import init_api
api = create_api()
init_api(api)

if __name__ == '__main__':\
    api.run(debug=True, port=os.getos.environ.get("PORT", default=5000))

