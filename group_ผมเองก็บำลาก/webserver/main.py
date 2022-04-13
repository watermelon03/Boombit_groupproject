import pymysql
# from app import app
from config import mysql
from flask import jsonify,Flask
from flask import flash, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_start/<int:serial>',methods=['GET'])
def get_start(serial):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM play WHERE serial =%s", serial)
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()	

@app.route('/get_record/<int:serial>',methods=['GET'])
def get_record(serial):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM record WHERE serial =%s", serial)
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()		

@app.route('/is_start/<int:serial>',methods=['GET'])
def is_start(serial):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT playing FROM play WHERE serial =%s", serial)
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/status_playing/<int:serial>/<int:playing>',methods=['GET'])
def status_playing(serial,playing):
	try:	
		sqlQuery = "UPDATE play SET playing=%s WHERE serial = %s"
		bindData = (playing, serial,)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sqlQuery, bindData)
		conn.commit()
		respone = jsonify("Update status playing successfully!")
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/recorded/<int:serial>',methods=['POST'])
def recorded(serial):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO record (serial, name, mode, playing) SELECT serial, name, mode, playing FROM play WHERE serial=%s", serial)
		conn.commit()
		respone = jsonify('Record updated successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/add_time_result',methods=['POST'])
def add_time():
	try:
		_json = request.json
		_time = _json['time']
		_serial = _json['serial']
		_result = _json['result']
		print(_json)
		if _time and _serial and _result and request.method == 'POST':			
			sqlQuery = "UPDATE record SET time=%s ,result=%s WHERE serial=%s"
			bindData = (_time,_result,_serial,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('Add time and result successfully!')
			respone.status_code = 200
			# empRows = cursor.fetchall()
			# respone = jsonify(empRows)
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/start_web',methods=['POST'])
def start_web():
	try:
		json = request.json
		name = json['name']
		mode = json['mode']
		serial = json['serial']
		if name and mode and serial and request.method == 'POST':
			SQL_Query = "INSERT INTO play(serial, name, mode, playing) VALUES(%s,%s,%s,0)"
			data = (serial, name, mode,)
			connection =mysql.connect()
			Pointer = connection.cursor()
			Pointer.execute(SQL_Query, data)
			connection.commit()
			response = jsonify('Update play table successfully!')
			response.status_code = 200
			return response
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		Pointer.close() 
		connection.close()

@app.route('/delete_play/<int:serial>', methods=['DELETE'])
def delete_play(serial):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM play WHERE serial =%s",serial)
		conn.commit()
		respone = jsonify('Deleted from play successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run(host='0.0.0.0' ,port='5000', debug=True)
