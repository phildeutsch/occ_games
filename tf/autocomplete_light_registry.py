import autocomplete_light.shortcuts as al
from models import TfPlayer

# This will generate a PersonAutocomplete class
class PersonAutocomplete(al.AutocompleteModelBase):
    search_fields = ['^first_name', 'last_name']
    model = TfPlayer
al.register(PersonAutocomplete)
