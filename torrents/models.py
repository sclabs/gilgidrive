import binascii, urllib, re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

def magnet_validator(value):
    if not 'tr=udp%3a%2f%2ftracker.gilgi.org%3a6969%2fannounce' in value:
        raise ValidationError(u'torrent must use tracker.gilgi.org')

def get_info_hash(magnet_link):
    return magnet_link[20:60]

def get_scrape_url(info_hash):
    return 'http://tracker.gilgi.org:6969/scrape?info_hash=' + urllib.quote_plus(binascii.a2b_hex(info_hash))

class Torrent(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    description = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    magnet_link = models.CharField(max_length=256, validators=[magnet_validator])

    class Meta:
        ordering = ['added']
    
    def get_info(self):
        response = urllib.urlopen(get_scrape_url(get_info_hash(self.magnet_link)))
        match = re.match( r'd5.*completei(.*)e10:downloadedi(.*)e10:incompletei(.*)eeee', response.read(), re.M|re.I)
        if match:
            return {'seeders': match.group(1), 'leechers': match.group(3), 'downloads': match.group(2)}
        return {'seeders': -1, 'leechers': -1, 'downloads': -1}

    def get_absolute_url(self):
        return reverse('torrent', kwargs={'pk': self.pk})
        
    def __unicode__(self):
        return self.title
