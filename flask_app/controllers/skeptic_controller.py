from flask_app import app
from flask import redirect, flash, session
from flask_app.models import skeptic_model


@app.route('/skeptic/<int:sighting_id>')
def skeptic(sighting_id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')

    data = {
        'sighting_id': sighting_id,
        'sighter_id': session['uid']
    }

    skeptic_model.Skeptic.save_skeptic(data)

    return redirect(f'/show/{sighting_id}')


@app.route('/believe/<int:sighting_id>')
def believe(sighting_id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')

    data = {
        'sighting_id': sighting_id,
        'sighter_id': session['uid']
    }

    skeptic_model.Skeptic.remove_skeptic(data)

    return redirect(f'/show/{sighting_id}')