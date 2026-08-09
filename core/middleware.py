from django.core.cache import cache
from django.http import HttpResponse


class RateLimitMiddleware:
    """
    Rate limiting simples por IP em formularios publicos sensiveis
    (login e candidaturas), usando a cache do Django — sem
    dependencias novas. So conta pedidos POST.

    Nota: com base na cache local (LocMemCache), os contadores sao
    por processo. Se a app vier a correr em varios workers/processos
    ao mesmo tempo, cada um conta a sua parte e o limite efetivo
    sobe proporcionalmente. Para um limite rigoroso nesse cenario,
    trocar para uma cache partilhada (ex: Redis/memcached).
    """

    LIMITS = {
        "/conta/login/": (10, 5 * 60),      # 10 pedidos / 5 min por IP
        "/candidaturas/": (5, 10 * 60),     # 5 candidaturas / 10 min por IP
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == "POST":

            limit_config = self.LIMITS.get(request.path)

            if limit_config:

                limit, period = limit_config
                ip = request.META.get("REMOTE_ADDR", "unknown")
                cache_key = f"ratelimit:{request.path}:{ip}"
                count = cache.get(cache_key, 0)

                if count >= limit:
                    return HttpResponse(
                        "<h1>Demasiados pedidos</h1>"
                        "<p>Tenta novamente daqui a alguns minutos.</p>",
                        status=429,
                        content_type="text/html; charset=utf-8",
                    )

                # incrementa mantendo o TTL original (nao renova a
                # janela a cada pedido, senao um utilizador ativo
                # nunca deixava de estar limitado)
                if count == 0:
                    cache.set(cache_key, 1, period)
                else:
                    cache.incr(cache_key)

        return self.get_response(request)


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
