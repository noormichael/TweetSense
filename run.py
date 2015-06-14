#!flask/bin/python
from app import app
app.run(debug=True)

import logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
