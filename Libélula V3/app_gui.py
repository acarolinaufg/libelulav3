from flask import Flask, render_template,request,redirect,url_for,flash,abort,session,jsonify
import json
import os.path
from werkzeug.utils import secure_filename
import numpy as np
import pickle
import psycopg2
from psycopg2 import Error
from flask_sqlalchemy import SQLAlchemy
#carregando o modelo
model1 = pickle.load(open('models/Modelo_treinado_libeluaCO2.pkl', 'rb'))
model2 = pickle.load(open('models/Modelo_treinado_libeluaEnergia.pkl', 'rb'))
model3 = pickle.load(open('models/Modelo_treinado_libeluaHeat.pkl', 'rb'))

#Iniciando o BD
#Iniciando o app
app = Flask(__name__)
app.secret_key = 'asdfghjk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ana575@localhost:5432/libelulaDB'


db = SQLAlchemy(app)

classe_t1 = classe_t2 =classe_t3 = 0
#Rotas do aplicativo
@app.route('/')
def inicio():
    return render_template('tte.html', codes = session.keys(),text1=classe_t1,text2=classe_t2,text3=classe_t3)
    #return redirect(url_for('comentario'))


@app.route('/adicionar', methods =['GET','POST'])
def adc():
    if request.method == 'POST':
        coment = {'Brassagem': 0, 'Centrifuga':0, 'Filtração':0, 'L_501':0, 'L_503':0, 'L_511':0,'L_511_Refri':0,'L_512':0,'L_521':0,'L_551':0,'L_561':0,'L_562':0}
        
        coment['Brassagem'] = request.form['Brassagem']
        coment['Centrifuga'] = request.form['Centrifuga']
        coment['Filtração'] = request.form['Filtracao']
        coment['L_501'] = request.form['L_501']
        coment['L_503'] = request.form['L_503']
        coment['L_511'] = request.form['L_511']
        coment['L_511_Refri'] = request.form['L_511_Refri']
        coment['L_512'] = request.form['L_512']
        coment['L_521'] = request.form['L_521']
        coment['L_551'] = request.form['L_551']
        coment['L_561'] = request.form['L_561']
        coment['L_562'] = request.form['L_562']
        
        #==================================================================================
      
        teste = np.array([[coment['L_501'],coment['L_503'],coment['L_511'],coment['L_511_Refri'],coment['L_512'],coment['L_521'],
        coment['L_551'],coment['L_561'],coment['L_562'],coment['Brassagem'],coment['Centrifuga'],coment['Filtração']]]) 

        global classe_t1, classe_t2, classe_t3

        classe_t1 = 0
        classe_t2 = 0
        classe_t3 = 0



        #Predizendo o valor do BS 
        
        CO_2 = model1.predict(teste)[0]
        energia = model2.predict(teste)[0]
        heat = model3.predict(teste)[0]
        print("O valor predito de CO2 é: {}" .format(str(CO_2)))
        print("O valor predito de energia é: {}" .format(str(energia)))
        print("O valor predito de heat é: {}" .format(str(heat)))

        #===================================================================================
         #injetando no banco de dados
        
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO DADOS_lib (L_501,L_503,L_511C,L_511R,L_512,L_521,L_551,L_561,L_562,brassagem,centrifuga,filtracao) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        record_to_insert = (coment['L_501'],coment['L_503'],coment['L_511'],coment['L_511_Refri'],coment['L_512'],coment['L_521'],
                            coment['L_551'],coment['L_561'],coment['L_562'],coment['Brassagem'],coment['Centrifuga'],coment['Filtração'])

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        
        #=============================================================================================
   
        
        return render_template("tte.html",text1=f'{CO_2:.2f}',text2=f'{energia:.2f}',text3=f'{heat:.2f}')
    if request.method == "GET":
        return render_template("tte.html",text_1=0,text2=0,text3=0)
@app.route('/pg_inicial')
def index():
    return redirect(url_for('inicio'))       
 
    

app.run(debug=True, host='0.0.0.0')