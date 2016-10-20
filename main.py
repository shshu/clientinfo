import json
import webapp2

with open('home.html', 'r') as f:
    html = f.read()

class MainPage(webapp2.RequestHandler):
	def get(self):
		ip = self.request.remote_addr
		country = self.request.headers.get('X-AppEngine-Country')
		region =  self.request.headers.get('X-AppEngine-Region')
		city = self.request.headers.get('X-AppEngine-City')
		country_flag = '<img src="/flags-mini/{country}.png">'.format(country = country.lower())
		self.response.write(html.format(ip, country_flag, country, region, city))
		
class IpPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		ip = self.request.remote_addr
		self.response.write(ip)
		
class CountryPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		country = self.request.headers.get('X-AppEngine-Country')
		self.response.write(country)

class FlagPage(webapp2.RequestHandler):
	def get(self):
		country = self.request.headers.get('X-AppEngine-Country')
		self.response.write('<html><body><img src="/flags/{country}.png" /></body></html>'.format(country =country.lower()))
		
class HeadersPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		json_d = {}
		for a in self.request.headers:
			if 'X-Appengine' not in a and 'X-Cloud-Trace-Contex' not in a:
				json_d[a] = self.request.headers[a]
		self.response.write(json.dumps(json_d))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/ip', IpPage),
	('/country', CountryPage),
	('/flag', FlagPage),
	('/json/headers', HeadersPage),
], debug=False)