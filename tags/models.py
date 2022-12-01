from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Тип табличных отношений для объекта, который тегнут. Определяет имя
    # таблицы БД, в которой объект записан
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Айди тегнутого объекта
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
