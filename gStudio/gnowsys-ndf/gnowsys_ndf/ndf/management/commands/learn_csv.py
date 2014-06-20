''' imports from installed packages '''
from django.core.management.base import BaseCommand, CommandError

from mongokit import IS

from django_mongokit import get_database

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

''' imports from application folders/files '''
from gnowsys_ndf.ndf.models import Node, GSystemType
from gnowsys_ndf.ndf.models import Group
from gnowsys_ndf.ndf.models import DATA_TYPE_CHOICES, QUIZ_TYPE_CHOICES_TU
from gnowsys_ndf.settings import GAPPS
from gnowsys_ndf.settings import META_TYPE
from gnowsys_ndf.factory_type import factory_gsystem_types, factory_attribute_types, factory_relation_types

from mongokit import Collection
from gnowsys_ndf.ndf.models import *
db = get_database()
collection = get_database()[GSystem.collection_name]
import csv



class Command(BaseCommand):
	def handle(self, *args, **options):
			
		with open('/home/aditya/Desktop/data.csv','rb') as f:
			r = csv.reader(f,delimiter ='	')
			for row in r:
				for a in row:
					print (a)

		
		'''
	tutFile = open("/home/aditya/Desktop/data.csv","rb")
	reader = csv.reader(tutFile)

	rownum=0
	for row in reader:
		if rownum==0:
			header=row
		else:
			colnum=0
			for col in row:
				print'%-8s: %s' % (header[colnum],col)
				colnum+=1
		
		rownum+=1

	tutFile.close()
	'''
