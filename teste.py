#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from jac.contrib.flask import JAC
from flask import Flask, render_template, request, session,redirect,url_for
import jinja2
from jac import CompressorExtension
import banco


app = Flask(__name__)
app.secret_key = 'olhoazulpiscina'

app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
app.config['COMPRESSOR_OUTPUT_DIR'] = './static'
app.config['COMPRESSOR_STATIC_PREFIX'] = '/static'
jac = JAC(app)

env = jinja2.Environment(extensions=[CompressorExtension])
env.compressor_output_dir = './static'
env.compressor_static_prefix = '/static'
env.compressor_source_dirs = './static_files'

data = []
registros = []

@app.route('/entrada')
def ponto_entrada():
    if 'login' in session:
        banco.record_in(session['login'],data[0], data[1],data[2])
        resultado = banco.get_registers(session['login'])
        registros = []
        registros.append(list(resultado))
        return render_template('restrita.html',resultado = tuple(registros))
    return redirect(url_for('home_page'))

@app.route('/saida')
def ponto_saida():
    if 'login' in session:
        banco.record_out(session['login'],data[0], data[1],data[2])
        resultado = banco.get_registers(session['login'])
        registros = []
        registros.append(list(resultado))
        return render_template('restrita.html',resultado = tuple(registros))
    return redirect(url_for('home_page'))

@app.route('/almocoent')
def ponto_entradaAl():
    if 'login' in session:
        banco.record_brakin(session['login'],data[0], data[1],data[2])
        resultado = banco.get_registers(session['login'])
        registros = []
        registros.append(list(resultado))
        return render_template('restrita.html',resultado = tuple(registros))
    return redirect(url_for('home_page'))

@app.route('/almocosai')
def ponto_saidaAl():
    if 'login' in session:
        banco.record_breakout(session['login'],data[0], data[1],data[2])
        resultado = banco.get_registers(session['login'])
        registros = []
        registros.append(list(resultado))
        print "renderiza de novo"
        return render_template('restrita.html',resultado = tuple(registros))
    return redirect(url_for('home_page'))

@app.route('/restrita')
def restrita():

    if 'login' in session:
        resultado = banco.get_registers(session['login'])
        registros = []
        registros.append(list(resultado))
        return render_template('restrita.html',resultado = tuple(registros))
    return redirect(url_for('home_page'))

@app.route('/sair')
def sair():
    session.pop('login', None)
    session.pop('name', None)
    session.pop('type', None)
    return redirect(url_for('home_page'))

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    login = ''
    senha = ''
    if request.method == 'POST':
        login = request.form.getlist('login')
        senha = request.form.getlist('senha')
        login = str(login[0])
        senha = str(senha[0])
    else:
        return redirect(url_for('home_page'))

    resultado = banco.Sign_in(login,senha)


    session['login'] = str(resultado[0][0])
    session['name'] = str(resultado[0][1])
    session['type'] = str(resultado[0][2])

    resultado = banco.today()

    data.append(str(resultado[0][0]))
    data.append(str(resultado[0][1]))
    data.append(str(resultado[0][2]))

    resultado = banco.get_registers(session['login'])
    registros = []
    registros.append(list(resultado))

    return redirect(url_for('restrita'))
    #return render_template('restrita.html',resultado = resultado)


if __name__ == '__main__':
    app.run()
