import { existsSync } from 'node:fs'
import path from 'node:path'

export function getPythonCommand() {
  if (process.env.PYTHON) return process.env.PYTHON

  const candidates = process.platform === 'win32'
    ? ['.venv/Scripts/python.exe', 'apps/backend/venv/Scripts/python.exe']
    : ['.venv/bin/python', 'apps/backend/venv/bin/python']

  return candidates.find((candidate) => existsSync(candidate))
    ? path.resolve(candidates.find((candidate) => existsSync(candidate)))
    : (process.platform === 'win32' ? 'python' : 'python3')
}
