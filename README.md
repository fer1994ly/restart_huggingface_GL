# restart_huggingface

Reinicia automáticamente un Hugging Face Space todos los días usando GitHub Actions.

## Cómo funciona

El workflow [`.github/workflows/restart-space.yml`](.github/workflows/restart-space.yml) se ejecuta:

- **Todos los días a las 06:00 UTC** (07:00 hora de UK en horario de verano) mediante un cron.
- **Manualmente** desde la pestaña *Actions* (botón *Run workflow*).

Reinicia el Space `ferferefer/Glaucoma-EyeFundus-ML`.

## Configuración requerida

Antes de que funcione, agrega tu token de Hugging Face como secreto en el repo:

1. Ve a **Settings → Secrets and variables → Actions → New repository secret**.
2. Nombre: `HF_TOKEN`
3. Valor: tu token de escritura de https://huggingface.co/settings/tokens
