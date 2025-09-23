from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Simple in-memory storage for demo purposes
# In a real application, this would be replaced with a database
patients = []
records = []

@app.route('/')
def index():
    """Home page showing recent records"""
    recent_records = records[-5:] if records else []
    return render_template('index.html', recent_records=recent_records, total_patients=len(patients))

@app.route('/patients')
def list_patients():
    """List all patients"""
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    """Add a new patient"""
    if request.method == 'POST':
        patient = {
            'id': len(patients) + 1,
            'name': request.form['name'],
            'age': request.form['age'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'medical_history': request.form['medical_history'],
            'created_at': datetime.now()
        }
        patients.append(patient)
        flash('Patient added successfully!', 'success')
        return redirect(url_for('list_patients'))
    
    return render_template('add_patient.html')

@app.route('/records')
def list_records():
    """List all medical records"""
    return render_template('records.html', records=records)

@app.route('/records/add', methods=['GET', 'POST'])
def add_record():
    """Add a new medical record"""
    if request.method == 'POST':
        record = {
            'id': len(records) + 1,
            'patient_name': request.form['patient_name'],
            'date': request.form['date'],
            'visit_type': request.form['visit_type'],
            'diagnosis': request.form['diagnosis'],
            'treatment': request.form['treatment'],
            'notes': request.form['notes'],
            'created_at': datetime.now()
        }
        records.append(record)
        flash('Medical record added successfully!', 'success')
        return redirect(url_for('list_records'))
    
    return render_template('add_record.html', patients=patients)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)