from flask import Flask, session, abort, render_template, request, redirect, url_for, flash
from server import app
from database_functions import *
from app.forms import AddRewardsForm, TransactionForm
from sqlalchemy import text

@app.route('/', methods=['GET', 'POST'])
def login_page():
    #return render_template('login.html')
    return redirect(url_for('cadet_landing_page'))

@app.route('/cadet_landing_page', methods=['GET', 'POST'])
def cadet_landing_page():
	con_status = connect_database()

	# Get all rows of db.table cadet
	record = read_data_cadet(con_status.cursor)

	close_database(con_status.con, con_status.cursor)
	return render_template('cadet_landing_page.html', table=record)

@app.route('/reward_landing_page', methods=['GET', 'POST'])
def reward_landing_page():
	con_status = connect_database()

	# Get all rows of db.table reward
	record = read_data_reward(con_status.cursor)

	close_database(con_status.con, con_status.cursor)
	return render_template('reward_landing_page.html', table=record)

@app.route('/rewards_add', methods=['GET','POST'])
def rewards_add():
	form = AddRewardsForm()

	if form.is_submitted():
		# Get user input, and con. to db
		result = request.form
		con_status = connect_database()	

		# Add the reward to db
		add_reward(result, con_status.cursor, con_status.con)

		# Close db con.
		close_database(con_status.con, con_status.cursor)
		return render_template('rewards_add.html', result=result)

		# ADD flash, confirming submission of reward to database
	
	return render_template('rewards_add.html', form=form)

@app.route('/transaction_landingPage', methods=['GET','POST'])
def transaction_landingPage():
	# Con to database
	con_status = connect_database()
	form = TransactionForm()

	# Get data to populate form
	names = get_cadet_name(con_status.cursor, con_status.con)
	rewards = get_reward_name(con_status.cursor, con_status.con)


	form.name.choices = [(name[2], name[0] + " " + name[1]) for name in names]
	form.reward.choices = [(reward[0], reward[1]) for reward in rewards]
	form.quant.choices = [(str(n), n) for n in range(1,10)]

	if form.is_submitted():
		result = request.form
		con_status = connect_database()

		cadet_id = request.form.get('name')
		form_name = get_form_name(con_status.cursor, con_status.con, cadet_id)
		print(type(form_name))
		print(*form_name)


	# Close db handle and con
	close_database(con_status.con, con_status.cursor)

	return render_template('transaction_landingPage.html', form=form);