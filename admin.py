from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class AdminView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin_rights

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index', next=request.url))


class RFSAdminView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin_rights

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index'))
