from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	content = forms.CharField(
		widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Write your comment here...',
			'rows': 4
		}),
		label='Comment'
	)

	class Meta:
		model = Comment
		fields = ['content']
