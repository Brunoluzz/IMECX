from django.shortcuts import render, redirect
from django.contrib import messages
from editions.models import Edition
from .forms import ApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .models import Application


def apply(request):
    edition = Edition.objects.filter(status="open").first()
    if request.method == "POST" and edition:
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.edition = edition
            if request.user.is_authenticated:
                app.user = request.user
            app.save()
            messages.success(request, "Candidatura submetida. Vamos contactar-te em breve!")
            return redirect("applications:thanks")
    else:
        form = ApplicationForm()
    return render(request, "applications/apply.html", {"form": form, "edition": edition})


def thanks(request):
    return render(request, "applications/thanks.html")

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    fields = ["edition", "full_name", "email", "university", "course_year", "area", "motivation", "cv"]
    login_url = "account_login"
    template_name = "applications/application_form.html"
    success_url = "/conta/area/"  # ajustamos para {% url %} quando tivermos o nome da rota

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
