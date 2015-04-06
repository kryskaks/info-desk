# -*- coding: utf8 -*-
import peewee
from peewee import Model, CharField, DateTimeField, ForeignKeyField, Field, PostgresqlDatabase
from config import DATABASE_URL
from playhouse.db_url import connect
from passlib.hash import pbkdf2_sha256
from datetime import datetime

db = connect(DATABASE_URL)
PostgresqlDatabase.register_fields({'password_hash': 'password_hash'})

class _Model(Model):
	class Meta:
		database = db

	def __repr__(self):
		data = ", ".join(["%s: %s" % (key, unicode(value).encode('utf8') if value else None) for key, value in self._data.items()])
		return "{class_name}: {{ {data} }}".format(class_name = self.__class__.__name__, data = data)

	@classmethod
	def get_by_id(cls, id):
		return cls.get(cls.id == id)

	@classmethod
	def get_by_name(cls, name):
		return cls.get(cls.name == name)		

class Merchant(_Model):
	w1_checkout_id = CharField()
	name = CharField()
	contacts = CharField()
	#w1_client_id = CharField()

	class Meta:
		db_table = "merchants"

class PasswordField(CharField):
	db_field = 'password_hash'

	def db_value(self, password):
		return pbkdf2_sha256.encrypt(password, rounds = 200000, salt_size = 16)

	def python_value(self, value):
		return str(value)


class User(_Model):
	email = CharField(index = True, unique = True)
	password_hash = PasswordField()
	name = CharField(unique = True)
	created = DateTimeField(default = datetime.now())
	last_logged_in = DateTimeField(null = True)
	merchant = ForeignKeyField(Merchant, null = True)
	role = CharField()
	access_list = CharField(null = True)

	class Meta:
		db_table = "users"

	def save_password(self, password):
		self.password_hash = pbkdf2_sha256.encrypt(password, rounds = 200000, salt_size = 16)
		self.save()		
	
	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.password_hash)

create_tables_list = [Merchant, User]
drop_tables_list = [User, Merchant]

def create_tables():
	try:
		db.connect()
		db.create_tables(create_tables_list, True)
	except Exception, ex:
		print ex
		db.rollback()

def drop_tables():
	try:
		db.connect()
		map(lambda l: db.drop_table(l, True), drop_tables_list)
	except Exception, ex:
		print ex
		db.rollback()

def init_db():		
	try:
		drop_tables()
		create_tables()
		padmin = User.create(email = 'krementar@w1.ua', password = '123', name = 'padmin', role = 'projectAdmin')
	except Exception, ex:
		print ex
		db.rollback()