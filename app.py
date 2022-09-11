from flask import Flask, render_template, jsonify, request, redirect, url_for
import traceback

app = Flask(__name__)
app.debug = True

#example back end data the frontend would need to access
nameList = ['Jacek', 'Gerwazy', 'Tadeusz', 'Sędzia', 'Joe']

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#this returns to user a staticly rendered template if they just enter our page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', encoding='utf-8')

#this returns to user a staticly rendered template that CHANGES depending on python variables
@app.route('/names', methods=['GET'])
def names():
    global nameList
    favouriteName = 'Ordon'
    return render_template('names.html', encoding='utf-8', names=nameList, fav=favouriteName)#here we pass variables to a static template

@app.route('/post', methods=['GET'])
def post():
    return render_template('post.html', encoding='utf-8')

#do work and return only a value based on input hidden in POST request
@app.route('/post/work', methods=['POST'])
def postWork():
    try:
        name = request.json
        return jsonify(len(name)) #here we just return a value for the frontend to handle
    except Exception as e: #proper error handling
        resp = jsonify(success=False, error=type(e).__name__)
        resp.status_code = 400 #generic error on their side
        logging.error(type(e).__name__ + ' in' + traceback.extract_tb(e.__traceback__, 1).format()[0]) #push error to logging
        return resp

#here we do work based on input in the url
@app.route('/post/work/<string:name>', methods=['GET'])
def postWorkGet(name):
    return jsonify(len(name)) #here we just return a value for the frontend to handle

@app.route('/add', methods=['GET'])
def add():
    return render_template('add.html', encoding='utf-8')

#here we handle POST to add a new name to the list. If something goes wrong we return the right error message
@app.route('/add/work', methods=['POST'])
def addWork():
    try:
        name = request.form['nameInput']
        try:
            global nameList
            nameList.append(name)
            #here we create the success response. How you do it is your choice, but to return something like this is standard (code and text)
            resp = jsonify(success=True)
            resp.status_code = 200
            logging.info('Added ' + name + ' to the name list')
            return redirect('/add',302,resp)
        except Exception as e: #proper error handling for our processing part
            resp = jsonify(success=False) #no point telling end user what our error was
            resp.status_code = 500 #generic error on our side
            logging.error(type(e).__name__ + ' in' + traceback.extract_tb(e.__traceback__, 1).format()[0]) #push error to logging
            return resp
    except Exception as e: #proper error handling for the input handling part of the code
        resp = jsonify(success=False, error=type(e).__name__)
        resp.status_code = 400 #generic error on their side
        logging.error(type(e).__name__ + ' in' + traceback.extract_tb(e.__traceback__, 1).format()[0]) #push error to logging
        return resp
    


    
    

#this part setups the backend. Don't touch it just copy :)
if __name__ == '__main__':
    import os
    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG) #this creates an error log next to .py file
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
