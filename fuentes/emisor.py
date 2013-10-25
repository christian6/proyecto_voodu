#!/usr/bin/env python
# -*- coding: cp1252 -*-

# example layout.py

import pygtk
pygtk.require('2.0')
import gtk
import random
import autopy
from autopy.mouse import LEFT_BUTTON, RIGHT_BUTTON
import psycopg2
from autopy import key

import os
import sys
import time
import Image
import ctypes
import zlib

#en Linux ====> import pyscreenshot as ImageGrab
from PIL import ImageGrab

import base64
import socket
from email.mime.image import MIMEImage

import threading

SaveDirectory=r'fotopantalla/'
IP_SERVIDOR = '192.168.1.22'
PUERTO_SERVIDOR = 10000
a = 0

DSN = "dbname=prueba1 user=abacouser password=abacouser host=abacotandil.no-ip.biz port=5500"

threads = list()


class LayoutExample:
    
    
    def WindowDeleteEvent(self, widget, event):
        # return false so that window will be destroyed
        return False

    def WindowDestroy(self, widget, *data):
        # exit main loop
        gtk.main_quit()

    def ButtonClicked(self, button):
        # exit main loop
        gtk.main_quit()
    
    def clicks(self):
        while a == 0:
            #levantamos la posision del puntero en el visor1 y la usamos en el emisor
            con = psycopg2.connect(DSN)
            cur = con.cursor()
            query = "select leftclick, rightclick from sesion where id = 1;"
            cur.execute(query)
            con.commit()
      
            for linea in cur.fetchall():
               # estas lineas hay que cambiarlas por las que van 
               # recuperar los valores de las coordenadas
               clickizquierdo = linea[0]
               clickderecho = linea[1]
               
               print "izquierdo:"+str(clickizquierdo)+" - "+"derecho: "+str(clickderecho)
            
               if clickizquierdo == 1:
                  autopy.mouse.click()
                  #Actualiza widthemisor
                  con = psycopg2.connect(DSN)
                  cur = con.cursor()
                  query_widthemisor = "update sesion set leftclick = 0 where id = 1;"
                  cur.execute(query_widthemisor)
                  con.commit()
                  cur.close()
            
               if clickderecho == 1:
                  autopy.mouse.click(RIGHT_BUTTON)
                  #Actualiza widthemisor
                  con = psycopg2.connect(DSN)
                  cur = con.cursor()
                  query_widthemisor = "update sesion set rightclick = 0 where id = 1;"
                  cur.execute(query_widthemisor)
                  con.commit()
                  cur.close()
    
    def rightclick(self):
        while a == 0:
           #levantamos la posision del puntero en el visor1 y la usamos en el emisor
           con = psycopg2.connect(DSN)
           cur = con.cursor()
           query = "select rightclick from sesion where id = 1;"
           print query
           cur.execute(query)
           con.commit()
      
           for linea in cur.fetchall():
              # estas lineas hay que cambiarlas por las que van 
              # recuperar los valores de las coordenadas
              clickderecho = linea[0]
              print clickderecho
            
              if clickderecho == 1:
                autopy.mouse.click(RIGHT_BUTTON)
                #Actualiza widthemisor
                con = psycopg2.connect(DSN)
                cur = con.cursor()
                query_widthemisor = "update sesion set rightclick = 0 where id = 1;"
                cur.execute(query_widthemisor)
                con.commit()
                cur.close()
    
    def posxy(self):
        a = 0
        while a == 0:
           #levantamos la posision del puntero en el visor1 y la usamos en el emisor
           con = psycopg2.connect(DSN)
           cur = con.cursor()
           query = "select posicionx, posiciony from sesion where id = 1;"
           cur.execute(query)
           con.commit()
      
           for linea in cur.fetchall():
              # estas lineas hay que cambiarlas por las que van 
              # recuperar los valores de las coordenadas
              posicx = linea[0]
              posicy = linea[1]
              autopy.mouse.move(posicx, posicy)
    
    def letra(self):
        a = 0
        while a == 0:
              #levantamos la posision del puntero en el visor1 y la usamos en el emisor
              con = psycopg2.connect(DSN)
              cur = con.cursor()
              query = "select letra, puedeescribir from sesion where id = 1;"
              cur.execute(query)
              con.commit()
         
         
              for linea in cur.fetchall():
                  # estas lineas hay que cambiarlas por las que van 
                  # recuperar los valores de las coordenadas
                  if linea[1] == 1:
                     letra = linea[0].replace('-','')

                     if letra <> '-':
                        key.type_string(letra,0)
                        #Actualiza letra a nada
                        con = psycopg2.connect(DSN)
                        cur = con.cursor()
                        query_letra = "update sesion set letra = '-' where id = 1;"
                        cur.execute(query_letra)
                        query_puedeescribir = "update sesion set puedeescribir = 0 where id = 1;"
                        cur.execute(query_puedeescribir)
                        con.commit()
                        cur.close()
               
              cur.close()
              
    def letra1(self):
        a = 0
        while a == 0:
              #levantamos la posision del puntero en el visor1 y la usamos en el emisor
              con = psycopg2.connect(DSN)
              cur = con.cursor()
              query = "select letra from sesion where id = 1;"
              cur.execute(query)
              con.commit()
         
         
              for linea in cur.fetchall():
                  # estas lineas hay que cambiarlas por las que van 
                  # recuperar los valores de las coordenadas
                
                  letra = linea[0].replace('-','')
                  print letra
                
                  if letra <> '-':
					 key.tap(letra)

                  #Actualiza letra a nada
                  con = psycopg2.connect(DSN)
                  cur = con.cursor()
                  query_letra = "update sesion set letra = '-' where id = 1;"
                  cur.execute(query_letra)
                  con.commit()
                  cur.close()
               
              cur.close()
              time.sleep(0.5)              
             
    
    def foto(self):
        a = 0
        while a == 0:
            img=ImageGrab.grab()
            saveas=os.path.join(SaveDirectory,'ScreenShot_'+str(a)+'.jpg')
            img.save(saveas)
            #redimensionar para hacerla mas chica y liviana en principio se dejaba cuadrado del tipo 800x600
            #pero en este momento, para tratar de resolver el problema de las proporciones de los movimientos
            #del mouse en el visor respecto del emisor. Por eso, el ancho y el alto se tomaran solamente la tercera
            #parte del ancho y alto de la medida que tenga la pantalla del emisor
            user32 = ctypes.windll.user32
            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            print screensize
            
            image = Image.open(SaveDirectory + 'ScreenShot_'+str(a)+'.jpg')
            width = screensize[0]
            height = screensize[1]
            image = image.resize((width, height), Image.ANTIALIAS)
            ext = ".jpg"
            image.save(SaveDirectory + 'ScreenShot_'+str(a)+ext)
            #le cambiamos la calidad, para que pesen menos al subir al servidor.
            image.save(SaveDirectory + 'ScreenShot_'+str(a)+'.jpg', quality=18)
            jpgtxt = base64.encodestring(open(SaveDirectory + 'ScreenShot_'+str(a)+'.jpg',"rb").read())
            #lo comprimo y lo envio comprimido
            #jpgtxt = base64.b64encode(zlib.compress(jpgtxt,9))
            jpgtxt = base64.b16encode(zlib.compress(jpgtxt,9))
            jpgtxt = jpgtxt.replace('AAA', 'L')
            jpgtxt = jpgtxt.replace('BBB', 'M')
            jpgtxt = jpgtxt.replace('CCC', 'N')
            jpgtxt = jpgtxt.replace('EEE', 'O')
            jpgtxt = jpgtxt.replace('FFF', 'P')
            jpgtxt = jpgtxt.replace('AA', 'Q')
            jpgtxt = jpgtxt.replace('BB', 'H')
            jpgtxt = jpgtxt.replace('CC', 'I')
            jpgtxt = jpgtxt.replace('DD', 'J')
            jpgtxt = jpgtxt.replace('EE', 'K')
            jpgtxt = jpgtxt.replace('00', 'T')
            jpgtxt = jpgtxt.replace('33', 'U')
            jpgtxt = jpgtxt.replace('44', 'V')
            jpgtxt = jpgtxt.replace('55', 'W')
            jpgtxt = jpgtxt.replace('66', 'X')
            jpgtxt = jpgtxt.replace('77', 'Y')
            jpgtxt = jpgtxt.replace('88', 'Z')
            jpgtxt = jpgtxt.replace('99', 'G')
            jpgtxt = jpgtxt.replace('AB', '+')
            jpgtxt = jpgtxt.replace('BC', '$')
            jpgtxt = jpgtxt.replace('CD', '%')
            jpgtxt = jpgtxt.replace('DE', '#')
            jpgtxt = jpgtxt.replace('EF', '*')
            jpgtxt = jpgtxt.replace('DA', '<')
            jpgtxt = jpgtxt.replace('ED', '>')
            jpgtxt = jpgtxt.replace('EC', '?')
            jpgtxt = jpgtxt.replace('BA', '¿')
            jpgtxt = jpgtxt.replace('CB', '=')
            jpgtxt = jpgtxt.replace('DC', '-')
            jpgtxt = jpgtxt.replace('FE', '!')
            jpgtxt = jpgtxt.replace('AD', '@')
            jpgtxt = jpgtxt.replace('FA', '(')
            jpgtxt = jpgtxt.replace('AF', ')')
            jpgtxt = jpgtxt.replace('FB', '|')
            jpgtxt = jpgtxt.replace('BF', '[')
            jpgtxt = jpgtxt.replace('01', ']')
            jpgtxt = jpgtxt.replace('02', '{')
            jpgtxt = jpgtxt.replace('03', '}')
            jpgtxt = jpgtxt.replace('04', '.')
            jpgtxt = jpgtxt.replace('05', 'a')
            jpgtxt = jpgtxt.replace('06', 'b')
            jpgtxt = jpgtxt.replace('07', 'c')
            jpgtxt = jpgtxt.replace('08', 'd')
            jpgtxt = jpgtxt.replace('09', 'e')
            jpgtxt = jpgtxt.replace('000', 'f')
            jpgtxt = jpgtxt.replace('111', 'g')
            jpgtxt = jpgtxt.replace('222', 'h')
            jpgtxt = jpgtxt.replace('333', 'i')
            jpgtxt = jpgtxt.replace('444', 'j')
            jpgtxt = jpgtxt.replace('555', 'k')
            jpgtxt = jpgtxt.replace('666', 'l')
            jpgtxt = jpgtxt.replace('777', 'm')
            jpgtxt = jpgtxt.replace('888', 'n')
            jpgtxt = jpgtxt.replace('999', '0')
            jpgtxt = jpgtxt.replace('FF', 'p')
            jpgtxt = jpgtxt.replace('EB', 'q')
            jpgtxt = jpgtxt.replace('DB', 'r')
            jpgtxt = jpgtxt.replace('BE', 's')
            jpgtxt = jpgtxt.replace('FD', 't')
            jpgtxt = jpgtxt.replace('FC', 'u')
            jpgtxt = jpgtxt.replace('BD', 'v')
            jpgtxt = jpgtxt.replace('DF', 'w')
            jpgtxt = jpgtxt.replace('CF', 'x')
            jpgtxt = jpgtxt.replace('CA', 'y')
            jpgtxt = jpgtxt.replace('CE', 'z')
            jpgtxt = jpgtxt.replace('AE', 'ç')
            jpgtxt = jpgtxt.replace('11', 'ª')
            jpgtxt = jpgtxt.replace('12', 'º')
            jpgtxt = jpgtxt.replace('13', '&')
            jpgtxt = jpgtxt.replace('14', '/')
            jpgtxt = jpgtxt.replace('15', '¡')
            jpgtxt = jpgtxt.replace('16', '¨')
            jpgtxt = jpgtxt.replace('17', '¬')
            jpgtxt = jpgtxt.replace('18', ':')
            jpgtxt = jpgtxt.replace('19', ',')
            jpgtxt = jpgtxt.replace('20', '_')
            jpgtxt = jpgtxt.replace('21', '~')
            jpgtxt = jpgtxt.replace('22', '"')
            jpgtxt = jpgtxt.replace('23', '´')
            jpgtxt = jpgtxt.replace('24', '^')
            jpgtxt = jpgtxt.replace('25', '·')

            #print jpgtxt            
            #enviando
            #client.sendto(jpgtxt, (IP_SERVIDOR, PUERTO_SERVIDOR))
            con = psycopg2.connect(DSN)
            cur = con.cursor()
            query = "update sesion set imagen = '"+jpgtxt+"' where id = 1;"
            cur.execute(query)
            con.commit()
            print "Actualizada la imagen"

            #levantamos la posision del puntero en el visor1 y la usamos en el emisor
            #con = psycopg2.connect(DSN)
            #cur = con.cursor()
            #query = "select posicionx, posiciony, leftclick, rightclick, letra from sesion where id = 1;"
            #cur.execute(query)
            #con.commit()
         

    
    

    def iniciar(self, button):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        
        #Actualiza widthemisor
        con = psycopg2.connect(DSN)
        cur = con.cursor()
        query_widthemisor = "update sesion set widthemisor = "+ str(screensize[0]) +" where id = 1;"
        cur.execute(query_widthemisor)
        con.commit()
        #cur.close()
        #Actualiza heigthemisor
        #con = psycopg2.connect(DSN)
        #cur = con.cursor()
        query_heigthemisor = "update sesion set heigthemisor = "+ str(screensize[1]) +" where id = 1;"
        cur.execute(query_heigthemisor)
        con.commit()
        cur.close()
        
        print "Iniciando foto"
        t = threading.Thread(target=self.foto)
        threads.append(t)
        t.start()
        
        print "Iniciando XY"
        t_posxy = threading.Thread(target=self.posxy)
        threads.append(t_posxy)
        t_posxy.start()
        
        print "hooking mouse"
        t_clicks = threading.Thread(target=self.clicks)
        threads.append(t_clicks)
        t_clicks.start()
        
        print "hooking teclado"
        t_letra = threading.Thread(target=self.letra)
        threads.append(t_letra)
        t_letra.start()
        

    def detener(self, button):
        # move the button
        a = 1
        self.layout.move(button, random.randint(0,500),
                         random.randint(0,500))

    def __init__(self):
        # create the top level window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Servidor de Imagenes")
        window.set_default_size(300, 300)
        window.connect("delete-event", self.WindowDeleteEvent)
        window.connect("destroy", self.WindowDestroy)
        # create the table and pack into the window
        table = gtk.Table(2, 2, False)
        window.add(table)
        # create the layout widget and pack into the table
        self.layout = gtk.Layout(None, None)
        self.layout.set_size(299, 299)
        table.attach(self.layout, 0, 1, 0, 1, gtk.FILL|gtk.EXPAND,
                     gtk.FILL|gtk.EXPAND, 0, 0)
        # create the scrollbars and pack into the table
        #vScrollbar = gtk.VScrollbar(None)
        #table.attach(vScrollbar, 1, 2, 0, 1, gtk.FILL|gtk.SHRINK,
        #             gtk.FILL|gtk.SHRINK, 0, 0)
        #hScrollbar = gtk.HScrollbar(None)
        #table.attach(hScrollbar, 0, 1, 1, 2, gtk.FILL|gtk.SHRINK,
        #             gtk.FILL|gtk.SHRINK, 0, 0)	
        # tell the scrollbars to use the layout widget's adjustments
        #vAdjust = self.layout.get_vadjustment()
        #vScrollbar.set_adjustment(vAdjust)
        #hAdjust = self.layout.get_hadjustment()
        #hScrollbar.set_adjustment(hAdjust)
        # create 3 buttons and put them into the layout widget
        button1 = gtk.Button("Iniciar")
        button1.connect("clicked", self.iniciar)
        self.layout.put(button1, 0, 0)
        button2 = gtk.Button("Detener")
        button2.connect("clicked", self.ButtonClicked)
        self.layout.put(button2, 100, 0)
        button3 = gtk.Button("Inactivo")
        button3.connect("clicked", self.ButtonClicked)
        self.layout.put(button3, 200, 0)
        # show all the widgets
        window.show_all()

def main():
    # enter the main loop
    gtk.main()
    return 0

if __name__ == "__main__":
    LayoutExample()
    main()

