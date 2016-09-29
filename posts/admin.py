from django.contrib import admin

from .models import Post

# registering Post model in the admin


class PostAdmin(admin.ModelAdmin):
	
	list_display = ["title", "updated", "timestamp"]
	list_filter = ["updated", "timestamp"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	search_fields = ["title", "timestamp"]
	
	class Meta:
		model = Post

admin.site.register(Post, PostAdmin)
