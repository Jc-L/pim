
Personal project to play with python.

# Initial setup

Development rely on a python virtual env, to create in the development directory with:

```bash
py -3 -m venv venv
```

Afterwards, using the environement (on Windows) can be done with:

```bash
source venv/Scripts/activate
```

Application can be launched with

```bash
winpty python pim-web.py
```

It should then be reachable on <http://127.0.0.1:5000/>


```bash
winpty python

import logging
from pimconfig import ProductionConfig, DevelopmentConfig, TestingConfig
from pimcore import PimApp
from pimdata import *
pim_app = PimApp(DevelopmentConfig)
pimdata.pimdata_init(pim_app.config )


```
