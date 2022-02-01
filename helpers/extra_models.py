from django.db import models


# this class contains the creatd_date field that will be used in both post and story model.
class CreatedDateModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        abstract = True  # abstract class so we can't make instances from this class.
