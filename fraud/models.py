from enum import unique
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_migrate,pre_migrate
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import fraud
from fraud.apps import FraudConfig
# Create your models here.

data_type=[('ip','ip'),('name','name'),('email','email'),('phone','phone'),('card_num','card_num')]
condition_type=[
    ('amount','amount'),
    
    ('VPN','VPN'),
    
    ('num refuse transaction with card number today','num refuse transaction with card number today'),
    ('num refuse transaction with email today','num refuse transaction with email today'),
    ('num refuse transaction with phone today','num refuse transaction with phone today'),
    ('num refuse transaction with name today','num refuse transaction with name today'),
    ('num refuse transaction with ip today','num refuse transaction with ip today'),
    
    ('num transaction with card number today','num transaction with card number today'),
    ('num transaction with email today','num transaction with email today'),
    ('num transaction with phone today','num transaction with phone today'),
    ('num transaction with name today','num transaction with name today'),
    ('num transaction with ip today','num transaction with ip today'),
    
    ('num refuse transaction with card number month','num refuse transaction with card number month'),
    ('num refuse transaction with email month','num refuse transaction with email month'),
    ('num refuse transaction with phone month','num refuse transaction with phone month'),
    ('num refuse transaction with name month','num refuse transaction with name month'),
    ('num refuse transaction with ip month','num refuse transaction with ip month'),
    
    ('num transaction with card number month','num transaction with card number month'),
    ('num transaction with email month','num transaction with email month'),
    ('num transaction with phone month','num transaction with phone month'),
    ('num transaction with name month','num transaction with name month'),
    ('num transaction with ip month','num transaction with ip month'),
    
            ]
compare_type=[('more than','more than'),('less than','less than'),
              ('equal','equal'),('more than or equal','more than or equal'),
              ('less than or equal','less than or equal')]

class BaseTransaction(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.CharField(max_length=30)
    card_num=models.CharField(max_length=30)
    ip=models.CharField(max_length=30)
    merchant=models.CharField(max_length=100,blank=True,null=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    currency=models.CharField(max_length=3,blank=True,null=True)
    description=models.CharField(max_length=255,blank=True,null=True)
    transaction_status=models.BooleanField(default=False)
    third_secure=models.BooleanField(default=False)
    message = models.TextField(blank=True,null=True)
    rule=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-created_at']
class Transaction(BaseTransaction):
    class Meta:
        db_table='transaction'
    def __str__(self):
        return self.name 
class Review(BaseTransaction):
    reviewed=models.BooleanField(default=False)
    reviewed_at=models.DateTimeField(blank=True,null=True)
    review_action=models.TextField(blank=True,null=True)
    class Meta:
        db_table='review'
    def __str__(self):
        return self.name 
class Action(models.Model):
    name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    active=models.BooleanField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table='action'
        ordering=['name']
    def __str__(self):
        return self.name
class BaseBlacklist(models.Model):
    type=models.CharField(max_length=255,choices=data_type,blank=True,null=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    card_num=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField(max_length=254,blank=True,null=True)
    phone=models.CharField(max_length=30,blank=True,null=True)
    ip=models.CharField(max_length=30,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['-created_at']
class Blacklist(BaseBlacklist):
    merchant=models.CharField(max_length=100,blank=True,null=True)
    class Meta:
        db_table='blacklist'
class GlobalBlacklist(BaseBlacklist):
    class Meta:
        db_table='global_blacklist'
class Whitelist(BaseBlacklist):
    merchant=models.CharField(max_length=100)
    class Meta:
        db_table='whitelist'
class GlobalWhitelist(BaseBlacklist):
    class Meta:
        db_table='global_whitelist'
class Rule(models.Model):
    condition=models.ManyToManyField('Condition',blank=False)
    name=models.CharField(max_length=255)
    active=models.BooleanField()
    priority=models.IntegerField()
    action= models.ManyToManyField(Action,blank=False)
    description=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table='rules'
    def __str__(self):
        return self.name
class Condition(models.Model):
    name=models.CharField(max_length=255)
    type=models.CharField(max_length=255,choices=condition_type,blank=True,null=True)
    compare_type=models.CharField(max_length=255,choices=compare_type,blank=True,null=True)
    value=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField(null=True,blank=True)
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='conditions'
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def createToken(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)


#defualte actions  
actions=[
    ["accept transaction","only accept transaction"],
    ["block transaction","block transaction only"],
    ["block client","block client name"],
    ["block phone","block client phone"],
    ["block card number","block client card number"],
    ["block email","block client email"],
    ["block ip","block client ip"],
    ["global block client","add client to global black list"],
    ["global block phone","add phone to global black list"],
    ["global block card number","add card number to global black list"],
    ["global block email","add email to global black list"],
    ["global block ip","add ip to global black list"],
    ["add to review","add transaction To review by risk team"],
        ]

def add_actions(**kwargs):
    for action in actions:
        if not Action.objects.filter(name=action[0]).exists():
            Action.objects.create(name=action[0],description=action[1],active=True)
    




#client (card num-email-phone- ip)
#mrchant (name-id)

# 1	amount more than 10000	1	amount	09:27:09.857613	10000	amount more than 10k	more than	2019-01-01 00:00:00	2019-01-01 00:00:00
# 2	amount less 10000	1	amount	10:21:01.329248	10000	if amount less than 10000 add to white list	less than	2019-01-01 00:00:00	2019-01-01 00:00:00