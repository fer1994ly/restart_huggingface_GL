"""Check a Hugging Face Space and restart it only if it is down or sleeping."""

import os
import sys

# Stages we consider "up and working"
HEALTHY = {"RUNNING", "RUNNING_BUILDING", "BUILDING", "RUNNING_APP_STARTING", "APP_STARTING"}


def keep_awake(api, repo_id):
    try:
        stage = api.get_space_runtime(repo_id).stage
        print(f"[{repo_id}] Estado actual del Space: {stage}")
    except Exception as e:
        print(f"[{repo_id}] ERROR al consultar el estado: {e}")
        return 1

    if stage in HEALTHY:
        print(f"[{repo_id}] El Space está funcionando. No hace falta reiniciar.")
        return 0

    print(f"[{repo_id}] El Space está caído/dormido ({stage}). Reiniciando...")
    try:
        api.restart_space(repo_id=repo_id)
        print(f"[{repo_id}] Space reiniciado correctamente")
    except Exception as e:
        print(f"[{repo_id}] ERROR al reiniciar: {e}")
        return 1
    return 0


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: el secreto HF_TOKEN no está configurado en el repo.")
        return 1

    repo_id = os.environ.get("SPACE_ID")
    if not repo_id:
        print("ERROR: la variable SPACE_ID no está definida.")
        return 1

    from huggingface_hub import HfApi

    return keep_awake(HfApi(token=token), repo_id)


if __name__ == "__main__":
    sys.exit(main())
