import webserver
import database as db

if __name__ == '__main__':

    webserver.app.run(port=db.SETTINGS['website_port_number'], debug=False)