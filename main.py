from api import api

if __name__ == '__main__':
    api.run(debug=True, port=os.getos.environ.get("PORT", default=5000))

