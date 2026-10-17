import django.db.models.deletion
from django.db import migrations, models


def migrate_company_names(apps, schema_editor):
    Lead = apps.get_model("leads", "Lead")
    Company = apps.get_model("companies", "Company")

    db = schema_editor.connection.alias

    for lead in Lead.objects.using(db).all():
        company_name = lead.company

        if not company_name:
            continue

        company_name = str(company_name).strip()

        company = (
            Company.objects.using(db)
            .filter(company_name__iexact=company_name)
            .first()
        )

        if company is None:
            raise ValueError(
                f"Company '{company_name}' for lead {lead.id} "
                "does not exist in the companies table."
            )

        lead.company_new_id = company.id
        lead.save(using=db, update_fields=["company_new"])


class Migration(migrations.Migration):

    dependencies = [
        (
            "companies",
            "0002_remove_company_company_owner_company_company_owner",
        ),
        (
            "leads",
            "0006_remove_lead_products_lead_products",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="company_new",
            field=models.ForeignKey(
                to="companies.company",
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name="+",
            ),
        ),
        migrations.RunPython(migrate_company_names),
        migrations.RemoveField(
            model_name="lead",
            name="company",
        ),
        migrations.RenameField(
            model_name="lead",
            old_name="company_new",
            new_name="company",
        ),
    ]