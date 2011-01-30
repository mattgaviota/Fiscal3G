#!/usr/bin/env python
#-*- coding: utf-8 -*-

#imports
import os
import csv
from tempfile import mkstemp

OUTBOX = os.path.abspath("outbox")

class Contact():
    
    def __init__(self, name, number, aspects = None, selected = None):
        self.name = name
        self.number = number
        self.aspects = aspects or []
        self.selected = selected or []
        
    def get_data(self):
        if self.selected:
            return [self.name, self.number, self.aspects, 'x']
        else:
            return [self.name, self.number, self.aspects, ' ']
    
    def select(self):
        self.selected.append(1)
    
    def unselect(self):
        try:
            self.selected.pop()
        except:
            pass
        return True
    
    def add_aspects(self, aspect):
        self.aspects.append(aspect)
        self.aspects = list(set(self.aspects))
        return True
        
    def clear_selection(self):
        self.selected = []
        return True
        
    def is_selected(self):
        if self.selected:
            return True
        else:
            return False
    
    def remove_aspect(self, aspect):
        return self.aspects.remove(aspect)
    
class Phonebook():
    
    def __init__(self):
        self.listofcontacts = []
        self.aspects = {}
    
    def add_contact(self, contact):
        self.listofcontacts.append(contact)
        return True
    
    def get_list_of_contacts(self):
        return self.listofcontacts
    
    def remove_contact(self, index):
        self.listofcontacts.pop(index)
        return True
    
    def search_contact(self, key):
        for index, contact in enumerate(self.listofcontacts):
            if key in contact.get_data():
                return index
    
    def select_contact(self, index):
        self.listofcontacts[index].select()
        return True
        
    def unselect_contact(self, index):
        self.listofcontacts[index].unselect()
        return True
        
    def select_all(self):
        for contact in self.listofcontacts:
            contact.select()
        return True
    
    def unselect_all(self):
        for contact in self.listofcontacts:
            contact.clear_selection()
        return True
    
    def show_contact(self, index):
        values = self.listofcontacts[index].get_data()
        print 'Contacto N°: %s' %(index)
        print '''
            Nombre       :  %s
            Número       :  %s
            Aspectos     :  %s
            Seleccionado : [%s]
            ''' %(values[0], values[1], values[2], values[3])
        print
        return True
    
    def show_all(self):
        for index,contact in enumerate(self.listofcontacts):
            self.show_contact(index)
        return True
    
    def choose_aspects(self):
        for key, value in sorted(self.aspects.iteritems()):
            print '%s : %s' %(key, value)
        options = raw_input('Añadir contacto a uno o mas números de Aspectos : ')
        chosedaspects = []
        for option in options:
            try:
                chosedaspects.append(self.aspects[option])
            except KeyError:
                pass
        return chosedaspects
    
    def select_by_aspect(self, aspect = None, band = True):
        if band:
            for key, value in sorted(self.aspects.iteritems()):
                print '%s : %s' %(key, value)
            options = raw_input('Seleccionar uno o mas números de Aspectos : ')
            for option in options:
                print option
                try:
                    for index, contact in enumerate(self.listofcontacts):
                        if self.aspects[option] in contact.get_data()[2]:
                            self.select_contact(index)
                except KeyError:
                    pass
        else:
            for index, contact in enumerate(self.listofcontacts):
                        if aspect in contact.get_data()[2]:
                            self.select_contact(index)
        return True
    
    def add_contact_to_aspect(self):
        option = raw_input('ingrese número de contacto, de telefono o nombre: ')
        try:
            try:
                self.show_contact(int(option))
                index = int(option)
            except (IndexError, ValueError):
                try:
                    self.show_contact(self.search_contact(option))
                    index = self.search_contact(option)
                except (IndexError, ValueError):
                    print 'opcion incorrecta'
                    
            for key, value in sorted(self.aspects.iteritems()):
                print '%s : %s' %(key, value)
            keys = raw_input('Seleccionar uno o mas números de Aspectos : ')
            for key in keys:
                self.listofcontacts[index].add_aspects(self.aspects[key])
        except (KeyError, ValueError):
            print 'Opcion incorrecta'
        return True
    
    def remove_contact_from_aspect(self):
        option = raw_input('ingrese número de contacto, de telefono o nombre: ')
        try:
            try:
                self.show_contact(int(option))
                index = int(option)
            except (IndexError, ValueError):
                try:
                    self.show_contact(self.search_contact(option))
                    index = self.search_contact(option)
                except (IndexError, ValueError):
                    print 'opcion incorrecta'
                    
            for key, value in enumerate(self.listofcontacts[index].aspects):
                print '%s : %s' %(key, value)
            keys = raw_input('Seleccionar uno o mas números de Aspectos : ')
            for key in keys:
                self.listofcontacts[index].remove_aspect(self.listofcontacts[index].aspects[int(key)])
        except (IndexError, KeyError):
            print 'Opcion incorrecta'
        return True
            
    def unselect_by_aspect(self):
        for key, value in sorted(self.aspects.iteritems()):
            print '%s : %s' %(key, value)
        options = raw_input('Seleccionar uno o mas números de Aspectos : ')
        for option in options:
            try:
                for contact in self.listofcontacts:
                    if self.aspects[option] in contact.get_data()[2]:
                        contact.unselect()
            except KeyError:
                pass
        return True
    
    def show_aspects(self):
        for key, value in sorted(self.aspects.iteritems()):
            print '%s : %s' %(key, value)
        return True
    
    def add_aspect(self):
        nameaspect = raw_input('Nombre del nuevo Aspecto: ')
        try:
            keys = self.aspects.keys()
            newkey = str(int(sorted(keys).pop()) + 1)
        except IndexError:
            newkey = '1'
        self.aspects[newkey] = nameaspect
        return True
    
    def remove_aspects(self):
        for key, value in sorted(self.aspects.iteritems()):
            print '%s : %s' %(key, value)
        options = raw_input('Seleccionar uno o mas números de Aspectos : ')
        for option in options:
            try:
                for contact in self.listofcontacts:
                    if self.aspects[option] in contact.get_data()[2]:
                        contact.remove_aspect(self.aspects[option])
                del self.aspects[option]
            except KeyError:
                pass
        return True
    
    def load_aspects_from_csv(self):
        file = open('./aspects.csv', 'rb')
        aspects = csv.reader(file, delimiter= ',', quotechar= '|')
        for row in aspects:
            self.aspects[row[0]] = row[1]
        return True 
    
    def load_contacts_from_csv(self):
        file  = open('./contacts.csv', 'rb')
        contacts = csv.reader(file, delimiter= ',', quotechar= '|')
        for row in contacts:
            name, number, aspects = tuple(row)
            contact = Contact(name, number, eval(aspects))
            self.add_contact(contact)
        return True
    
    def write_contacts_to_csv(self):
        file = open('./contacts.csv', 'a')
        contactwriter = csv.writer(file, delimiter= ',', quotechar= '|', 
                        quoting= csv.QUOTE_ALL)
        for contact in self.listofcontacts:
            contactwriter.writerow(contact.get_data()[:-1])
        file.close()
        return True
    
    def write_aspects_to_csv(self):
        file = open('./aspects.csv', 'a')
        contactwriter = csv.writer(file, delimiter= ',', quotechar= '|', 
                        quoting= csv.QUOTE_ALL)
        for key, value in self.aspects.iteritems():
            contactwriter.writerow([key, value])
        file.close()
        return True
    
    def write_sms_to_folder(self, telefonos, mensaje):
        reports = []
        for telefono in telefonos:
            report = (
                "%s\n"
                "%s\n"
                % (telefono, mensaje)
                )
            reports.append(report)
        
        for report in reports:
            temp_fd, tempfile = mkstemp(".send", "",OUTBOX)
            with os.fdopen(temp_fd, 'w') as file:
                file.write(report)
    
    def select_phone_to_send(self, aspect):
        telefonos = []
        for contact in self.listofcontacts:
            if contact.is_selected():
                if aspect in contact.get_data()[2]:
                    telefonos.append(contact.get_data()[1])
        return telefonos
    
    def write_sms_to_send(self, band = True):
        if band:
            print 'Aspectos'
            for key, value in sorted(self.aspects.iteritems()):
                print '%s : %s' %(key, value)
            options = raw_input('Seleccionar uno o mas números de Aspectos : ')
            try:
                for option in options:
                    aspect = self.aspects[option]
                    self.select_by_aspect(aspect, False)
                    telefonos = self.select_phone_to_send(aspect)
            except KeyError:
                    print 'Aspecto inexistente'
        else:
            option = raw_input('ingrese número de contacto, de telefono o nombre: ')
            try:
                contact = self.listofcontacts[int(option)]
                telefonos = [contact.get_data()[1]]
            except (IndexError, ValueError):
                try:
                    contact = self.listofcontacts[self.search_contact(option)]
                    telefonos = [contact.get_data()[1]]
                except (IndexError, ValueError):
                    print 'Contacto inexistente'
        
        mensaje = raw_input('Escriba mensaje a enviar: ')
        self.write_sms_to_folder(telefonos, mensaje)                
        return 0
        
    def write_sms_from_number(self):
            numero = raw_input('Ingrese el número de telefono: ')
            mensaje = raw_input('Escriba mensaje a enviar: ')
            self.write_sms_to_folder([numero], mensaje)
            return 0
        
        
#main modules

def menu():
    print u"""
        Contactos                           Aspectos
        [1]   Agregar Contacto             [5]  Agregar Aspecto 
        [2]   Mostrar Contacto             [6]  Mostrar Aspectos
        [3]   Eliminar Contacto            [7]  Quitar Aspecto/s
        [4]   Mostrar Todos                [8]  Agregar contacto a Aspecto
                                           [9]  Quitar contacto de Aspecto
        
        Selección                           Cargar 
        [10]  Seleccionar Contacto         [16] Aspectos
        [11]  Deseleccionar Contacto       [17] Contactos
        [12]  Seleccionar Todos            
        [13]  Seleccionar Ninguno           Salvar
        [14]  Seleccionar por Aspecto/s    [18] Aspectos     
        [15]  Deseleccionar por Aspecto/s  [19] Contactos
        
        Enviar Mensaje a
        [20] Aspectos
        [21] Contacto
        [22] Número
        
        """
    return True

def send_sms_to_number(phonebook):
    phonebook.write_sms_from_number()

def send_sms_to_contact(phonebook):
    phonebook.write_sms_to_send(False)

def send_sms_to_aspects(phonebook):
    phonebook.write_sms_to_send()
    return True

def show_aspects_from_phonebook(phonebook):
    return phonebook.show_aspects()

def add_aspect_to_phonebook(phonebook):
    return phonebook.add_aspect()

def remove_aspect_from_phonebook(phonebook):
    return phonebook.remove_aspects()

def add_contact_from_phonebook_to_aspect(phonebook):
    phonebook.add_contact_to_aspect()

def remove_contact_from_phonebook_from_aspect(phonebook):
    phonebook.remove_contact_from_aspect()

def select_by_aspect_in_phonebook(phonebook):
    return phonebook.select_by_aspect()

def unselect_by_aspect_in_phonebook(phonebook):
    return phonebook.unselect_by_aspect()

def load_contacts_from_csv_to_phonebook(phonebook):
    return phonebook.load_contacts_from_csv()

def load_aspects_from_csv_to_phonebook(phonebook):
    return phonebook.load_aspects_from_csv()

def write_aspects_to_phonebook_to_csv(phonebook):
    return phonebook.write_aspects_to_csv()

def write_contacts_to_phonebook_to_csv(phonebook):
    return phonebook.write_contacts_to_csv()

def add_contact_to_phonebook(phonebook):
    name = raw_input('Ingrese el nombre: ')
    number = raw_input('Ingrese el número: ')
    aspects = self.choose_aspects()
    contact = Contact(name, number, aspects)
    phonebook.add_contact(contact)
    return True

def show_contact_from_phonebook(phonebook):
    option = raw_input('ingrese número de contacto, de telefono o nombre: ')
    try:
        phonebook.show_contact(int(option))
    except (ValueError, IndexError):
        try:
            phonebook.show_contact(phonebook.search_contact(option))
        except (ValueError, IndexError):
            print 'No existe el contacto'
    return True

def remove_contact_from_phonebook(phonebook):
    option = raw_input('ingrese número de contacto, de telefono o nombre: ')
    try:
        phonebook.remove_contact(int(option))
    except:
        try:
            phonebook.remove_contact(phonebook.search_contact(option))
        except:
            print 'No existe el contacto'
    return True

def show_all_in_phonebook(phonebook):
    return phonebook.show_all()

def select_contact_from_phonebook(phonebook):
    contactnumber = raw_input('Ingrese número de contacto a seleccionar: ')
    try:
        phonebook.select_contact(int(contactnumber))
    except:
        print 'contacto no existe'
    return True

def unselect_contact_from_phonebook(phonebook):
    contactnumber = raw_input('Ingrese número de contacto a deseleccionar: ')
    try:
        phonebook.unselect_contact(int(contactnumber))
    except:
        print 'contacto no existe'
    return True

def select_all_contacts_from_phonebook(phonebook):
    return phonebook.select_all()

def unselect_all_contacts_from_phonebook(phonebook):
    return phonebook.unselect_all()


FUNCTION = {
            '1' : add_contact_to_phonebook,
            '2' : show_contact_from_phonebook,
            '3' : remove_contact_from_phonebook,
            '4' : show_all_in_phonebook,
            '5' : add_aspect_to_phonebook,
            '6' : show_aspects_from_phonebook,
            '7' : remove_aspect_from_phonebook,
            '8' : add_contact_from_phonebook_to_aspect,
            '9' : remove_contact_from_phonebook_from_aspect,
            '10': select_contact_from_phonebook,
            '11': unselect_contact_from_phonebook,
            '12': select_all_contacts_from_phonebook,
            '13': unselect_all_contacts_from_phonebook,
            '14': select_by_aspect_in_phonebook,
            '15': unselect_by_aspect_in_phonebook,
            '16': load_aspects_from_csv_to_phonebook,
            '17': load_contacts_from_csv_to_phonebook,
            '18': write_aspects_to_phonebook_to_csv,
            '19': write_contacts_to_phonebook_to_csv,
            '20': send_sms_to_aspects,
            '21': send_sms_to_contact,
            '22': send_sms_to_number
            }
    
def main():
    phonebook = Phonebook()
    load_contacts_from_csv_to_phonebook(phonebook)
    load_aspects_from_csv_to_phonebook(phonebook)
    os.system('clear')
    menu()
    option = raw_input('Ingrese opción: ')
    while ((option) != 'salir'):
        try:
            #os.system('clear')
            FUNCTION[option](phonebook)
        except KeyError:
            print 'Opción fuera de rango'
    
        menu()
        option = raw_input('Ingrese opcion: ')
        

if __name__ == '__main__':
    main()
