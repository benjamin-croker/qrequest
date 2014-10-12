import webserver

if __name__ == '__main__':
    webserver.app.run(host='0.0.0.0', port=webserver.settings['website_port_number'], debug=False)
