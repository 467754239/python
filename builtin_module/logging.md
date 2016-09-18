## logging两种使用场景

> logging模块

```
import logging

logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s] - [%(threadName)5s] - [%(filename)s-line:%(lineno)d] [%(levelname)s] %(message)s',
                filename='/var/log/agent.log'),
                filemode='a'
                )
```

> flask logger

```
import logging
from logging.handlers import RotatingFileHandler
from app import app

formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s- %(levelname)s - %(message)s')
handler = RotatingFileHandler('/var/log/flask.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
```