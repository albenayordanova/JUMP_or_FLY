from django import forms

from jump.main_app.models import Equip, Spot
from jump.common.view_mixins import BootstrapFormMixin, DisabledFieldsFormMixin


class CreateEquipForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        equip = super().save(commit=False)
        equip.user = self.user
        if commit:
            equip.save()
        return equip

    class Meta:
        model = Equip
        fields = ('brand', 'type', 'date_of_manufacture')
        widgets = {
            'brand': forms.TextInput(
                attrs={
                    'placeholder': "Enter equip brand and model",
                }
            ),
        }


class EditEquipForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Equip
        exclude = ('user',)


class DeleteEquipForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Equip
        exclude = ('user',)


class SpotForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        spot = super().save(commit=commit)
        if commit:
            spot.save()
        return spot

    class Meta:
        model = Spot
        fields = ('name', 'picture', 'description')
