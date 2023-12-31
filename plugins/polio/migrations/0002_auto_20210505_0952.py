# Generated by Django 3.0.14 on 2021-05-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polio", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="ag_nopv_group_met_at",
            field=models.DateField(blank=True, null=True, verbose_name="AG/nOPV Group"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="cvdpv2_notified_at",
            field=models.DateField(blank=True, null=True, verbose_name="cVDPV2 Notication"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="cvdpv_notified_at",
            field=models.DateField(blank=True, null=True, verbose_name="cVDPV Notication"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="detection_first_draft_submitted_at",
            field=models.DateField(blank=True, null=True, verbose_name="1st Draft Submission"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="detection_rrt_oprtt_approval_at",
            field=models.DateField(blank=True, null=True, verbose_name="RRT/OPRTT Approval"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="dg_authorized_at",
            field=models.DateField(blank=True, null=True, verbose_name="DG Authorization"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="eomg",
            field=models.DateField(blank=True, null=True, verbose_name="EOMG"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="investigation_at",
            field=models.DateField(blank=True, null=True, verbose_name="Field Investigation Date"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="onset_at",
            field=models.DateField(blank=True, help_text="When the campaign starts", null=True),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="pv2_notified_at",
            field=models.DateField(blank=True, null=True, verbose_name="PV2 Notication"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="pv_notified_at",
            field=models.DateField(blank=True, null=True, verbose_name="PV Notication"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="risk_assessment_first_draft_submitted_at",
            field=models.DateField(blank=True, null=True, verbose_name="1st Draft Submission"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="risk_assessment_rrt_oprtt_approval_at",
            field=models.DateField(blank=True, null=True, verbose_name="RRT/OPRTT Approval"),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="three_level_call_at",
            field=models.DateField(blank=True, null=True, verbose_name="3 level call"),
        ),
        migrations.AlterField(
            model_name="round",
            name="ended_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="im_ended_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="im_started_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="lqas_ended_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="lqas_started_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="mop_up_ended_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="mop_up_started_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="round",
            name="started_at",
            field=models.DateField(blank=True, null=True),
        ),
    ]
