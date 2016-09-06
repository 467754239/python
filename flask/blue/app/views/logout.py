from . import asset

@asset.route('/logout')
def manage_logout():
    return 'manage logout'
