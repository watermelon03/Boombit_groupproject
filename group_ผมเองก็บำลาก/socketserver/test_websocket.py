import socketserver
import requests
from flask import jsonify
import json
#URL = "http://526a-2001-44c8-4446-9790-cc50-4af7-9ae-1512.ap.ngrok.io/"
URL = "http://ea99-1-46-131-201.ap.ngrok.io/"
class MyTCPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		data_s = self.data.decode("utf-8").split(':')
		code = data_s[0]
		self.how_to_do(code , data_s)
		# just send back the same data, but upper-cased
		#self.request.sendall(self.data.upper())
		#self.request.send(b'test back \n')

	def how_to_do(self,code , data_s):
		if code == 'hello':
			#request to backend place here
			rj = {}
			try:
				r = requests.get(URL+'status_playing/'+str(data_s[1])+"/1")
			except Exception as err:
				print(err)
			try:
				r2  = requests.get(URL+"get_start/"+str(data_s[1]))
			except Exception as err:
				print(err)
				
			#print(r2.text)
			rj = json.loads(r2.text)[0]
			name = rj['name']
			mode = rj['mode']
			#socket = self.request[1]
			msg = name+":"+str(mode)
			try :
				print("seng msg back ",msg)
				self.request.sendall(bytes(msg,"utf-8"))
			except Exception as err:
				print(err)
			
		elif code == 'bro im done':
			serial = str(data_s[1])
			record = str(data_s[2])
			res = data_s[3]
			d = {'serial': serial , 'time' : record , 'result':res}
			try :
				r = requests.post(URL+'recorded/'+serial)	
				r2 = requests.post(URL+'add_time_result', json=d)	
			except Exception as err:
				print(err)
			print(code)
			#request record goes here


if __name__ == "__main__":
    HOST, PORT = "localhost", 9001

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
