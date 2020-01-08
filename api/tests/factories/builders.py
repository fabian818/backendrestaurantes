from django.core.management import call_command


def meta_data():
    call_command("sh", "fixtures/create_metadata.sh", verbosity=0)


def meta_data_specific(files):
    for file in files:
        call_command("loaddata", f"fixtures/{file}.yaml", verbosity=0)