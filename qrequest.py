import webserver
import database as db

if __name__ == '__main__':

    webserver.app.run(host='0.0.0.0', port=db.SETTINGS['website_port_number'], debug=False)
