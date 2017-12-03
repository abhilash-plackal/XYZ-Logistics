from tastypie import fields, utils
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication, BasicAuthentication
from fund_transfer_app.models import *
from django.contrib.auth.models import User, Group
from django.utils import timezone
import datetime
from decimal import *
from django.utils.html import escape

class UserResource(ModelResource):
    class Meta:
        list_allowed_methods = ['get']
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True

class NodeResource(ModelResource):
    manager = fields.ForeignKey( UserResource, 'manager', full=True)
    parent = models.ForeignKey( 'self', 'parent')

    class Meta:
        queryset = Node.objects.all()
        resource_name = 'node'
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True

class TransactionResource(ModelResource):
    actor = fields.ForeignKey( UserResource, 'actor', full=True)
    node = fields.ForeignKey( NodeResource, 'node')
    
    class Meta:
        queryset = Transaction.objects.all()
        resource_name = 'transaction'
        allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        user = bundle.request.user if bundle.request else None

        if (Group.objects.get(name='root_users').user_set.filter(id=user.id).exists()):
            from_list = Node.objects.filter(name__exact=bundle.data['from'])
            to_list = Node.objects.filter(name__exact=bundle.data['to'])

            to_obj = None
            from_obj = None
            amount = Decimal(bundle.data['amount'])

            if from_list.count() != 0:
                from_obj = from_list[0]

            if to_list.count() != 0:
                to_obj = to_list[0]

            if from_obj.balance < amount:
                print('Insufficient fund!!')
                return bundle

            if (from_obj == None) or (to_obj == None):
                return bundle 

            if (from_obj.name == 'Root') and (from_obj.name == to_obj.parent.name):
                bundle.data['node'] = from_obj
                bundle.data['transaction_type'] = 'DEBIT'
            elif (to_obj.name == 'Root') and (to_obj.name == from_obj.parent.name):
                bundle.data['node'] = to_obj
                bundle.data['transaction_type'] = 'CREDIT'
            elif (to_obj.name == from_obj.parent.name) or (from_obj.name == to_obj.parent.name):
                bundle.data['node'] = from_obj
                bundle.data['transaction_type'] = 'CREDIT' if (from_obj.name == to_obj.parent.name) else 'DEBIT'
            else:
                print('Fund cant be transfered from `' + from_obj.name + '` to `' + to_obj.name 
                                            + "` since they don't have a parent child relationship")
                return bundle


            to_obj.balance = to_obj.balance + amount
            to_obj.save()

            from_obj.balance = from_obj.balance - amount
            from_obj.save()

            bundle.data['amount'] = amount

            str_date = str(datetime.datetime.now())
            bundle.data['transaction_date'] = str_date
            
            bundle.data['actor'] = user

            bundle.data.pop('from', None)
            bundle.data.pop('to', None)

            return super(TransactionResource, self).obj_create(bundle, **kwargs)   

        return bundle 

