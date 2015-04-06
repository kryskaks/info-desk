# -*- coding: utf8 -*-
import peewee
from peewee import Model, CharField, DateTimeField, ForeignKeyField
from config import DATABASE_URL
from playhouse.db_url import connect
from passlib.hash import pbkdf2_sha256
from datetime import datetime

db = connect(DATABASE_URL)

class _Model(Model):
	class Meta:
		database = db

	def __repr__(self):
		data = ", ".join(["%s: %s" % (key, unicode(value).encode('utf8') if value else None) for key, value in self._data.items()])
		return "{class_name}: {{ {data} }}".format(class_name = self.__class__.__name__, data = data)

	@classmethod
	def get_by_id(cls, id):
		return cls.get(cls.id == id)

class Merchant(_Model):
	w1_checkout_id = CharField()
	name = CharField()
	contacts = CharField()
	w1_client_id = CharField()

	class Meta:
		db_table = "merchants"


class User(_Model):
	email = CharField(index = True, unique = True)
	password_hash = CharField()
	name = CharField()
	created = DateTimeField()
	last_logged_in = DateTimeField(null = True)
	merchant = ForeignKeyField(Merchant, null = True)
	role = CharField()

	class Meta:
		db_table = "users"

	@classmethod
	def new(cls, email, password, name, role, merchant = None):
		return User.create(
			email = email,
			password_hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16),
			name = name,
			created = datetime.now(),
			merchant = merchant,
			role = role)		

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

	except Exception, ex:
		print ex
		db.rollback()