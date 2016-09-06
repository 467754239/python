# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask

app = Flask(__name__)

import login
import logout

import mail
import form
