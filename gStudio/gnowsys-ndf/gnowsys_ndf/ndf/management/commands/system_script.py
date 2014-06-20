''' imports from installed packages '''
from django.core.management.base import BaseCommand, CommandError


#from mongokit import IS
from gnowsys_ndf.ndf.models import *
from django_mongokit import get_database

#defining global variables
database = get_database()
collection = database[Node.collection_name]
user_id = 1
"""
try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

'''imports from application folders/files '''
"""

from gnowsys_ndf.ndf.models import *
from gnowsys_ndf.settings import GAPPS
from gnowsys_ndf.settings import META_TYPE
from gnowsys_ndf.factory_type import factory_gsystem_types, factory_attribute_types, factory_relation_types

####################################################################################################################
#global variables
#db = get_database()
#collection = db[Node.collection_name]



#for taking input json file
import json
import sys

def create_GSystemType():
	"""
	GSystemType WikiData
	"""
	cursor = collection.Node.find({"_type":u"GSystemType", "name":u"WikiData"})
	if (cursor.count() != 0):
		print "Wikidata already exists"
		wiki_id = cursor[0]._id
	else:
		GAPP = collection.Node.one({"name": u"GAPP"})
		GAPP_id = GAPP._id
		wiki = collection.GSystemType()
		wiki.name = u"WikiData"
		wiki.created_by = int(user_id)
		wiki.member_of.append = GAPP_id
		wiki.save()
		wiki_id = wiki._id
		print "Created a GSystemType for----> WikiData \n"
	
	cursor = collection.Node.find({"_type": u"GSystemType", "name": u"Theme"})
	if (cursor.count() != 0):
		print "theme already exists"
		
	else:
		factory = collection.Node.one({"name": u"factory_types"})
		factory_id = factory._id
		obj = collection.GSystemType()
		obj.name = u"Theme"
		obj.created_by = int(1)
		obj.type_of.append(wiki_id)
		obj.member_of.append(factory_id)
		obj.save()
		print "Created an object of GSystem Type --> Theme \n"
	
	cursor = collection.Node.find({"_type":u"GSystemType", "name": u"Topic"})
	if(cursor.count() != 0):
		print "Topic already exists"
	else:	
		factory = collection.Node.one({"name": u"factory_types"})
                factory_id = factory._id
		obj1 = collection.GSystemType()
		obj1.name = u"Topic"
		obj1.created_by = int(1)
		obj1.type_of.append(wiki_id)
		obj1.member_of.append(factory_id)
		obj1.save()
		print "Created an object of GSystemtype"

	
def create_Topic(name):
	print "Creating a GSystem Topic"
	cursor = collection.Node.find({"name": u"Topic"})
	topic_type = cursor[0]
	print topic_type
	cursor2 = collection.Node.find({"name": name, "_type": u"GSystem"})
	print cursor2.count()
	if (cursor2.count() != 0):
		print "Topic already exists"
		return
	else:
		topic_type_id = topic_type._id
		topic = collection.GSystem()
		topic.name = name
		topic.created_by = int(1)
		topic.member_of.append(topic_type_id)
		topic.save()
		print topic
		print "Created a topic -->" + name + "\n"
		

def display_objects():
	cursor = collection.Node.find()
	for a in cursor:
		print a.name
		

class Command(BaseCommand):
	def handle(self, *args, **options):
		print "Inside the Handle method now \n. Calling hello\n"
		create_GSystemType()
		create_Topic(u"topic1")
		create_Topic(u"topic2")
		create_Topic(u"topic3")
		print "All objects\n"
		display_objects()






