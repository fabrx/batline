# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 15:49
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_branche', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_cat', models.CharField(choices=[('Cour', 'Cour'), ('Livre', 'Livre'), ('memoire', 'Mémoire'), ('tfc', 'TFC'), ('bats', 'BATS')], max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Faculte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_fac', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Fichier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=20)),
                ('universite', models.CharField(max_length=40)),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('date_modif', models.DateTimeField(auto_now=True)),
                ('fichier', models.FileField(upload_to='')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Categorie')),
                ('faculte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Faculte')),
            ],
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('age', models.IntegerField()),
                ('genre', models.CharField(choices=[('Mr', 'Monsier'), ('Mlle', 'Mademoiselle'), ('Mme', 'Madame')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('faculte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Faculte')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('fichier_post', models.FileField(null=True, upload_to='')),
                ('faculte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Faculte')),
                ('fichier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Fichier')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_promo', models.CharField(choices=[('G1', '1er Graduat'), ('G2', '2eme Graduat'), ('G3', '3eme Graduat'), ('L1', '1er Licence'), ('L2', '2eme Licence')], max_length=10)),
                ('faculte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Faculte')),
            ],
        ),
        migrations.CreateModel(
            name='Universite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigle', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
                ('date_de_creation', models.PositiveSmallIntegerField()),
                ('nombre_etudiant', models.PositiveIntegerField()),
                ('nom_recteur', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='membre',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Promotion'),
        ),
        migrations.AddField(
            model_name='membre',
            name='universite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Universite'),
        ),
        migrations.AddField(
            model_name='fichier',
            name='romotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Promotion'),
        ),
        migrations.AddField(
            model_name='branche',
            name='branche_categorie',
            field=models.ManyToManyField(to='web.Categorie'),
        ),
        migrations.AddField(
            model_name='branche',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Promotion'),
        ),
    ]
