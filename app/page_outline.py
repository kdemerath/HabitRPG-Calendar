from html_writer import Tag

def get():
	target = Tag('div', {'class': 'container'})(
		Tag('h1')(
			'Habitica week at a glance'
		)
	)
	framework = Tag('html')(
		Tag('head')(
			#Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/normalise.css'}),
			#Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/style.css'}),
			Tag('link', {'type': 'text/css', 'rel': 'stylesheet', 'href': 'static/app-f131975d.css'}),
			Tag('title')(
				'Habitica week at a glance'
			)
		),
		Tag('body')(
			target
		)
	)
	framework.set_insert_point(target)
	return framework
