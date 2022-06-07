from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from web_forms import LoginForm, NewUserForm, ManagerChangeForm, OOOForm1, OOOForm2, OOOForm3
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(160)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

today_date = date.today().strftime('%B-%Y').split('-')
cur_month = today_date[0]
cur_year = today_date[1]
current_month = f'{cur_month}, {cur_year}'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    ohr = db.Column(db.String(20), unique=True, nullable=False)
    work_process = db.Column(db.String(50), nullable=False)
    band = db.Column(db.String(20), nullable=False)
    manager_name = db.Column(db.String(60), nullable=True)
    manager_ohr = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(1500), nullable=False)
    meeting_data = relationship("MeetingData", back_populates='user')


class MeetingData(db.Model):
    __tablename__ = 'meetingdata'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="meeting_data")
    current_month = db.Column(db.String(30))
    manager_name = db.Column(db.String(50))
    manager_ohr = db.Column(db.String(50))
    requested_meeting_date = db.Column(db.String(50))
    accepted_meeting_date = db.Column(db.String(50))
    question1 = db.Column(db.String(100))
    emp_comment1 = db.Column(db.String(502))
    manager_comment1 = db.Column(db.String(502))
    rating1 = db.Column(db.Integer)
    question2 = db.Column(db.String(100))
    emp_comment2 = db.Column(db.String(502))
    manager_comment2 = db.Column(db.String(502))
    rating2 = db.Column(db.Integer)
    question3 = db.Column(db.String(100))
    emp_comment3 = db.Column(db.String(502))
    manager_comment3 = db.Column(db.String(502))
    rating3 = db.Column(db.Integer)
    question4 = db.Column(db.String(100))
    emp_comment4 = db.Column(db.String(502))
    manager_comment4 = db.Column(db.String(502))
    rating4 = db.Column(db.Integer)
    question5 = db.Column(db.String(100))
    emp_comment5 = db.Column(db.String(502))
    manager_comment5 = db.Column(db.String(502))
    rating5 = db.Column(db.Integer)
    question6 = db.Column(db.String(100))
    emp_comment6 = db.Column(db.String(502))
    manager_comment6 = db.Column(db.String(502))
    rating6 = db.Column(db.Integer)
    question7 = db.Column(db.String(100))
    emp_comment7 = db.Column(db.String(502))
    manager_comment7 = db.Column(db.String(502))
    rating7 = db.Column(db.Integer)
    score = db.Column(db.Float)
    loc = db.Column(db.Integer)


class WAMData(db.Model):
    __tablename__ = 'wamtable'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    name = db.Column(db.String(100))
    OHR = db.Column(db.String(20))
    Band = db.Column(db.String(20))
    Grade = db.Column(db.String(20))
    combined_vertical = db.Column(db.String(50))
    vertical = db.Column(db.String(50))
    Account = db.Column(db.String(50))
    process_code = db.Column(db.String(25))
    process_name = db.Column(db.String(50))
    supervisor_id = db.Column(db.String(30))
    supervisor_name = db.Column(db.String(60))
    region = db.Column(db.String(50))
    l2_product = db.Column(db.String(50))
    session_Time = db.Column(db.Float)
    activity = db.Column(db.Float)
    breaks = db.Column(db.Float)
    value_add_breaks = db.Column(db.Float)
    idle_time = db.Column(db.Float)

    def to_dict(self):
        return {
            'date': self.date.strftime("%a, %d %b %Y"),
            'name': self.name,
            'OHR': self.OHR,
            'band': self.Band,
            'manager': self.supervisor_name,
            'session': self.session_Time,
            'activity': self.activity,
            'breaks': self.breaks,
            'value_add_breaks': self.value_add_breaks,
            'idle': self.idle_time
        }


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def update_wam(file):
    file_data = pd.read_csv(file)
    file_data = file_data.fillna(0)
    rows = file_data.iterrows()
    for index, row_data in rows:
        data = WAMData.query.filter_by(date=row_data.Date, OHR=row_data.OHR).first()
        if not data:
            l_name = row_data['Last Name']
            f_name = row_data['First Name']
            full_name = f_name + ' ' + l_name
            data = WAMData(date=datetime.strptime(row_data['Date'], "%m/%d/%Y"), last_name=l_name, first_name=f_name,
                           name=full_name,
                           OHR=row_data['OHR'], Band=row_data['Band'], Grade=row_data['Grade'],
                           combined_vertical=row_data['Combined Vertical'],
                           vertical=row_data['Vertical'], Account=row_data['Account'],
                           process_code=row_data['Process Code'],
                           process_name=row_data['Process Name'], supervisor_id=row_data['Supervisor ID'],
                           supervisor_name=row_data['Supervisor Name'],
                           region=row_data['Region'], l2_product=row_data['L2 Product'],
                           session_Time=row_data['Session Time'],
                           activity=row_data['Activity'], breaks=row_data['Breaks'],
                           value_add_breaks=row_data['Value Add Breaks'], idle_time=row_data['Idle Time'])
            db.session.add(data)
            db.session.commit()


@app.route('/api/get_wam_data')
def read_wam():
    manager_arg = request.args.get('manager')
    employee_arg = request.args.get('employee')
    last_date = date.today() - timedelta(days=1)
    first_date = last_date - timedelta(days=90)
    query = db.session.query(WAMData).filter(WAMData.Account == current_user.work_process,
                                             WAMData.date.between(first_date, last_date))
    if current_user.band == 'Band 5':
        query = query.filter(WAMData.Account == current_user.work_process, WAMData.OHR == current_user.ohr, WAMData.date.between(first_date, last_date))
    elif employee_arg != 'everyone' and employee_arg != 'None':
        query = query.filter(WAMData.Account == current_user.work_process, WAMData.OHR == employee_arg,
                             WAMData.date.between(first_date, last_date))
    elif manager_arg != 'everyone' and manager_arg != 'None':
        query = query.filter(WAMData.Account == current_user.work_process, WAMData.supervisor_id == manager_arg,
                             WAMData.date.between(first_date, last_date))

    # Search Filter

    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            WAMData.date.like(f'%{search}%'),
            WAMData.name.like(f'%{search}%'),
            WAMData.OHR.like(f'%{search}%'),
            WAMData.supervisor_name.like(f'%{search}%'),
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['date', 'name', 'manager', 'activity']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        if col_name == 'manager':
            col_name = 'supervisor_name'
        col = getattr(WAMData, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [wam_data.to_dict() for wam_data in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': WAMData.query.count(),
        'draw': request.args.get('draw', type=int),
    }


def allowed_file(filename):
    allowed_extensions = ['csv']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['wam_file']
        if not allowed_file(file.filename):
            return redirect(url_for('dashboard', message='file_upload_failed'))
        update_wam(file)
        return redirect(url_for('dashboard', message='file_uploaded'))


# Populating manager name in New user form
@app.route('/<process_work>/<band>')
def manager(process_work, band):
    if band == 'Band 5':
        manager_obj = User.query.filter_by(work_process=process_work, band='Band 4 and above').all()
        manager_list = []
        for manager in manager_obj:
            new_obj = {'id': manager.name, 'name': manager.name}
            manager_list.append(new_obj)
        return jsonify({'managers': manager_list})
    elif band == 'Band 4 and above':
        manager_list = []
        new_obj = {'id': '', 'name': ''}
        manager_list.append(new_obj)
        return jsonify({'managers': manager_list})


@app.route('/')
def home():
    return render_template('index.html', user_active=current_user.is_active)


@app.route('/dashboard')
@login_required
def dashboard():
    manager_arg = request.args.get('manager')
    employee_arg = request.args.get('employee')
    message = request.args.get('message')
    if manager_arg is None and employee_arg is None:
        manager_arg = 'everyone'
        employee_arg = 'everyone'

    last_date = date.today()
    account = current_user.work_process
    first_date = last_date - timedelta(days=91)
    if current_user.band == 'Band 5':
        user_ohr = current_user.ohr
        data = pd.read_sql_query(
            f'SELECT wamtable.id, wamtable.date, wamtable.name, wamtable."OHR", wamtable."Band", wamtable."Grade", wamtable."Account", wamtable.process_code, wamtable.process_name, wamtable.supervisor_id, wamtable.supervisor_name, wamtable.activity FROM wamtable WHERE wamtable."Account" = "{account}" AND wamtable."OHR" = "{user_ohr}" AND wamtable.date BETWEEN "{first_date}" AND "{last_date}" ORDER BY wamtable.supervisor_name ASC',
            con=db.engine)
        if not data.empty:
            fig = px.bar(data, x=data.date, y=data.activity, color=data.name, title='Per Day Session Time',
                         height=800, hover_data=["date", "name", "OHR", "activity"],
                         labels={"date": "Date", "name": "Name", "activity": "Session Time"})
            fig.update_layout(xaxis_title='Dates', yaxis_title='Session Time(in minutes)', font_family="Rockwell")
            fig.update_xaxes(tickformat="%d %b %Y", tickangle=45, rangeslider_visible=True)
            plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('dashboard/dashboard.html', plot_json=plot_json, user_active=current_user.is_active,
                                   message=message, employee_arg=current_user.ohr, manager_arg=None)
        else:
            return render_template('dashboard/dashboard.html', user_active=current_user.is_active,
                                   message='db_empty', employee_arg=current_user.ohr, manager_arg=None)
    data = pd.read_sql_query(
        f'SELECT wamtable.id, wamtable.date, wamtable.name, wamtable."OHR", wamtable."Band", wamtable."Grade", wamtable."Account", wamtable.process_code, wamtable.process_name, wamtable.supervisor_id, wamtable.supervisor_name, wamtable.activity FROM wamtable WHERE wamtable."Account" = "{account}" AND wamtable.date BETWEEN "{first_date}" AND "{last_date}" ORDER BY wamtable.supervisor_name ASC',
        con=db.engine)
    if not data.empty:
        manager_df = data[['supervisor_name', 'supervisor_id']].drop_duplicates()
        if employee_arg != 'everyone' and employee_arg is not None:
            manager_ohr = data[data['OHR'] == employee_arg]['supervisor_id'].reset_index()['supervisor_id'][0]
            data = data[data['supervisor_id'] == manager_ohr]
            emp_df = data[['name', 'OHR']].drop_duplicates()
            data = data[data['OHR'] == employee_arg]
            if not data.empty:
                fig = px.bar(data, x=data.date, y=data.activity, color=data.name, title='Per Day Session Time',
                             height=800, hover_data=["date", "name", "OHR", "activity"],
                             labels={"date": "Date",  "name": "Name", "activity": "Session Time"})
                fig.update_layout(xaxis_title='Dates', yaxis_title='Session Time(in minutes)', font_family="Rockwell")
                fig.update_xaxes(tickformat="%d %b %y", tickangle=45, rangeslider_visible=True)
                fig.add_shape(type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                              x0=0, x1=1, xref="paper", y0=240, y1=240, yref="y")
                fig.add_shape(type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                              x0=0, x1=1, xref="paper", y0=540, y1=540, yref="y")
                plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template('dashboard/dashboard.html', plot_json=plot_json, manager_list=manager_df,
                                       emp_df=emp_df, manager_arg=manager_arg, employee_arg=employee_arg,
                                       user_active=current_user.is_active, message=message)
            else:
                return render_template('dashboard/dashboard.html', user_active=current_user.is_active, message='db_empty',
                                       manager_arg=manager_arg, employee_arg=employee_arg, manager_list=manager_df,
                                       emp_df=emp_df)
        if manager_arg != 'everyone' and manager_arg is not None:
            data = data[data['supervisor_id'] == manager_arg]
            emp_df = data[['name', 'OHR']].drop_duplicates()
            if not data.empty:
                fig = px.line(data, x=data.date, y=data.activity, color=data.name, title='Per Day Session Time',
                              height=800, hover_data=["date", "name", "OHR", "activity"],
                              labels={"date": "Date", "name": "Name", "activity": "Session Time"})
                fig.update_layout(xaxis_title='Dates', yaxis_title='Session Time(in minutes)', font_family="Rockwell")
                fig.update_xaxes(tickformat="%d %b %Y", tickangle=45, rangeslider_visible=True)
                plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template('dashboard/dashboard.html', plot_json=plot_json, manager_list=manager_df,
                                       emp_df=emp_df, manager_arg=manager_arg, employee_arg=employee_arg,
                                       user_active=current_user.is_active, message=message)
            else:
                emp_df = []
                return render_template('dashboard/dashboard.html', user_active=current_user.is_active, message='db_empty',
                                       manager_arg=manager_arg, employee_arg=employee_arg, manager_list=manager_df, emp_df=emp_df)
        if manager_arg == 'everyone' and employee_arg == 'everyone':
            emp_df = data[['name', 'OHR']].drop_duplicates()
            if not data.empty:
                fig = px.line(data, x=data.date, y=data.activity, color=data.name, title='Per Day Session Time',
                              hover_data=["date", "name", "OHR", "activity"], height=800,
                              labels={"date": "Date",  "name": "Name", "activity": "Session Time"})
                fig.update_layout(xaxis_title='Dates', yaxis_title='Session Time(in minutes)', font_family="Rockwell")
                fig.update_xaxes(tickformat="%d %b %Y", tickangle=45, rangeslider_visible=True)
                plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template('dashboard/dashboard.html', plot_json=plot_json, manager_list=manager_df,
                                       emp_df=emp_df, manager_arg=manager_arg, employee_arg=employee_arg,
                                       user_active=current_user.is_active, message=message)
            else:
                emp_df = []
                return render_template('dashboard/dashboard.html', user_active=current_user.is_active, message='db_empty',
                                       manager_arg=manager_arg, employee_arg=employee_arg, manager_list=manager_df,
                                       emp_df=emp_df)
    else:
        manager_df = []
        emp_df = []
        return render_template('dashboard/dashboard.html', user_active=current_user.is_active, message='db_empty',
                               manager_arg=manager_arg, employee_arg=employee_arg, manager_list=manager_df, emp_df=emp_df)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(ohr=form.ohr.data).first()
        if user is None:
            flash('User not in database. Please check your credentials and try again.')
            return redirect(url_for('login'))
        elif check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Incorrect credentials entered. Please try again.')
            return redirect(url_for('login'))
    return render_template('user/login.html', form=form, user_active=current_user.is_active)


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    form = NewUserForm()
    if form.validate_on_submit():
        new_ohr = form.ohr.data
        query = User.query.filter_by(ohr=new_ohr).first()
        if query is not None:
            flash('OHR already exists in the system. Please login instead.')
            return redirect(url_for('login'))
        new_user = User(name=form.name.data, ohr=new_ohr, work_process=form.proc.data, band=form.band.data,
                        password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('user/register.html', form=form, user_active=current_user.is_active)


@app.route('/change_manager', methods=['GET', 'POST'])
def change_manager():
    form = ManagerChangeForm()
    with open('static/text/manager_change.dat', 'r') as file:
        ohr = file.read()
    if request.method == 'POST':
        new_manager_ohr = form.manager_details.data.split('(')[1].split(')')[0].split(':')[-1].strip()
        new_manager_name = User.query.filter_by(ohr=new_manager_ohr).first().name
        emp_details = User.query.filter_by(ohr=ohr).first()
        emp_details.manager_name = new_manager_name
        emp_details.manager_ohr = new_manager_ohr
        db.session.commit()
        return redirect(url_for('dashboard', message='manager_changed'))
    return render_template('user/change_manager.html', form=form, user_active=current_user.is_active)


@app.route('/get_emp_ohr', methods=['POST'])
def get_emp_ohr():
    if request.method == 'POST':
        received_data = request.get_data()
        try:
            ohr = received_data.decode('utf-8').split('=')[-1]
            emp = User.query.filter_by(ohr=ohr).first()
            with open('static/text/manager_change.dat', 'w') as file:
                file.write(emp.ohr)
            manager_list = db.session.query(User).filter(User.work_process == emp.work_process,
                                                         User.band != 'Band 5').all()
            manager_dict = []
            for managers in manager_list:
                manager_dict.append(f'{managers.name.title()} \t (OHR: {managers.ohr})')
            return jsonify(
                {'status': 'ok', 'name': emp.name, 'ohr': emp.ohr, 'band': emp.band, 'process': emp.work_process,
                 'manager_name': emp.manager_name, 'manager_ohr': emp.manager_ohr, 'dict': manager_dict})
        except:
            return jsonify({'status': 'error'})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/meetings/create_new')
@login_required
def create_new_meetings():
    query_data = MeetingData.query.filter_by(current_month=current_month, manager_ohr=current_user.ohr).all()
    if not query_data:
        band5_details = User.query.filter_by(manager_ohr=current_user.ohr).all()
        for band5s in band5_details:
            meeting_launch = MeetingData(user_id=band5s.id, current_month=current_month,
                                         manager_name=current_user.name, manager_ohr=current_user.ohr, loc=0)
            db.session.add(meeting_launch)
            db.session.commit()
        return redirect(url_for('dashboard', message='meeting_created'))
    else:
        return redirect(url_for('dashboard', message='creating_meeting_failed'))


@app.route('/meetings/open_meetings', methods=['GET', 'POST'])
@login_required
def open_meetings():
    if current_user.band == 'Band 5':
        # Working on LOC for emp
        meeting_id = request.args.get('meet_id')
        if meeting_id:
            meeting_id = int(meeting_id)
            open_meet_data = MeetingData.query.get(meeting_id)
        else:
            open_meet_data = MeetingData.query.filter(MeetingData.user_id == current_user.id, MeetingData.loc.in_((0, 2))).first()
        loc = open_meet_data.loc
        if loc == 0:
            form = OOOForm1()
            if form.validate_on_submit():
                rating = [int(request.form.get(f"r{x}")) for x in range(1, 8)]
                open_meet_data.requested_meeting_date = datetime.strftime(
                    datetime.strptime(request.form.get("meeting_date"), "%Y-%m-%d"), "%B %d, %Y")
                open_meet_data.question1 = form.q1.label.text
                open_meet_data.emp_comment1 = form.q1.data
                open_meet_data.rating1 = rating[0]
                open_meet_data.question2 = form.q2.label.text
                open_meet_data.emp_comment2 = form.q2.data
                open_meet_data.rating2 = rating[1]
                open_meet_data.question3 = form.q3.label.text
                open_meet_data.emp_comment3 = form.q3.data
                open_meet_data.rating3 = rating[2]
                open_meet_data.question4 = form.q4.label.text
                open_meet_data.emp_comment4 = form.q4.data
                open_meet_data.rating4 = rating[3]
                open_meet_data.question5 = form.q5.label.text
                open_meet_data.emp_comment5 = form.q5.data
                open_meet_data.rating5 = rating[4]
                open_meet_data.question6 = form.q6.label.text
                open_meet_data.emp_comment6 = form.q6.data
                open_meet_data.rating6 = rating[5]
                open_meet_data.question7 = form.q7.label.text
                open_meet_data.emp_comment7 = form.q7.data
                open_meet_data.rating7 = rating[6]
                open_meet_data.loc = 1
                open_meet_data.score = ((sum(rating) * 100.0)/(len(rating) * 5.0))
                db.session.commit()
                return redirect(url_for('dashboard', message='form_submitted'))
            return render_template('meetings/meeting_start.html', form=form, user_active=current_user.is_active)
        elif loc == 2:
            form = OOOForm3()
            if form.validate_on_submit():
                open_meet_data.loc = 10
                db.session.commit()
                return redirect(url_for('dashboard', message='form_submitted'))
            return render_template('meetings/meeting_submit.html', form=form, meeting_data=open_meet_data,
                                   user_active=current_user.is_active)
        else:
            return redirect(url_for('previous_meetings'))
    else:
        return redirect(url_for('previous_meetings'))


@app.route('/open_meetings2/', methods=['GET', 'POST'])
def open_meetings2():
    if current_user.band != 'Band 5':
        meeting_id = int(request.args.get('meet_id'))
        meet_data = MeetingData.query.get(meeting_id)
        form = OOOForm2()
        if form.validate_on_submit():
            meet_data.accepted_meeting_date = datetime.strftime(
                datetime.strptime(request.form.get("meeting_date"), "%Y-%m-%d"), "%B %d, %Y")
            meet_data.manager_comment1 = form.m1.data
            meet_data.manager_comment2 = form.m2.data
            meet_data.manager_comment3 = form.m3.data
            meet_data.manager_comment4 = form.m4.data
            meet_data.manager_comment5 = form.m5.data
            meet_data.manager_comment6 = form.m6.data
            meet_data.manager_comment7 = form.m7.data
            meet_data.loc = 2
            db.session.commit()
            return redirect(url_for('dashboard', message='form_submitted'))
        return render_template('meetings/meeting_manager_comment.html', form=form, meeting_data=meet_data,
                               user_active=current_user.is_active)
    else:
        meeting_id = request.args.get('meet_id')
        return redirect(url_for('open_meetings', meet_id=meeting_id))


@app.route('/meetings/previous_meetings/details', methods=['GET', 'POST'])
def meeting_details():
    meeting_id = int(request.args.get('meeting_id'))
    meeting_data = MeetingData.query.get(meeting_id)
    form = OOOForm3()
    if form.validate_on_submit():
        return redirect(url_for('previous_meetings'))
    return render_template('meetings/meeting_submit.html', form=form, meeting_data=meeting_data,
                           user_active=current_user.is_active)


@app.route('/meetings/previous_meetings')
def previous_meetings():
    if current_user.band == 'Band 5':
        cur_meetings = db.session.query(MeetingData).filter(MeetingData.user_id == current_user.id,
                                                            MeetingData.loc.in_(('0', '2'))).all()
        pend_meetings = db.session.query(MeetingData).filter(MeetingData.user_id == current_user.id,
                                                             MeetingData.loc == 1).all()
        completed_meetings = db.session.query(MeetingData).filter(MeetingData.user_id == current_user.id,
                                                                  MeetingData.loc == 10).all()
        band5s = []
    else:
        band5s = User.query.filter_by(manager_ohr=current_user.ohr).all()
        cur_meetings = db.session.query(MeetingData).filter(MeetingData.manager_ohr == current_user.ohr,
                                                            MeetingData.loc == 1).all()
        pend_meetings = db.session.query(MeetingData).filter(MeetingData.manager_ohr == current_user.ohr,
                                                             MeetingData.loc.in_(('0', '2'))).all()
        completed_meetings = db.session.query(MeetingData).filter(MeetingData.manager_ohr == current_user.ohr,
                                                                  MeetingData.loc == 10).all()
    return render_template('meetings/prev_meeting.html', cur_meetings=cur_meetings, pend_meetings=pend_meetings,
                           completed_meetings=completed_meetings, band5s=band5s, user_active=current_user.is_active)


@app.route('/search_meeting_list', methods=['POST'])
def search_meeting_list():
    if request.method == 'POST':
        try:
            received_data = request.get_data()
            received_ohr = int(received_data.decode('utf-8').split('=')[-1])
            meeting_data_query = db.session.query(MeetingData).join(User).filter(User.ohr == received_ohr,
                                                                                 MeetingData.loc == 10).all()
            meeting_data_list = [{'ohr': received_ohr, 'month': data.current_month, 'meet_id': data.id} for data in
                                 meeting_data_query]
            return jsonify('', render_template('meetings/meetings_temp_search_result.html', search_result=meeting_data_list))
        except:
            return jsonify({'status': 404})


if __name__ == '__main__':
    app.run(debug=True)
