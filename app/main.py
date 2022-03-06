from flask import Flask,render_template,request
import sqlite3 as sql
import requests
import json

api_data = requests.get("https://age-of-empires-2-api.herokuapp.com/api/v1/civilizations")
# Deserialization - the act of converting a string to an object
text = json.loads(api_data.text)
# inside civilizations key
new_text = text["civilizations"]
#remove unwanted keys
wanted_keys = {"id","name","army_type","expansion"}
#list of dictinaries
l = [{k:v for k, v in i.items() if k in wanted_keys} for i in new_text]
l_new = l[0]

conn = sql.connect('database.db')
cur = conn.cursor()
# Check if table exists
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Civilizations' ''')

if cur.fetchone()[0]!=1 :
    cur.execute(''' CREATE TABLE IF NOT EXISTS Civilizations (id number,name text,army_type text,expansion text)''')
    for l_new in l:
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in l_new.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in l_new.values())
        sqll = "INSERT INTO %s (%s) VALUES (%s);" % ('Civilizations', columns, values)
        cur.execute(sqll)

conn.commit()
conn.close()

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/addnew')
def new_civilization():
    return render_template('civilization.html')

@app.route("/addrec",methods= ['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                id = request.form['id']
                name = request.form['name']
                army_type = request.form['army_type']
                expansion = request.form['expansion']
                if id == "" or name == "":
                    msg = "Id or name can't be empty"
                    return render_template('result.html')
                cur = con.cursor()
                cur.execute("INSERT INTO Civilizations VALUES (:id,:name,:army_type,:expansion)",(id,name,army_type,expansion))
                con.commit()
                msg="Success"

        except:
            con.rollback()
            msg ="Error"
        finally:
            con.close()
            return render_template('result.html',msg=msg)

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute("SELECT * FROM Civilizations")

    rows = cur.fetchall()

    return render_template("list.html", rows = rows)


@app.route('/d_specify')
def d_specify():
    return render_template('remove.html')


@app.route("/d_specific", methods=['POST', 'GET'])
def d_specific():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                cur = con.cursor()
                field = request.form.get('options')
                if field == "id":
                    id = request.form['inputted']
                    form_selected = int(id)
                    cur.execute("DELETE FROM Civilizations WHERE id = ?", (form_selected,))
                elif field == "name":
                    name = request.form['inputted']
                    form_selected = name
                    cur.execute("DELETE FROM Civilizations WHERE name = ?", (form_selected,))
                elif field == "army_type":
                    army_type = request.form['inputted']
                    form_selected = army_type
                    cur.execute("DELETE FROM Civilizations WHERE army_type = ?", (form_selected,))
                elif field == "expansion":
                    expansion = request.form['inputted']
                    form_selected = expansion
                    cur.execute("DELETE FROM Civilizations WHERE expansion = ?", (form_selected,))

                con.commit()
                msg = "success"
        except:
            con.rollback()
            msg = "Error"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

@app.route('/u_specify')
def u_specify():
    return render_template('update.html')

@app.route("/u_specific", methods=['POST', 'GET'])
def u_specific():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                cur = con.cursor()
                field = request.form.get('options')
                id = int(request.form['id'])
                if field == "name":
                    name = request.form['inputted']
                    form_selected = name
                    cur.execute("UPDATE Civilizations SET name=? WHERE id=?", (form_selected,id))
                elif field == "army_type":
                    army_type = request.form['inputted']
                    form_selected = army_type
                    cur.execute("UPDATE Civilizations SET army_type=? WHERE id=?", (form_selected, id))
                elif field == "expansion":
                    expansion = request.form['inputted']
                    form_selected = expansion
                    cur.execute("UPDATE Civilizations SET expansion=? WHERE id=?", (form_selected, id))
                con.commit()
                msg = "Successfully updated."
        except:
            msg = "Update failed."
            con.rollback()
        finally:
            con.close()
            return render_template('result.html', msg=msg)

@app.route('/s_specify')
def s_specify():
    return render_template('select.html')

@app.route('/s_specific', methods=['POST', 'GET'])
def s_specific():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                field = request.form.get('options')
                selected_input = request.form.get('inputted')
                if field == "id":
                    if isinstance(selected_input,str):
                        try:
                            selected_input = int(selected_input)
                            msg = "Success"

                        except:
                            msg = "Id cannot be str"
                            return render_template('result.html', msg=msg)

                        finally:
                            cur.execute("SELECT * FROM Civilizations WHERE id = ? ", (selected_input,))
                            con.close()
                            rows = cur.fetchall()
                            return render_template('result.html',rows = rows, msg=msg)

                    cur.execute("SELECT * FROM Civilizations WHERE id = ? ", (selected_input,))
                if field == "name":
                    cur.execute("SELECT * FROM Civilizations WHERE name = ? ", (selected_input,))
                if field == "army_type":
                    cur.execute("SELECT * FROM Civilizations WHERE army_type = ? ", (selected_input,))
                if field == "expansion":
                    cur.execute("SELECT * FROM Civilizations WHERE expansion = ? ", (selected_input,))
                msg = "Successfully selected"
                rows = cur.fetchall()
        except:
            con.rollback()
            msg = "Failed to select"
            rows = cur.fetchall()
        finally:
            con.close()
            try:
                rows
            except:
                rows = []
            return render_template('list.html', rows = rows , msg=msg)


if __name__ == "__main__":
    app.run(port = 5000,host="0.0.0.0")