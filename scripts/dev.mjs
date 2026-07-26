import { spawn } from 'node:child_process'
import { getPythonCommand } from './python-command.mjs'

const isWindows = process.platform === 'win32'
const npmCommand = isWindows ? 'npm.cmd' : 'npm'
const pythonCommand = getPythonCommand()

const processes = [
  spawn(pythonCommand, ['apps/backend/manage.py', 'runserver'], {
    stdio: 'inherit',
  }),
  spawn(npmCommand, ['run', 'dev', '--workspace=apps/frontend'], {
    stdio: 'inherit',
  }),
]

let stopping = false

function stop(exitCode = 0) {
  if (stopping) return
  stopping = true

  for (const child of processes) {
    if (!child.killed) child.kill()
  }

  process.exitCode = exitCode
}

for (const child of processes) {
  child.on('error', (error) => {
    console.error(error.message)
    stop(1)
  })

  child.on('exit', (code, signal) => {
    if (!stopping && (code !== 0 || signal)) stop(code ?? 1)
  })
}

process.on('SIGINT', () => stop())
process.on('SIGTERM', () => stop())
