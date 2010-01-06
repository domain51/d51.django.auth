
from south.db import db
from django.db import models
from d51.django.auth.facebook.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'FacebookID'
        db.create_table('facebook_facebookid', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.OneToOneField(orm['auth.User'], related_name="facebook")),
        ))
        db.send_create_signal('facebook', ['FacebookID'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'FacebookID'
        db.delete_table('facebook_facebookid')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'facebook.facebookid': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {'related_name': '"facebook"'})
        }
    }
    
    complete_apps = ['facebook']
