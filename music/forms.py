from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=70,
                             error_messages={
                                 'required': 'This field is required',
                                 'max_length': 'Max length character exceeds'
                             })


class CreatePlaylistForm(forms.Form):
    name = forms.CharField(max_length=100, label='Enter Playlist Name')


class FavouritesForm(forms.Form):
    song = forms.IntegerField()
