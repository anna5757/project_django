from django.contrib import admin
from task_manager.models import Tasks, Tags, Projects, ProjectsDetails, Comments, Attachments
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.admin import EmptyFieldListFilter
# Register your models here.
from django.utils.safestring import mark_safe
from task_manager.models.tasks import TaskStatus



#inline
class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1

class TagsInline(admin.TabularInline):
    model = Tags.tasks.through
    extra = 1

class AttachmentsInline(admin.StackedInline):
    model = Attachments
    extra = 1

class ProjectDetailsInline(admin.StackedInline):
    model = ProjectsDetails
    extra = 1
#StackedInline - улучшает визуальное восприятие и читаемость, особенно когда текст длинный


class TasksAdmin(admin.ModelAdmin):
    #fields = ("description",("name", "status"), "created_at","comments_count")
    #readonly_fields = ("created_at", "comments_count")
    fields = (("name", "status"),"description", "priority")
    #fields = ("name", "description", "status")#какие поля показ для отображение в конкрет задаче
    #exclude = ("is_reopened",) #какие поля искл для отображение в конкрет задаче
    # fieldsets = []
    #     (
    #         None,
    #         {
    #             "fields": ["name", "status", "priority",], #основные поля для отображения
    #         },
    #     ),
    #     (
    #         "Advanced options",
    #         {
    #             "classes": ["collapse"], #  свернутом окне дополнительные поля
    #             "fields": ["assignee", "description", "project"],
    #         },
    #     ),
    # ]
    list_display = (
        "display_name",
        "status",
        "priority",
        "project",
        "assignee",
        "name_and_status", # мое кастомное поле
        "priority_status",
        "assignee_email",
        "is_reopened",
    ) #что в общем списке задач. какие именно колонки. существ + ккастомное
    def name_and_status(self, obj):
        return f'{obj.name} - {obj.status}'

    # readonly_fields = ("status",)
    exclude = ("is_reopened",) #какие поля искл для отображение в конкрет задаче
    list_editable = ("status", "priority",) # менять поля модели прямо в списке не переходя на конкрет задачу
    list_display_links = ("display_name",) #по какой колонке в общем списке переход на задачу
    search_fields = ("name",)
    list_filter = (
        "status",
        "priority",
        "project",
        "assignee",
        ("assignee", EmptyFieldListFilter),
    )
    ordering = ("-priority","name")
    inlines = (CommentsInline, AttachmentsInline, TagsInline)
    actions = (
        "make_canceled",
        "decrease_priority",
        "make_completed",
        "make_reopened",
        "process_admin",
        )

    def priority_status(self,obj):  #свое поле со своими значения в поле
        if obj.priority < 3:
            return "LOW"
        if obj.priority < 5:
            return "MEDIUM"
        return "HIGH"
    priority_status.string = ""
    priority_status.short_description = "приоритет статуса"

    @admin.display(description="Наименование")
    def display_name(self, instance):
        return mark_safe(f"<h1>{instance.name}</h1>")

    @admin.display(description="Email", ordering="assignee__email")
    def assignee_email(self, obj):
        return obj.assignee.email if obj.assignee else "-"

    @admin.display(description="Количество комментариев")
    def comments_count(self, obj):
        return obj.comments.count()


    @admin.action(description="Mark selected status as canceled")
    def make_canceled(modeladmin, request, queryset):
        queryset.update(status=TaskStatus.CANCELED)

    @admin.action(description="Mark selected status as finished")
    def make_completed(modeladmin, request, queryset):
        queryset.update(status=TaskStatus.COMPLETED)

    @admin.action(description="Mark selected tasks as reopened")
    def make_reopened(modeladmin, request, queryset):
        queryset.udate(is_reopened = False)

    @admin.action(description="Добавить комментарий 'Processed by admin'")
    def process_admin(modeladmin, request, queryset):
        for task in queryset:
            Comments.objects.create(
                task = task,
                message = "Processed by admin"
            )

    @admin.action(description="Decrease priority on 1 point")
    def decrease_priority(self, request, queryset):
        lst_non_decrease_obj = []
        for obj in queryset:
            if obj.priority > 1:
                obj.priority -= 1
                obj.save()
            else:
                lst_non_decrease_obj.append(obj)
        if lst_non_decrease_obj:
            self.message_user(
                request,
                f"count not decrease priority obj {len(lst_non_decrease_obj)}. {[item.name for item in lst_non_decrease_obj]}",
                messages.ERROR,
            )

class ProjectsAdmin(admin.ModelAdmin):
    # fields = ("name", "description",)
    exclude = ("owner",)


    inlines = (ProjectDetailsInline,)


class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ("name","task","display_photo","photo","secure_view")
    @admin.display(description="Отображение картинки")
    def display_photo(self, instance):
        if instance.photo:
            return mark_safe(f'<img src={ instance.photo.url } width=50/>')



admin.site.register(Tasks,TasksAdmin)
admin.site.register(Tags)
admin.site.register(Projects,ProjectsAdmin)
admin.site.register(ProjectsDetails)
admin.site.register(Comments)
admin.site.register(Attachments, AttachmentsAdmin)