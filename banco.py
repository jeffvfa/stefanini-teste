#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb, time

# Define endereço do servidor, nome de usuário do bd, senha do usuário do bd e nome da base de dados
aServidor = "localhost"
aUsuario  = "root"
aSenha    = "chatuba"
aBanco    = "stefanini"

# Realiza a conexão com o banco
db = MySQLdb.connect(aServidor, aUsuario, aSenha, aBanco)
cursor = db.cursor() # seta o cursor para a conexão

# Função que executa os comandos SQL no banco
def Executa_SQL(pSQL):
  try:
    cursor.execute(pSQL)
    db.commit()
    return 1
  except:
    print("Erro: Não foi possível executar o SQL")
    db.rollback()
    return 0

# Função que executa comandos SQL (Select)
def Busca_SQL(pSQL):
  try:
    cursor.execute(pSQL)
    results = cursor.fetchall()
    return results
  except:
    print("Erro: Não foi possível buscar os dados")
    return 0

def Create_user(ilogin,inome,itipo,isenha):
    QUERY = "insert into users(login, name, type, password) values ('" + str(ilogin) + "', '" + str(inome) + "', " + str(itipo) + ", md5('" + str(isenha) + "'));"
    result = Executa_SQL(QUERY)

    # TODO: inserir os ponto também "insert into records (idUser, day,month,year,inrec) values (1,1,1,1,current_timestamp);"


    id = get_userid(ilogin)

    for i in xrange(0,365):
      date = sum_period(i)
      QUERY = "insert into records (idUser, day,month,year) values ("+ str(id) +", "+ str(date[0]) +", "+ str(date[1]) +", "+ str(date[2]) +");"
      result = Executa_SQL(QUERY)

    return result

def Delete_user(ilogin):
    QUERY = "delete from users where login like '" + str(ilogin) + "';"
    result = Executa_SQL(QUERY)
    if result == 0:
        print("login não encontrado")
    return result

def get_userid(ilogin):
    QUERY = "select id from users where login like '" + ilogin +"' ;"

    result = Busca_SQL(QUERY)

    if result == 0:
      return 0
    return ((result[0])[0])


def Sign_in(ilogin, ipass):
    QUERY = "select login,name,type from users where login like '" + str(ilogin) + "' and password like "+ "md5('" + str(ipass) + "');"
    result = Busca_SQL(QUERY)
    return result

def sum_period(periodo):
  QUERY = "select year(date_add(sysdate(), interval "+ str(periodo) +" day));"
  result = Busca_SQL(QUERY)
  year = ((result[0])[0])

  #print year

  QUERY = "select month(date_add(sysdate(), interval "+ str(periodo) +" day));"
  result = Busca_SQL(QUERY)
  month = ((result[0])[0])

  #print month

  QUERY = "select day(date_add(sysdate(), interval "+ str(periodo) +" day));"
  result = Busca_SQL(QUERY)
  day = ((result[0])[0])

  #print day

  list = [day, month, year]

  return list


def record_in(ilogin, day, month, year):
  id = get_userid(ilogin)
  QUERY = "update records set inrec = (CURRENT_TIMESTAMP()) where iduser =" + str(id) + " and day = " +  str(day) +" and month = " +  str(month) +  " and year = " +  str(year) +";"
  result = Executa_SQL(QUERY)
  return result

def record_out(ilogin, day, month, year):
  id = get_userid(ilogin)
  QUERY = "update records set outrec = (CURRENT_TIMESTAMP()) where iduser =" + str(id) + " and day = " +  str(day) +" and month = " +  str(month) +  " and year = " +  str(year) +";"
  result = Executa_SQL(QUERY)
  return result

def record_brakin(ilogin, day, month, year):
  id = get_userid(ilogin)
  QUERY = "update records set brakin = (CURRENT_TIMESTAMP()) where iduser =" + str(id) + " and day = " +  str(day) +" and month = " +  str(month) +  " and year = " +  str(year) +";"

  result = Executa_SQL(QUERY)
  return result

def record_breakout(ilogin, day, month, year):
  id = get_userid(ilogin)
  QUERY = "update records set breakout = (CURRENT_TIMESTAMP()) where iduser =" + str(id) + " and day = " +  str(day) +" and month = " +  str(month) +  " and year = " +  str(year) +";"
  result = Executa_SQL(QUERY)
  return result

def today():
    QUERY = "select day(current_timestamp()), month(current_timestamp()), year(current_timestamp());"
    result = Busca_SQL(QUERY)

    return result

def close_connection():
    db.close()

def get_registers(ilogin):
    id = get_userid(ilogin)
    QUERY= "select day,month,year,inRec, outRec , breakOut , brakIn  from records where iduser = " + str(id) +";"
    result = Busca_SQL(QUERY)
    return result
#Create_user('julio','julio da mata',0,'senha')
