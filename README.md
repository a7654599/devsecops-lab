# devsecops-lab

DevOps Assignment 9 – Practicing DevSecOps Fundamentals.

A small Flask inventory service used as a target for:

| Level | Check | Where |
|---|---|---|
| A | Linting: Flake8 + flake8-bandit | `.flake8`, `.github/workflows/ci.yml` |
| E | SCA: GitHub Dependabot | `.github/dependabot.yml` |
| O | SAST: GitHub CodeQL | `.github/workflows/codeql.yml` |

> Demo repository only. It pins old, vulnerable dependencies on purpose. Do not deploy.
