from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
)

from django import forms


class IMECXFormMixin:
    """
    Aplica automaticamente o design system do IMECX
    aos widgets dos formulários.
    """

    def _style_fields(self):
        for field in self.fields.values():
            # Não aplicar aos checkboxes
            if isinstance(field.widget, forms.CheckboxInput):
                continue

            css = field.widget.attrs.get("class", "")
            classes = css.split()

            if "field__control" not in classes:
                classes.append("field__control")

            field.widget.attrs["class"] = " ".join(classes)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class IMECXLoginForm(IMECXFormMixin, LoginForm):
    pass


class IMECXSignupForm(IMECXFormMixin, SignupForm):
    pass


class IMECXResetPasswordForm(IMECXFormMixin, ResetPasswordForm):
    pass

class IMECXResetPasswordKeyForm(IMECXFormMixin, ResetPasswordKeyForm):
    pass