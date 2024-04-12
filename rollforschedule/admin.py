from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class GenericView(ModelView):

    column_hide_backrefs = False
    column_display_pk = True
    can_delete = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin_rights

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index', next=request.url))


class PlayerView(GenericView):

    column_list = (
        'id', 'username', 'email', 'admin_rights', 'created_at', 'tables'
    )

    def get_edit_form(self):
        form_class = super(PlayerView, self).get_edit_form()
        del form_class.password
        return form_class


class TableView(GenericView):

    column_list = ('id', 'title', 'description', 'players')


class AvailabilityView(GenericView):

    column_list = ('player_id', 'day', 'available')


class AdminView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin_rights

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index'))
