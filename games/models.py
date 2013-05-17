from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.context_processors import csrf
from datetime import datetime
from PIL import Image, ImageOps
import StringIO
import re
import os



class Game(models.Model):
    name = models.CharField(max_length=20)
    url = models.SlugField(max_length=20, editable = False, unique=True)     
    date = models.DateField(default=datetime.now())
    details = models.TextField()
    image = models.ImageField(upload_to=
        lambda instance, filename: 'games/' + instance.url+'/image',
        blank=True)
    thumbnail = models.ImageField(upload_to=
        lambda instance, filename: 'games/' + instance.url+'/thumbnail',
        blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_obj = Game.objects.get(pk = self.pk)
            if self.image is not None and self.image.path != old_obj.image.path:
                try:
                    os.remove(old_obj.image.path)
                except:
                    pass
        else:
            self.url = slugify(self.name)

        try:
            os.remove(self.thumbnail.path)
        except:
            pass
        super(Game, self).save(*args, **kwargs)
        if self.image:
            imgFile = Image.open(self.image.path)
            if imgFile.mode not in ('L', 'RGB'):
                imgFile = imgFile.convert('RGB')
            working = imgFile.copy()
            working.thumbnail((192,144), Image.ANTIALIAS)
            fp = StringIO.StringIO()
            working.save(fp, "JPEG", quality=95)
            cf = ContentFile(fp.getvalue())
            try:
                os.remove(self.thumbnail.path)
            except:
                pass
            self.thumbnail.save(name=self.image.name, content=cf, save=False);
        super(Game, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name


class GameResource(models.Model):
    name = models.CharField(max_length=20)
    game = models.ForeignKey(Game, related_name='resources')
    link = models.CharField(max_length=256,blank=True,null=True)
    file = models.FileField(upload_to=lambda instance, filename: 'games/' +instance.game.url+'/'+
        instance.game.url+'-'+slugify(instance.name)+
        re.search("\.[^.]*$", filename).group(),blank=True,null=True)
    url = models.CharField(max_length=256,editable=False) 

    def save(self):
        if self.pk is not None:
            old = GameResource.objects.get(pk = self.pk)
            if self.file is not None and self.file.path != old.file.path:
                try:
                    os.remove(old.file.path)
                except:
                    pass
        super(GameResource, self).save()
        if self.file:
            self.url = self.file.url
        elif self.link:
            self.url = self.link
        else:
            self.url = ''
        super(GameResource, self).save()
    
    def __unicode__(self):
        return self.game.name + ' ('+self.name+')'
    
