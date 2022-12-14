from flask_app import app
from flask import request, render_template, redirect, flash, session
from flask_app.models import sighting_model, skeptic_model


@app.route('/dashboard')
def dashboard():
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')

    return render_template('dashboard.html',sightings=sighting_model.Sighting.get_all_sightings_with_users())

@app.route('/new/sighting')
def new_sighting():
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    return render_template('add.html')

@app.route('/add', methods=["POST"])
def add_sighting():
    if not sighting_model.Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    
    data = {
        **request.form,
        'sighter_id': session['uid']
    }

    sighting =  sighting_model.Sighting.save_sighting(data)

    if not sighting:
        flash('Error in adding sighting.','sighting')
        return redirect('/new/sighting') 
    
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def view_sighting(id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    
    sighting = sighting_model.Sighting.get_one_sighting_with_user(id)
    if sighting.sighter_id == session['uid']:
        return redirect(f'/edit/{id}')

    return render_template('view.html',sighting=sighting)

@app.route('/edit/<int:id>')
def edit_sighting(id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    
    sighting = sighting_model.Sighting.get_one_sighting_with_user(id)
    
    if session['uid'] != sighting.sighter_id:
        return redirect('/dashboard')
    
    return render_template('modify.html',sighting=sighting)

@app.route('/update/<int:id>', methods=["POST"])
def update_sighting(id):
    if not sighting_model.Sighting.validate_sighting(request.form):
        return redirect(f'/edit/{id}')
    data = {
        **request.form,
        'id': id
    }

    sighting_model.Sighting.update_sighting(data)
    
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_sighting(id):
    if 'uid' not in session:
        flash('Please login first.','login')
        return redirect('/')
    
    if session['uid'] != sighting_model.Sighting.get_one_sighting_with_user(id).sighter_id:
        return redirect('/dashboard')
    
    sighting_model.Sighting.remove_sighting(id)
    return redirect('/dashboard')