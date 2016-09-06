
from . import asset

@asset.route('/login', methods=['GET', 'POST'])
def manage_host():
    return 'manage login'
