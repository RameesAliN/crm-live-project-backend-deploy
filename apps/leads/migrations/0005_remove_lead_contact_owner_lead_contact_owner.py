from django.conf import settings
from django.db import migrations, models


def copy_contact_owners(apps, schema_editor):
    Lead = apps.get_model("leads", "Lead")
    db_alias = schema_editor.connection.alias

    for lead in Lead.objects.using(db_alias).all():
        old_owner_id = lead.old_contact_owner_id

        if old_owner_id is not None:
            lead.contact_owner.add(old_owner_id)


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0004_alter_lead_lead_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="lead",
            old_name="contact_owner",
            new_name="old_contact_owner",
        ),
        migrations.AddField(
            model_name="lead",
            name="contact_owner",
            field=models.ManyToManyField(
                blank=True,
                related_name="owned_leads",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(
            copy_contact_owners,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="lead",
            name="old_contact_owner",
        ),
    ]