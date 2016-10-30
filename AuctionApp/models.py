from django.db import models

# Create your models here.
class itemType(models.Model):
    typeName = models.CharField(max_length=30)

    @classmethod
    def getByTypeName(cls, typeName):
        return cls.objects.get(typeName=typeName)

    @classmethod
    def getAll(self):
        return self.objects.all()
    @classmethod
    def getAll(self):
        return self.objects.all()
    def exists(self,Id):
        return len(itemType.objects.filter(id=Id)) > 0

# Create your models here.