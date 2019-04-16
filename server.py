from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key= 'lalitha'
@app.route('/')
def routingTo():
    mysql = connectToMySQL("first_flask")
    selctQuery = 'select name from dojo_location;'
    locationsList = mysql.query_db(selctQuery, None)
    mysql = connectToMySQL("first_flask")
    selctQuery = 'select name from dojo_languages;'
    skillsList = mysql.query_db(selctQuery, None)
    print('myDict=', locationsList)
    print('skillsList=', skillsList)
    return render_template('form.html', locList=locationsList, skillsList=skillsList)

@app.route('/registration', methods=['POST'])
def goToResults():
    is_valid = True
    name = request.form['name']
    if len(name) == 0:
        is_valid = False
        flash('Please enter a name')

    location = request.form['location']
    if len(location) == 0:
        is_valid = False
        flash('Please select a location')

    lang = request.form['language']
    if len(lang) == 0:
        is_valid = False
        flash('Please select a language')
    
    comment = request.form['comment']
    if len(comment) > 121:
        is_valid = False
        flash('Max limit for the comments is 120 characters')
    
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL("first_flask")
        insertQuery = 'insert into dojo_survey (name, location, language, comment) values (%(name)s,%(location)s,%(language)s, %(comment)s);'
        data = {
            'name': name,
            'location' : location,
            'language' : lang,
            'comment' : comment
        }
        id = mysql.query_db(insertQuery, data)
        return render_template('results.html', name=name, location=location, lang=lang, comment=comment)

if __name__ == '__main__':
    app.run(debug=True)