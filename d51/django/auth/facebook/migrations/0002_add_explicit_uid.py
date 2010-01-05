
from south.db import db
from django.db import models
from d51.django.auth.facebook.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'FacebookID.uid'
        db.add_column('facebook_facebookid', 'uid', models.PositiveIntegerField(primary_key=True))
        
        # Deleting field 'FacebookID.id'
        db.delete_column('facebook_facebookid', 'id')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'FacebookID.uid'
        db.delete_column('facebook_facebookid', 'uid')
        
        # Adding field 'FacebookID.id'
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
