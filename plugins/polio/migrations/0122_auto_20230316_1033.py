# Generated by Django 3.2.15 on 2023-03-16 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0121_merge_20230112_1017"),
    ]

    operations = [
        migrations.RenameField(
            model_name="campaign",
            old_name="gpei_consolidation_at_WFEDITABLE",
            new_name="gpei_consolidated_budgets_at_WFEDITABLE",
        ),
        migrations.RenameField(
            model_name="campaign",
            old_name="re_submission_to_orpg_operations_2_at_WFEDITABLE",
            new_name="re_submitted_to_orpg_operations2_at_WFEDITABLE",
        ),
        migrations.RenameField(
            model_name="campaign",
            old_name="submission_to_orpg_operations_1_at_WFEDITABLE",
            new_name="submitted_to_orpg_operations1_at_WFEDITABLE",
        ),
        migrations.RenameField(
            model_name="campaign",
            old_name="submission_to_orpg_operations_2_at_WFEDITABLE",
            new_name="submitted_to_orpg_operations2_at_WFEDITABLE",
        ),
        migrations.RenameField(
            model_name="campaign",
            old_name="submitted_to_orpg_at_WFEDITABLE",
            new_name="submitted_to_orpg_wider_at_WFEDITABLE",
        ),
        migrations.AddField(
            model_name="campaign",
            name="approval_confirmed_at_WFEDITABLE",
            field=models.DateField(blank=True, null=True),
        ),
    ]
