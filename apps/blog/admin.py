from django.contrib import admin
from models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('title', 'author', 'votes', 'datetime')
    actions = ['do_some_action']

    def do_some_action(self, request, queryset):
        print "YES"
    do_some_action.short_description = "Description of the action!"


BLACKLISTED_USERS = ('admin@admin.com', )

class CommentAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('get_comment_author', 'post')
    actions = ['accept', 'reject']

    def get_comment_author(self, obj):
        return obj.author.email
    get_comment_author.short_description = 'Author'

    def accept(self, request, queryset):
        rows_num = queryset.count() #queryset.update(status=ACCEPTED)
        self.message_user(request, "%s successfully accepted." % rows_num)
    accept.short_description = '"Accept" Comments!'

    def reject(self, request, queryset):
        rows_num = queryset.count() #queryset.update(status=REJECTED)
        self.message_user(request, "%s successfully rejected." % rows_num)
    reject.short_description = '"Reject" Comments!'

    def get_actions(self, request):
        global BLACKLISTED_USERS
        actions = super(CommentAdmin, self).get_actions(request)
        if request.user.email in BLACKLISTED_USERS:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
