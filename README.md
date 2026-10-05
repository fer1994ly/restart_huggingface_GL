# restart_huggingface

Mantiene despiertos varios Hugging Face Spaces usando GitHub Actions.

## Cómo funciona

El workflow [`.github/workflows/restart-space.yml`](.github/workflows/restart-space.yml) se ejecuta:

- **Cada 30 minutos** mediante un cron: consulta el estado de cada Space y lo reinicia solo si está caído o dormido.
- **Manualmente** desde la pestaña *Actions* (botón *Run workflow*).

Spaces vigilados (matriz del workflow):

- `ferferefer/Glaucoma-EyeFundus-ML`
- `ferferefer/retinal_age`

## Configuración requerida

Antes de que funcione, agrega tu token de Hugging Face como secreto en el repo:

1. Ve a **Settings → Secrets and variables → Actions → New repository secret**.
2. Nombre: `HF_TOKEN`
3. Valor: tu token de escritura de https://huggingface.co/settings/tokens

## Tests

```bash
pip install huggingface_hub pytest pyyaml
python -m pytest -q
```

El workflow ejecuta los tests antes de revisar cada Space.
