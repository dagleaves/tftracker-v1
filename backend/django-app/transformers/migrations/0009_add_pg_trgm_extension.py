from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ("transformers", "0008_alter_transformer_subline_alter_transformer_toyline"),
    ]

    operations = [
        CreateExtension(name='pg_trgm'),
    ] 