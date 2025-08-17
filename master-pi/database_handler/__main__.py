from api_handler.api_handler import APIHandler

def main():
    db_info_file = 'database_handler/resources/database_info.json'
    api_handler = APIHandler(db_info_file)
    api_handler.app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main()