
from south.db import db
from django.db import models
from d51.django.auth.twitter.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TwitterToken'
        db.create_table('twitter_twittertoken', (
            ('uid', models.PositiveIntegerField(primary_key=True)),
            ('user', models.OneToOneField(orm['auth.User'], related_name='twitter')),
            ('key', models.CharField(max_length=100)),
            ('secret', models.CharField(max_length=100)),
        ))
        db.send_create_signal('twitter', ['TwitterToken'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TwitterToken'
        db.delete_table('twitter_twittertoken')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'twitter.twittertoken': {
            'key': ('models.CharField', [], {'max_length': '100'}),
            'secret': ('models.CharField', [], {'max_length': '100'}),
            'uid': ('models.PositiveIntegerField', [], {'primary_key': 'True'}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {'related_name': "'twitter'"})
        }
    }
    
    complete_apps = ['twitter']
