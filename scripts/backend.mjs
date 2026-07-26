import { spawn } from 'node:child_process'
import { getPythonCommand } from './python-command.mjs'

const child = spawn(
  getPythonCommand(),
  ['apps/backend/manage.py', ...process.argv.slice(2)],
  { stdio: 'inherit' },
)

child.on('error', (error) => {
  console.error(`Não foi possível iniciar o Python: ${error.message}`)
  process.exitCode = 1
})

child.on('exit', (code) => {
  process.exitCode = code ?? 1
})
