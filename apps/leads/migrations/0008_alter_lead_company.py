from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "companies",
            "0002_remove_company_company_owner_company_company_owner",
        ),
        (
            "leads",
            "0007_alter_lead_company",
        ),
    ]

    operations = []