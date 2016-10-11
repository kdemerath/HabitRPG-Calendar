import datetime
import calendar
import markdown
import page_outline
import traceback
import re
import requests
import json
from html_writer import Tag

def get_tasks(uuid, ukey, time_offset):
	heads = {
		'x-api-user': uuid,
		'x-api-key': ukey,
		'content-type': 'application/json'
	}
	# ToDos
	r = requests.get('https://habitica.com/api/v3/tasks/user', headers = heads)
	tasks = json.loads(str(r.content, encoding = 'utf-8'))
	tasks = tasks['data']
	tasks_by_date = {}
	display_dates = get_display_dates()
	for i in tasks:
		if i['type'] == 'todo':
			if 'date' in i:
				datetext = i['date']
				if datetext != None:
					dateparts = re.split(r'\-|\:|\.|T|Z', datetext)
					dateparts = [int(i) for i in dateparts if i.isnumeric()]
					dto = datetime.datetime(dateparts[0], dateparts[1], dateparts[2], dateparts[3])
					# This should fix the off-by-one issue.
					dto += datetime.timedelta(hours = 12)
					item = (i['text'], i['notes'])
					dto = dto.date() # Remove the time part.
					if dto in tasks_by_date:
						tasks_by_date[dto].append(item)
					else:
						tasks_by_date[dto] = [item]
		elif i['type'] == 'daily':
			if 'frequency' in i:
				frequencytext = i['frequency']
				if frequencytext != None:
					if frequencytext == 'weekly':
						if i['repeat'].get('m') == True:
							dto = display_dates[0]
							dto = dto.date()
							print(dto)
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
						if i['repeat'].get('t') == True:
							dto = display_dates[1]
							dto = dto.date()
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
						if i['repeat'].get('w') == True:
							dto = display_dates[2]
							dto = dto.date()
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
						if i['repeat'].get('th') == True:
							dto = display_dates[3]
							dto = dto.date()
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
						if i['repeat'].get('f') == True:
							dto = display_dates[4]
							dto = dto.date()
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
						if i['repeat'].get('s') == True:
							dto = display_dates[5]
							dto = dto.date()
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
						if i['repeat'].get('su') == True:
							dto = display_dates[6]
							dto = dto.date()
							item = (i['text'], i['notes'])
							if dto in tasks_by_date:
								tasks_by_date[dto].append(item)
							else:
								tasks_by_date[dto] = [item]
	
	return tasks_by_date

def get_display_dates():

	this_year = datetime.datetime.now().year
	this_month = datetime.datetime.now().month
	this_day = datetime.datetime.now().day
	this_weekday = calendar.weekday(this_year, this_month, this_day)

	#def dates_for_month(year, month):
	#	if month > 12:
	#		month -= 12
	#		year += 1
	#	return calendar.Calendar().itermonthdates(year, month)

	display_dates = set()

	#for i in range(datetime.datetime.now().month, datetime.datetime.now().month + 1):
	#	display_dates = display_dates.union(set(dates_for_month(this_year, i)))
	
	for i in range(0 - this_weekday, 7 - this_weekday):
		display_dates.add(datetime.datetime.now() + datetime.timedelta(days=i))

	display_dates = list(display_dates)
	display_dates.sort(key = lambda x: x.day)
	display_dates.sort(key = lambda x: x.month)
	display_dates.sort(key = lambda x: x.year)

	return display_dates

def make_cal(uuid, ukey, timezone):

	# HabitRPG Stuff

	try:

		# Date stuff

		timezone_delta = datetime.timedelta(hours = int(timezone))

		dto_now = datetime.datetime.now()
		dto_now += timezone_delta
		current_date = '{}/{}/{}'.format(dto_now.day, dto_now.month, dto_now.year)

		display_dates = get_display_dates()
		# print(display_dates)
		
		# Get tasks

		tasks_by_date = get_tasks(uuid, ukey, timezone_delta)

		# HTML Stuff

		days_of_week = [
			'Monday',
			'Tuesday',
			'Wednesday',
			'Thursday',
			'Friday',
			'Saturday',
			'Sunday'
		]

		months_of_year_short = [
			'Jan', 'Feb', 'Mar', 'Apr',
			'May', 'Jun', 'Jly', 'Aug',
			'Sep', 'Oct', 'Nov', 'Dec'
		]

		# Construct row of table
		the_table = Tag('table', {'class': 'myTable'})(
			Tag('tr')(
				*[Tag('td')(Tag('p')(i)) for i in days_of_week]
			)
		)
		print('calender aufbauen')
		for i in range(0, len(display_dates), 7):
			row = Tag('tr')
			for j in display_dates[i: i + 7]:
				text = '{} {}'.format(j.day, months_of_year_short[j.month - 1])
				datetext = Tag('p', {'class': 'smallText'})(text)
				contents_html = ''
				print(j)
				for k in tasks_by_date.get(j.date, []):
					markdown_html = markdown.markdown(k[0])
					if k[1]:
						markdown_html = '<span title="{}">{}</span>'.format(k[1], markdown_html)
					contents_html += markdown_html
				cell = Tag('td')(datetext, contents_html)
				if j.month % 2 == 0:
					cell['class'] = 'lightBackground'
				if j.month == dto_now.month and j.day == dto_now.day:
					cell['class'] = 'blueBackground'
				row(cell)
			the_table(row)

		html_framework = page_outline.get()
		html_framework(
			Tag('p')(
				'Current Date: ',
				current_date,
				' (UTC + ', timezone, ')'
			),
			the_table
		)

		return html_framework

	except Exception as e:

		trace = str(traceback.format_exc())

		html_framework = page_outline.get()
		html_framework(
			Tag('p')(
				'Something went wrong!',
				Tag('br'),
				'Go to the ', Tag('a', {'href': '/settings'})('settings page'), ' and input your details again.',
				Tag('br'),
				'If the problem keeps orruring, you can go to the ',
				Tag('a', {'href': 'https://github.com/DXsmiley/HabitRPG-Calendar', 'target': '_blank'})('GitHub page'),
				' and talk to DXsmiley about it. Alternatively, send me a message on HabitRPG (@DXsmiley).',
				Tag('br'),
				Tag('br'),
				'Error occurred: ',
				str(e),
				Tag('br'),
				'Traceback: ',
				Tag('br'),
				trace
			)
		)

		return str(html_framework)
