# Grupo "Direcao": pensado para quem hoje e superuser mas nao deve
# ter acesso ao axes (registos de tentativas de login). Como
# is_superuser ignora sempre todas as permissoes -- nao ha forma de
# um superuser "nao ver" uma parte do admin -- a unica forma de
# aplicar esta restricao e deixar de ser superuser e passar a
# depender de permissoes explicitas, como este grupo.
#
# Fica com tudo o que o grupo "Administrador" ja tem, mais gestao
# de Users e Groups (para poder continuar a gerir a equipa). Nunca
# ganha permissoes sobre o app "axes".

from django.db import migrations


EXTRA_PERMISSIONS = [
    ("auth", "user", ["add", "change", "delete", "view"]),
    ("auth", "group", ["add", "change", "delete", "view"]),
]


def create_direcao_group(apps, schema_editor):

    from django.contrib.auth.management import create_permissions

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    administrador = Group.objects.filter(name="Administrador").first()

    direcao, _ = Group.objects.get_or_create(name="Direção")

    permissions = list(administrador.permissions.all()) if administrador else []

    for app_label, model_name, actions in EXTRA_PERMISSIONS:

        content_type = ContentType.objects.get(
            app_label=app_label,
            model=model_name,
        )

        for action in actions:
            permissions.append(
                Permission.objects.get(
                    content_type=content_type,
                    codename=f"{action}_{model_name}",
                )
            )

    direcao.permissions.set(permissions)


def remove_direcao_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Direção").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_setup_groups"),
    ]

    operations = [
        migrations.RunPython(create_direcao_group, remove_direcao_group),
    ]
