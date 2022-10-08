#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
#import add actions function from fraud app models file
#from fraud.models import Action
#run method add action in fraud app models.py   
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

def add_actions():
    for action in actions:
        if not Action.objects.filter(name=action[0]).exists():
            Action.objects.create(name=action[0],description=action[1],active=True)




def main():
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paymob.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
