
from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension

class Migration(migrations.Migration):

    dependencies = [
        # Coloque a última migration do seu app aqui, por exemplo:
        ('cidadao', '0001_initial'),
    ]

    operations = [
        UnaccentExtension(),
    ]