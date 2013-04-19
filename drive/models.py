import binascii, urllib, re

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from .random_primary import RandomPrimaryIdModel

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

def magnet_validator(value):
    if value:
        if not 'tr=udp%3a%2f%2ftracker.gilgi.org%3a6969%2fannounce' in value:
            raise ValidationError(u'torrent must use tracker.gilgi.org')

def get_info_hash(magnet_link):
    return magnet_link[20:60]

def get_scrape_url(info_hash):
    return 'http://tracker.gilgi.org:6969/scrape?info_hash=' + urllib.quote_plus(binascii.a2b_hex(info_hash))

class File(RandomPrimaryIdModel):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    description = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    magnet_link = models.CharField(max_length=256, validators=[magnet_validator], blank=True, null=True)
    direct_link = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ['-added']
    
    def get_info(self):
        if not self.magnet_link:
            return {'seeders': 0, 'leechers': 0, 'downloads': 0}
        response = urllib.urlopen(get_scrape_url(get_info_hash(self.magnet_link)))
        match = re.match( r'.*completei(.*)e10:downloadedi(.*)e10:incompletei(.*)eeee', response.read(), re.S|re.M|re.I)
        if match:
            #print 'match succeeded'
            #response = urllib.urlopen(get_scrape_url(get_info_hash(self.magnet_link)))
            #print response.read()
            return {'seeders': match.group(1), 'leechers': match.group(3), 'downloads': match.group(2)}
        #print 'match failed'
        #response = urllib.urlopen(get_scrape_url(get_info_hash(self.magnet_link)))
        #print response.read()
        return {'seeders': 0, 'leechers': 0, 'downloads': 0}

    def get_absolute_url(self):
        return reverse('file', kwargs={'pk': self.pk})
        
    def __unicode__(self):
        return self.title
