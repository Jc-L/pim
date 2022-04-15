
import threading
import time

# load/configure logging
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG, datefmt='%Y-%d-%m %H:%M:%S')
logging.debug('starting')

# load/configure flask
try:
    import flaskr
    # from flask import Flask, escape, request
except ModuleNotFoundError as err:
    logging.critical(f"early initialization error. {type(err).__name__}: {err}")
    # print(f"Unexpected {err=}, {type(err)=}")
    exit(1)
except BaseException as err:
    logging.critical(f"Unexpected {err=}, {type(err)=}")
    exit(1)

##################################
# 
##################################

def maintenance_thread(dumbval):
    cur_thr = threading.current_thread()
    logging.info("[%s %s] starting", cur_thr.name, cur_thr.native_id)
    while True:
        time.sleep(10)
        logging.info("[%s %s] executing", cur_thr.name, cur_thr.native_id)
    logging.info("[%s] finishing", cur_thr.name)
    return 0

# see https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread
def web_thread():
    return 0
    

##################################
# Flask routes
##################################

app = flaskr.create_app()

##################################
# Main part
##################################

if __name__ == "__main__":
    logging.debug('creating maintenance thread ')
    maintenance_thread = threading.Thread(target=maintenance_thread, name='maintenance_thread', daemon=True, args=("dumb value",))
    maintenance_thread.start()
    logging.debug('flask app starting in main thread')
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False, threaded=True)