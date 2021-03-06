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

def create_WikiData_Theme_Topic():
	"""
	creates GSystemType: WikiData(a member_of GAPP), GSystemType Theme and Topic(a member_of factory_settings) 
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

	
def create_Topic(name, user_id):
	"""
	Creates a topic if it does not exist
	"""
	
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
		topic.created_by = int(user_id)
		topic.member_of.append(topic_type_id)
		topic.save()
		print topic
		print "Created a topic -->" + name + "\n"
		
def create_AttributeType(name, data_type, system_name, user_id):
	"""
	This method creates an attribute type of given name and which will be for the given system_type(WikiData)
	The following data_types are possible:
	DATA_TYPE_CHOICES = (
    	"None",
    	"bool",
    	"basestring",
    	"unicode",
    	"int",
    	"float",
    	"long",
    	"datetime.datetime",
    	"list",
    	"dict",
    	"ObjectId",
    	"IS()"
	)
	User Id will be used for filling the created_by field.
	"""
	print "Creating an Attribute Type"
	cursor = collection.Node.find({"name":unicode(name)})
	if cursor.count() != 0:
		print "The AttributeType already exists."
	else:
		attribute_type = collection.AttributeType()
		attribute_type.name = unicode(name)
		attribute_type.data_type = data_type
		system_type = collection.Node.one({"name":u"WikiData"})
		attribute_type.subject_type.append(system_type._id)
		attribute_type.created_by = user_id
		attribute_type.modified_by = user_id
		factory_id = collection.Node.one({"name":u"factory_types"})._id
		attribute_type.member_of.append(factory_id)
		attribute_type.save()
		"""	
		Adding the attribute type to the WikiData GSytemType attribute_set"
		"""
		system_type.attribute_type_set.append(attribute_type._id)
		print "Created the Attribute_Type " + str(name)
		
		
def create_Attribute(name, subject_name, attribute_type_name, object_value):
	"""
	Creating an Attribute with specified name, subject_id, attribute_type and value.
	This will create an attribute iff the attribute is not present for the same subject
	"""
	print "Creating an attribute"
	subject = collection.Node.one({"name":unicode(subject_name)})
	attribute_type = collection.Node.one({"name": unicode(attribute_type_name), "_type": u"AttributeType"})
	print attribute_type
	cursor = collection.Node.find({"subject":subject._id, "attribute_type": attribute_type._id})
	if cursor.count()!= 0:
		print "The attribute " + str(attribute_type_name) + " already exists."
	else:
		att = collection.GAttribute()
		att.subject = subject._id
		#DBref = {"$ref":Node.collection_name, "$id":attribute_type._id, "$name": attribute_type.name}
		att.attribute_type = attribute_type
		att.object_value = unicode(object_value)
		print type(object_value), str("------------------------------------")
		print "Abt to create"
		att.save()
		print "Created attribute " + str(name)
	
	
def create_RelationType(name, inverse_name, object_type_name, user_id):
	"""	
	Creating a RelationType with the following parameters.
	1. name - inherits Node class.
	2. inverse_name  - This is the name of the inverse of the relation.
	3. subject_type - Which Systemtype is the relation defined under.
	4. object_type - which object is the relation type defined for?
	"""
        print "Creating a Relation Type"
        cursor = collection.Node.find({"name":unicode(name)})
        if cursor.count() != 0:
                print "The RelationType already exists."
        else:
                relation_type = collection.RelationType()
                relation_type.name = unicode(name)
                system_type = collection.Node.one({"name":u"WikiData"})
                relation_type.subject_type.append(system_type._id)
                relation_type.inverse_name = unicode(inverse_name)
		relation_type.created_by = user_id
                relation_type.modified_by = user_id
		object_type = collection.Node.one({"name":unicode(object_type_name)})
		relation_type.object_type.append(ObjectId(object_type._id))
                factory_id = collection.Node.one({"name":u"factory_types"})._id
                relation_type.member_of.append(factory_id)
                relation_type.save()
                """     
                Adding the attribute type to the WikiData GSytemType attribute_set"
                """
                system_type.relation_type_set.append(ObjectId(relation_type._id))
                print "Created the Relation_Type " + str(name)
 

def create_Relation(name, subject_name, relation_type_name, right_subject_name):
	"""
	Creates a GRelation with following parameters:
	1. Name: Given Name
	2. Subject: which GSytem class object
	3. Relation Type: The type of relation
	4. Right Subject: The subject on the right. The object related to the current object.
	"""
	print "Creating a Relation."
	cursor = collection.Node.find({"name":unicode(subject_name), "_type":u"GRelation"})
	if cursor.count()!=0:
		print "The Relation Already exists"
	else:
		relation = collection.GRelation()
		#relation.created_by = user_id
		#relation.modified_by = user_id
		#relation.name = unicode(name)
		left_system = collection.Node.one({"name":unicode(subject_name)})
		relation.subject = ObjectId(left_system._id)
		relation_type = collection.Node.one({"name":unicode(relation_type_name), "_type":u"RelationType"})
		relation.relation_type = relation_type
		right_system = collection.Node.one({"name":unicode(right_subject_name)})
		relation.right_subject = ObjectId(right_system._id)
		relation.save()
		print "Created a Relation " + str(name)




def display_objects():
	cursor = collection.Node.find()
	for a in cursor:
		print a.name
		

class Command(BaseCommand):
	def handle(self, *args, **options):
		create_WikiData_Theme_Topic()
		create_Topic(u"topic1", user_id)
		create_Topic(u"topic2", user_id)
		create_Topic(u"topic3", user_id)
		create_Topic(u"topic4", user_id)
		create_AttributeType("wiki_attr2", "unicode", "WikiData", user_id)
		create_Attribute("attr1", "topic1", "wiki_attr2", "This is the value of the wiki_attr1 field")
		create_RelationType("same_theme1", "same_theme1", "topic1", user_id) 
		create_Relation("theme1", "topic1", "same_theme1", "topic2")
		print "All objects\n"
                display_objects()







