import apis.server as server
import config

if __name__ == "__main__":
    server.app.run(port=config.PORT, debug=config.DEBUG)