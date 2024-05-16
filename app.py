from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb
import pickle

app = Flask(__name__)

# Konfigurasi koneksi ke MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bipolar'

mysql = MySQL(app)

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/biodata")
def biodata():
    return render_template('biodata.html')

@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/hasil")
def hasil():
    return render_template('hasil.html')

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        nama = request.form['name']
        email = request.form['email']
        telepon = request.form['phone']
        tanggal_lahir = request.form['tanggal_lahir']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (name, email, phone, tanggal_lahir) VALUES (%s, %s, %s, %s)", (nama, email, telepon, tanggal_lahir))
            mysql.connection.commit()
            user_id = cur.lastrowid
            cur.close()
            return redirect(url_for('form_with_id', user_id=user_id))
        except MySQLdb.Error as e:
            print(f"Error: {e}")
            return "Terjadi masalah saat menambahkan biodata Anda"

@app.route("/form/<int:user_id>")
def form_with_id(user_id):
    return render_template('form.html', user_id=user_id)


@app.route("/submitt", methods=['POST'])
def submitt():
    if request.method == 'POST':
        user_id = request.form['user_id']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        p6 = request.form['p6']
        p7 = request.form['p7']
        p8 = request.form['p8']
        p9 = request.form['p9']
        p10 = request.form['p10']
        p11 = request.form['p11']
        p12 = request.form['p12']
        p13 = request.form['p13']
        
        # Menyimpan jawaban pengguna ke dalam database
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO answer (user_id, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13))
            mysql.connection.commit()
            cur.close()
            
            # Prediksi hasil berdasarkan jawaban pengguna
            input_data = [[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]]
            prediction = model.predict(input_data)
            
            # Simpan hasil prediksi ke dalam database
            cur = mysql.connection.cursor()
            cur.execute("UPDATE answer SET hasil=%s WHERE user_id=%s", (prediction[0], user_id))
            mysql.connection.commit()
            cur.close()
            
            return redirect(url_for('hasil', prediction=prediction[0]))
        except MySQLdb.Error as e:
            print(f"Error: {e}")
            return "Terjadi masalah saat menambahkan jawaban Anda"
    

if __name__ == "__main__":
    app.run(debug=True)
