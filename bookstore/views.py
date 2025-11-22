import os
import hmac
import hashlib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git

@csrf_exempt
def update(request):
    if request.method == "POST":
        # 1. Pegue o secret configurado no PythonAnywhere
        secret = os.environ.get("GITHUB_WEBHOOK_SECRET", "").encode()

        # 2. Pegue o header enviado pelo GitHub
        signature = request.headers.get("X-Hub-Signature-256")

        if signature is None:
            return HttpResponse("Missing signature", status=400)

        # 3. Calcule o hash do payload recebido
        mac = hmac.new(secret, msg=request.body, digestmod=hashlib.sha256)
        expected_signature = "sha256=" + mac.hexdigest()

        # 4. Compare com o header
        if not hmac.compare_digest(expected_signature, signature):
            return HttpResponse("Invalid signature", status=403)

        # 5. Se válido, faça o pull
        repo = git.Repo('/home/sidneygyne/book-store')
        origin = repo.remotes.origin
        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    return HttpResponse("Update endpoint is alive", status=200)
