
from south.db import db
from django.db import models
from d51.django.auth.facebook.models import *

class Migration:
    
    def forwards(self, orm):
        db.rename_column('facebook_facebookid', 'id', 'uid')
        db.alter_column('facebook_facebookid', 'uid', models.PositiveIntegerField(primary_key=True))
        
    def backwards(self, orm):
        db.rename_column('facebook_facebookid', 'uid', 'id')
        db.add_column('facebook_facebookid', 'id', models.AutoField(primary_key=True))
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'facebook.facebookid': {
            'uid': ('models.PositiveIntegerField', [], {'primary_key': 'True'}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {'related_name': '"facebook"'})
        }
    }
    
    complete_apps = ['facebook']
