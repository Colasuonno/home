from . import app

@app.route('/alive')
def alive():
    return "Yes"
