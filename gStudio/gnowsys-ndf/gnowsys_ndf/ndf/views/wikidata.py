from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from gnowsys_ndf.ndf.models import *
from django_mongokit import get_database
from django.template import RequestContext

database = get_database()
collection = database[Node.collection_name]

def index(request, group_id):
	ins_objectid  = ObjectId()
    	if ins_objectid.is_valid(group_id) is False :
        	group_ins = collection.Node.find_one({'_type': "Group","name": group_id})
        	auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
      	if group_ins:
       		group_id = str(group_ins._id)
      	else :
        	auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
        if auth :
         	group_id = str(auth._id)
    	else :
        	pass

	topic_coll = collection.Node.find({"_type": u"GSystem"})
	print "here: " + str(topic_coll)	
	context = RequestContext(request, {'title': "WikiData Topics", 'topic_coll': topic_coll})
	template = "ndf/wikidata.html"
     	variable = RequestContext(request,{'title': "WikiData Topics"})
	context_variables = {'title': "WikiData Topics"}
	context_instance = RequestContext(request, {'title': "WikiData Topics", 'groupid':group_id, 'group_id':group_id})
      	return render(request, template, {'title': "WikiData Topics", 'topic_coll': topic_coll, 'groupid':group_id, 'group_id':group_id})


