from datetime import datetime
from bs4 import BeautifulSoup

def test_login_logout_successful(client, clubs):
	email = clubs[0]['email']

	# login
	response = client.post('/showSummary', data={'email': email})
	assert response.status_code == 200
	assert response.request.path == '/showSummary'

	# logout
	response = client.get('/logout', follow_redirects=True)
	assert response.status_code == 200
	assert response.request.path == '/'

def test_login_booking_successful(client, clubs, competitions):
	club = clubs[0]
	email = club['email']
	competition = [comp for comp in competitions if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()][0]
	
	# login
	response = client.post('/showSummary', data={'email': email})
	assert response.status_code == 200
	assert response.request.path == '/showSummary'

	# booking
	path = f"/book/{competition['name']}/{club['name']}"
	response = client.get(path)
	assert response.status_code == 200
	assert response.request.path == path
	assert "How many places?" in response.get_data(as_text=True)

def test_login_booking_purchase_successful(client, clubs, competitions):
	club = clubs[0]
	email = club['email']
	competition = [comp for comp in competitions if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()][0]
	
	# login
	response = client.post('/showSummary', data={'email': email})
	assert response.status_code == 200
	assert response.request.path == '/showSummary'

	# booking
	path = f"/book/{competition['name']}/{club['name']}"
	response = client.get(path)
	assert response.status_code == 200
	assert response.request.path == path
	assert "How many places?" in response.get_data(as_text=True)

	# purchase
	data = {"club": club['name'], "competition": competition['name'], "places": "5"}
	response = client.post('/purchasePlaces', data=data)
	assert response.status_code == 200
	assert response.request.path == '/purchasePlaces'
	assert "Great-booking complete!" in response.get_data(as_text=True)


def test_login_booking_purchase_logout_successful(client, clubs, competitions):
	club = clubs[0]
	email = club['email']
	competition = [comp for comp in competitions if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()][0]
	
	# login
	response = client.post('/showSummary', data={'email': email})
	assert response.status_code == 200
	assert response.request.path == '/showSummary'

	# booking
	path = f"/book/{competition['name']}/{club['name']}"
	response = client.get(path)
	assert response.status_code == 200
	assert response.request.path == path
	assert "How many places?" in response.get_data(as_text=True)

	# purchase
	data = {"club": club['name'], "competition": competition['name'], "places": "5"}
	response = client.post('/purchasePlaces', data=data)
	assert response.status_code == 200
	assert response.request.path == '/purchasePlaces'
	assert "Great-booking complete!" in response.get_data(as_text=True)
	
	# logout
	response = client.get('/logout', follow_redirects=True)
	assert response.status_code == 200
	assert response.request.path == '/'

def test_login_booking_purchase_logout_clubs_points_successful(client, clubs, competitions):
	club = clubs[0]
	email = club['email']
	competition = [comp for comp in competitions if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > datetime.now()][0]
	
	# login
	response = client.post('/showSummary', data={'email': email})
	assert response.status_code == 200
	assert response.request.path == '/showSummary'

	# booking
	path = f"/book/{competition['name']}/{club['name']}"
	response = client.get(path)
	assert response.status_code == 200
	assert response.request.path == path
	assert "How many places?" in response.get_data(as_text=True)

	# purchase
	data = {"club": club['name'], "competition": competition['name'], "places": "5"}
	response = client.post('/purchasePlaces', data=data)
	assert response.status_code == 200
	assert response.request.path == '/purchasePlaces'
	assert "Great-booking complete!" in response.get_data(as_text=True)
	
	# logout
	response = client.get('/logout', follow_redirects=True)
	assert response.status_code == 200
	assert response.request.path == '/'

	# clubs points
	response = client.get('/clubs/points')
	soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")
	assert response.status_code == 200
	assert len(soup.find_all("p")) == len(clubs)


