# Cria os grupos de staff do admin e as respetivas permissoes.
#
# Sao permissoes sobre os DADOS do programa (candidaturas, edicoes,
# tarefas, participacoes) — nunca sobre utilizadores, grupos ou o
# django-axes. Essas ficam reservadas a superusers, para que o
# acesso aos registos de tentativas de login (axes) e a gestao de
# quem e staff continue limitado a quem ja e superuser hoje.

from django.db import migrations


GROUPS = {
    "Administrador": [
        # Gere por completo os dados do programa.
        ("applications", "application", ["add", "change", "delete", "view"]),
        ("applications", "participation", ["add", "change", "delete", "view"]),
        ("applications", "engineeringarea", ["add", "change", "delete", "view"]),
        ("editions", "edition", ["add", "change", "delete", "view"]),
        ("tasks", "task", ["add", "change", "delete", "view"]),
        ("tasks", "tasksubmission", ["add", "change", "delete", "view"]),
        ("tasks", "notification", ["view"]),
        ("accounts", "profile", ["view", "change"]),
    ],
    "Técnico": [
        # Cria/gere tarefas e avalia submissoes.
        ("tasks", "task", ["add", "change", "view"]),
        ("tasks", "tasksubmission", ["change", "view"]),
        ("tasks", "notification", ["view"]),
        ("applications", "participation", ["view"]),
        ("editions", "edition", ["view"]),
    ],
    "Funcionário": [
        # Trata candidaturas e a logistica das edicoes.
        ("applications", "application", ["add", "change", "delete", "view"]),
        ("applications", "engineeringarea", ["add", "change", "delete", "view"]),
        ("applications", "participation", ["change", "view"]),
        ("editions", "edition", ["change", "view"]),
    ],
}


def create_groups(apps, schema_editor):

    # Garante que as permissoes de add/change/delete/view de cada
    # modelo ja existem, mesmo que os modelos tenham sido criados
    # nesta mesma execucao de "migrate" (as permissoes normalmente
    # so sao criadas no post_migrate, que corre so no fim).
    from django.contrib.auth.management import create_permissions

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    for group_name, rules in GROUPS.items():

        group, _ = Group.objects.get_or_create(name=group_name)

        permissions = []

        for app_label, model_name, actions in rules:

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

        group.permissions.set(permissions)


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=GROUPS.keys()).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("applications", "0009_alter_participation_options"),
        ("editions", "0003_edition_initial_points"),
        ("tasks", "0008_alter_notification_options_alter_task_options_and_more"),
        ("accounts", "0004_alter_profile_options"),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
