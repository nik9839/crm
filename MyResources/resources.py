import uuid

from MyResources.fetchCalenderData import register_resource
from MyResources.models import  Resources



def insertResource(self,resourceObject):

    if resourceObject.get('capacity')==None:
        resourceObject['capacity']=0

    if resourceObject.get('buildingId')==None:
        resourceObject['buildingId']='---'
        resourceObject['floorName'] = 0

    resource = Resources(resourceEmail=resourceObject['resourceEmail'],resourceId=resourceObject['resourceId'],
                         generatedResourceName=resourceObject['generatedResourceName'],resourceType=resourceObject['resourceType'],
                         capacity=resourceObject['capacity'],resourceCategory=resourceObject['resourceCategory'],
                         buildingId=resourceObject['buildingId'],floorName=resourceObject['floorName'], resourceDumpdata=resourceObject,
                         resourceUUID= uuid.uuid4())
    resource.save()

    register_resource(resourceObject['resourceEmail'])


def insert_multiple_resources(self,resourcesObject):
    for resource in resourcesObject:
        insertResource(self,resource)