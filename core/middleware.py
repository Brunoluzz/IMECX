class SecurityHeadersMiddleware:
    """
    Cabecalhos de seguranca adicionais, em complemento aos ja
    aplicados pelo django.middleware.security.SecurityMiddleware
    (HSTS, X-Content-Type-Options, etc. — ver settings.py).

    A Content-Security-Policy abaixo reflete o que o site
    efetivamente carrega hoje (fontes da Google, htmx via unpkg,
    ficheiros estaticos proprios). Se adicionares um novo script ou
    stylesheet externo, tens de o acrescentar aqui tambem, senao o
    browser bloqueia-o.
    """

    CSP = "; ".join([
        "default-src 'self'",
        "script-src 'self' https://unpkg.com",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data:",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ])

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # O admin (Jazzmin) carrega os seus proprios bundles JS/CSS
        # de formas que nao foram todas auditadas aqui; para nao
        # arriscar partir o painel em produção, a CSP so se aplica
        # ao site publico. O admin continua protegido pelas outras
        # camadas (login, axes, permissões, HTTPS, HSTS, etc.).
        if not request.path.startswith("/admin/"):
            response.setdefault("Content-Security-Policy", self.CSP)

        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")

        return response
