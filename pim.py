
import argparse
import os
from asyncio.windows_events import NULL
from curses import meta
import logging
import threading
import time

from pimconfig import ProductionConfig, DevelopmentConfig, TestingConfig
from pimcore import PimApp

pim_app = PimApp(ProductionConfig)

# commandline management
cmdlineparser = argparse.ArgumentParser(description='Start PIM, the Personal Information Manager')
# commandline options for loglevel
group_loglevel = cmdlineparser.add_mutually_exclusive_group()
group_loglevel.add_argument('-d', '--debug', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.WARNING, help="activate debug loglevel" )
group_loglevel.add_argument('-v', '--verbose', action='store_const', dest='loglevel', const=logging.INFO, default=logging.WARNING, help="activate verbose (info) loglevel" )
group_env = cmdlineparser.add_mutually_exclusive_group(required=True)
group_env.add_argument('--prod', action='store_const', dest='config', const=ProductionConfig, help='use "production" environment' )
group_env.add_argument('--dev',  action='store_const', dest='config', const=DevelopmentConfig, help='use "development"" environment' )
group_env.add_argument('--test', action='store_const', dest='config', const=TestingConfig, help='use "testing" environment' )
group_disable_modules = cmdlineparser.add_argument_group(title='options for modules', description=None)
group_disable_modules.add_argument('--disable-web', action='append_const', dest='disable', const='web', help='disable web server' )
group_disable_modules.add_argument('--disable-cli', action='append_const', dest='disable', const='cli', help='disable command-line interface' )
group_disable_modules.add_argument('--disable-mnt', action='append_const', dest='disable', const='maintenance', help='disable maintenance module' )
cmdlineargs = cmdlineparser.parse_args()
# commandline content used to update global pim_app object
pim_app.loglevel = cmdlineargs.loglevel
pim_app.config = cmdlineargs.config
if cmdlineargs.disable != None:
    pim_app.modules = pim_app.modules - set(cmdlineargs.disable)

# load/configure logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s', level=pim_app.loglevel, datefmt='%Y-%d-%m %H:%M:%S')
logging.debug('debug mode is active')

# load/configure local modules
try:
    import pimdata
    import pimweb
except ModuleNotFoundError as err:
    logging.critical(f"early initialization error. {type(err).__name__}: {err}")
    # print(f"Unexpected {err=}, {type(err)=}")
    exit(1)
except BaseException as err:
    logging.critical(f"Unexpected {err=}, {type(err)=}")
    exit(1)

##################################
# 'Maintenance' module
##################################
def maintenance_start():
    logging.debug('creating maintenance thread')
    thread_maintenance = threading.Thread(target=maintenance_thread, name='maintenance', daemon=True)
    thread_maintenance.start()

def maintenance_thread():
    cur_thr = threading.current_thread()
    logging.info("[%s %s] starting", cur_thr.name, cur_thr.native_id)
    while True:
        time.sleep(5)
        logging.info("[%s %s] executing", cur_thr.name, cur_thr.native_id)
    logging.info("[%s] finishing", cur_thr.name)
    return 0


##################################
# 'Web' module
##################################

def web_start():
    logging.debug('creating \'web\' module')
    web_app = pimweb.create_module(pim_app.config)
    logging.debug('\'web\' module starting in main thread')
    web_app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False, threaded=True)

# see https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread
def web_thread():
    return 0
    

##################################
# 'CLI' module
##################################

def cli_start():
    import pimcli
    logging.debug('creating \'cli\' module')
    cli = pimcli.PimCli()


##################################
# Main part
##################################
logging.debug(f'using environment "{pim_app.config.ENV}"')

if __name__ == "__main__":
    pimdata.pimdata_init(pim_app.config )
    logging.debug(f'starting {len(pim_app.modules)} module(s)')
    if 'maintenance' in pim_app.modules:
        maintenance_start()
    else:
        logging.info('skipping disabled \'maintenance\' module')
    if 'web' in pim_app.modules:
        web_start()
    else:
        logging.info('skipping disabled \'web\' module')
    if 'cli' in pim_app.modules:
        cli_start()
    else:
        logging.info('skipping disabled \'cli\' module')

