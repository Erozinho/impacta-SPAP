from flask import render_template

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')