from django.forms import ModelForm
from .models import Torrent

class AddForm(ModelForm):
    class Meta:
        model = Torrent
        exclude = ('user', 'added',)
        
class EditForm(ModelForm):
    class Meta:
        model = Torrent
        exclude = ('user', 'added', 'magnet_link',)
