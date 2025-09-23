# Index
- [YOUR PROJECT TITLE](#your-project-title)
- [Video Demo](#https://youtu.be/XZxGqB2oSII)
- [Description](#description)
- [Approach](#approach)
- [Role-based Functionality](#for-now-the-role-based-functionality-of-this-app-is-as-follows)
  - [Patient role](#patient-role)
  - [Nursing role](#nursing-role)
  - [Supervisor role](#supervisor-role)
- [PROJECT FILES](#project-files)
  - [TEMPLATES](#templates)
  - [PYTHON](#python)
  - [DATABASE](#database)
  - [REQUIREMENTS](#requirements)
  - [README](#readme)
- [Routes and roles](#routes-and-roles)

# YOUR PROJECT TITLE
#### Video Demo: <[Project](https://youtu.be/XZxGqB2oSII)>
#### Description:
Home Care in Mexico
This is a web base application to communicate between a patient, the nurse and the nurse's supervisor in home care. It is designed to work in Mexico, because of the gap between homecare workers and the need of them.

## Use of AI
I used copilot from VSCode and CHTA-GTP to help me understand my mistakes and write me some specific functions. Took me a while to understand I had to check with more acuracy what copilot and chat-gpt proposed. I made the terrible mistake of accepting a reorganization proposal from one of this tools. It deleted and rename functionality. Took me some extra hours to get the app up and ruunning again.
With the infrastructure  I used, to work with sqlite3, I had to import "pyodbc", but I can not use it inside CS50, so it will not run from inside CS50. Instead, it can be run ..........


## Approach

The focus of this system is communication. It's important to share data and information about situations that may affect a patient's health.
It is desirable that the patient share data relating to symptoms, events, study results and somatometry measurements.
For their part, the nurse must record the care plan, including medical indications, and may also record prescriptions and somatometry. They must also include nursing actions (treatments, screenings, catheter placement, vital sign readings, administration of prescribed medications, etc.) in the plan.
For their part, the supervisor will review and approve the care plans, having access to the entire file and direct communication with the nurse.
The scope and possibilities for development based on this scheme are many and are considered outside the scope of this project.
Just to name a few:
•	On the patient side, communication with health gadgets can feed the care record, which can be consulted by the doctor(s) and trusted staff that each patient decides.
•	Artificial intelligence could also be used to identify symptoms and events, and in case of any risk, alert the nurse and supervisor.
•	On the nursing side, the Care Plan can be integrated into daily task sheets, a log of completed activities can be kept, and outstanding tasks can be notified to both nursing and supervisors. Nurses can also be supported by accessing the applicable legal framework and specific procedures.
•	Prescriptions can be scheduled on the calendar and confirmation requested. For medications related to chronic diagnoses, stock and usage can be recorded to provide advance warning of the need for refills.
•	For the supervisory role, analyses can be performed on both the patient's health status and the efficiency and effectiveness of each nurse.


For now, the role-based functionality of this app is as follows:
# Patient role.
The patient can record events that may impact their health (observable events or occurrences, such as fever, bleeding, or falls) and symptoms (non-quantifiable subjective manifestations such as pain, anxiety, or dizziness). They can also authorize other users to view their records (and revoke this authorization).
The Care Plan and prescriptions will also be visible to you.

# Nursing role
The nurse will be able to record a new Care Plan when required. She will be able to view all patient records. She will also be able to record the patient's somatometry.
You will be able to consult the events and symptoms recorded by the patient.
You'll be able to see the supervisor's comments in the Care Plan if you reject it. You'll be able to make adjustments and send comments to the supervisor until it's accepted.

# Supervisor role
The supervisor will have access to the Care Plans pending approval. They will be able to view and review the remaining information. They can accept or reject the plans. In this case, a field will open to present it to the nursing staff and explain the reason for the rejection.
 







# PROJECT FILES
## TEMPLATES
### apology.html
Error messages
### autoaccess.html
Authorization, by the patient, for another person to access the care record.
### personaldata.html
	Allows the patient to record their personal data.
### documents.html
	Allows patients to upload relevant PDF documents to their medical record, such as the results of ancillary studies.
### event.html
	Allows patients to record important events such as illnesses, traumatic events, medical treatments, environmental and social events, etc.
### index.html
### layout.html
Base template that adapts the interface according to the logged-in user, displaying a different menu for nurses, patients, and supervisors.
### login.html
	Routine to verify password and search for user role
### macros.html
	Macros to highlight a patient's risks (joys, ulcers, etc.)
### password.html
	Routine for the user to change their password
### prescriptions.html
Allows nurses to record medical prescription(s) for follow-up.
### register.html
	Login screen, asking for username and password
### nursing_registry.html
This is the nurse's work screen. It allows you to view the Care Plan, as well as record prescriptions, somatometry, and suggested adjustments to the Care Plan.
### select_patient.html
	Allows the nurse to select which patient she will work with
### symptoms.html
	Allows the patient to record symptoms .
### somatometry.html
	Allows nurse and patient to record symptoms.


## PYTHON
### App.py

1.	Flask Application Configuration
	Initialize Flask and configure the session.
	Configure upload folders and custom filters for Jinja.
2.	Connecting to the database
	get_db_connection() function to connect to SQLite and create tables if they do not exist.
3.	Main routes (endpoints)
o	/
	Methods: GET, POST
	Function: index
	Displays the main dashboard with user and patient data, care plans, somatometry, symptoms, events, documents, authorizations, and prescriptions.
o	/personaldata
	Methods: GET, POST
	Function: personal data
	Allows the patient to register or update their personal data.
o	/autoaccess
	Methods: GET, POST
	Function: self-access
	Allows you to record and display access authorizations.
o	/edit_last_nursing
	Method: POST
	Allows nursing to edit the last rejected care plan.
o	/login
	Methods: GET, POST
	Function: login
	Allows you to log in.
o	/password
	Methods: GET, POST
	Function: password
	Allows you to change the user's password.
o	/register
	Methods: GET, POST
	Function: register
	It allows you to register a new user and, if you are a patient, it redirects you to complete your personal information.
o	/nursing_registry
	Methods: GET, POST
	Function: nursing_registration
	Allows nursing to record a new care plan for a selected patient.
o	/select_patient
	Methods: GET, POST
	Function: select_patient
	It allows nursing to select the patient they will work on.
o	/symptoms
	Methods: GET, POST
	Function: symptoms
	Allows the patient to record and view their symptoms.
o	/event
	Methods: GET, POST
	Function: event
	Allows the patient to record events and authorizations.
o	/somatometry
	Methods: GET, POST
	Function: somatometry
	It allows recording and displaying somatometry data (weight, height, blood pressure, etc.) for both the patient and the nurse.
o	/documents
	Methods: GET, POST
	Function: documents
	Allows the patient to upload and view documents.
o	/prescriptions
	Methods: GET, POST
	Function: prescriptions
	Allows you to record and display medical prescriptions.
o	/logout
	Method: GET
	Function: logout
	Logs out the user.
o	/validate_last
	Method: POST
	Allows you to validate, comment on, or cancel the latest care plan.
4.	Auxiliary functions
o	get_care_plans(patient_id)
	Obtains a patient's care plans.
o	register_user(username, password, role, full_name)
	Register a user and, if they are a patient, add them to the patient table.
5.	Session and context management
o	Injects the username into the templates.
o	Configure headers to avoid caching.


### Helpers.py
1.	validate(user, db)
o	Checks if the user exists in the database.
2.	apology(message, code=400)
o	Displays a custom error page ( apology.html ) with the error message and code.
3.	login_required(f)
o	Decorator to protect routes; requires the user to be logged in for access.
4.	mxn(value)
o	Formats a numeric value as currency in Mexican pesos (MXN).
5.	rows_to_dict(rows)
o	Converts a list of SQLite rows (sqlite3.Row) to a list

## DATABASE
patients.db has the next .SCHEMA
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE summary (id INTEGER PRIMARY KEY AUTOINCREMENT, users_id INTEGER NOT NULL, symbol TEXT NOT NULL, qty INTEGER NOT NULL);
CREATE TABLE Patients ( usersId INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT, Password TEXT, FullName TEXT, File TEXT, Name TEXT, FirstLastName TEXT, SecondLastName TEXT, DateOfBirth TEXT, -- YYYY-MM-DD EntityOfBirth INTEGER, SexCURP INTEGER, BiologicalSex INTEGER, Gender REAL, CURP TEXT, MentalState TEXT, GroupRH TEXT, -- I changed "Group and RH" (spaces are not allowed in the name) PrimaryDiagnosis TEXT, -- without spaces PrimaryICD TEXT, -- char(4) → TEXT SecondDiagnosis TEXT, SecondCIE TEXT, ThirdDiagnosis TEXT, ThirdCIE TEXT, Address INTEGER, PatientEmail TEXT, PatientPhone TEXT, PatientWhatsApp TEXT, TutorContactName TEXT, RelationshipContactTutor TEXT, TelephoneContactTutor TEXT, WhatsAppContactTutor TEXT, FirstContact INTEGER DEFAULT 1, ActivePatient INTEGER NOT NULL, DateLastMovement TEXT -- YYYY-MM-DD
, Allergic INTEGER DEFAULT 0, Risk of Falls INTEGER DEFAULT 0, Risk of Ulcers INTEGER DEFAULT 0);
CREATE TABLE move ( id INTEGER PRIMARY KEY AUTOINCREMENT, date NOT NULL, users_id INTEGER NOT NULL, event TEXT NOT NULL, type INTEGER NOT NULL );
CREATE TABLE symptoms ( id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, users_id INTEGER NOT NULL, type TEXT NOT NULL, duration TEXT, intensity TEXT, description TEXT );
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'patient');
CREATE TABLE events ( id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, users_id INTEGER NOT NULL, type INTEGER NOT NULL, event TEXT NOT NULL, type INTEGER NOT NULL );
CREATE TABLE documents ( id INTEGER PRIMARY KEY AUTOINCREMENT, users_id INTEGER NOT NULL, date TEXT NOT NULL, topic TEXT NOT NULL, comments TEXT, filename TEXT NOT NULL );
CREATE TABLE IF NOT EXISTS "care_plans" ( id INTEGER PRIMARY KEY AUTOINCREMENT, users_id INTEGER NOT NULL, date TEXT NOT NULL, fall_risk TEXT, mental_state TEXT, ulcer_risk TEXT, diabetic_foot_risk TEXT, wounds TEXT, stomas TEXT, hygiene TEXT, postural_measures TEXT, fluid_balance TEXT, devices TEXT, airway_care TEXT , status TEXT NOT NULL DEFAULT 'Pending review', comments TEXT, diet TEXT, rehabilitation TEXT, allergy TEXT, detections TEXT, actions TEXT);
CREATE TABLE prescriptions ( id INTEGER PRIMARY KEY AUTOINCREMENT, users_id INTEGER NOT NULL, medication TEXT NOT NULL, dose TEXT NOT NULL, quantity TEXT NOT NULL, via TEXT NOT NULL, each_quantity TEXT NOT NULL, each_unit TEXT NOT NULL, unit_measure TEXT NOT NULL, since TEXT NOT NULL, during_quantity TEXT NOT NULL, during_unit TEXT NOT NULL , frequency TEXT, observations TEXT, current TEXT);
CREATE TABLE somatometria ( id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, peso REAL, talla REAL, imc REAL, circ_abdominal REAL, temp REAL, systolic INTEGER, diastolic INTEGER, fcard INTEGER, fresp INTEGER, o2 INTEGER, glucemia REAL, users_id INTEGER ,registered_by INTEGER);




## REQUIREMENTS
Requirements.txt has the requirements for this project:
•	Flask
•	Flask-Session
•	pytz
•	SQLAlchemy

## README
This is the readme.md










# Routes and roles
Route	Methods	Function	Required Role / Access
/	GET, POST	index	All (according to role: supervisor, nurse or patient)
/personaldata	GET, POST	personal data	Patient
/autoaccess	GET, POST	self-access	Patient
/edit_last_nursing	POST	edit_last_nursing	Nursing
/login	GET, POST	login	Public (no session)
/register	GET, POST	register	Public (no session)
/nursing_registry	GET, POST	nursing_registration	Nursing
/select_patient	GET, POST	select_patient	Nursing
/symptoms	GET, POST	symptoms	Patient
/event	GET, POST	event	Patient
/somatometry	GET, POST	somatometry	Patient and Nursing
/documents	GET, POST	documents	Patient
/prescriptions	GET, POST	prescriptions	Patient and Nursing
/logout	GET	logout	All with session
/validate_last	POST	validate_last	Supervisor


