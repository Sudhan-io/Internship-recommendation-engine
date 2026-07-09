# Contributing to InternMatch

Thank you for your interest in contributing to InternMatch! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Environment](#development-environment)
4. [Branching Strategy](#branching-strategy)
5. [Pull Request Process](#pull-request-process)
6. [Issue Reporting](#issue-reporting)

## Code of Conduct
This project and everyone participating in it is governed by the [InternMatch Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started
1. **Fork the repository** on GitHub.
2. **Clone your fork** locally.
3. **Create a new branch** for your feature or bug fix.

## Development Environment
Please refer to the [Installation Guide](docs/INSTALLATION.md) and [Running Guide](docs/RUNNING.md) to set up your local development environment. The project spans three primary stacks:
- **Backend**: Java 17 + Spring Boot
- **Frontend**: React 18 + Vite + Tailwind
- **AI Service**: Python 3.12 + FastAPI + spaCy

Ensure all three are running and interacting correctly before submitting major changes.

## Branching Strategy
- `main`: Represents the production-ready code.
- `dev` or `development`: Represents the active integration branch.
- `feature/<feature-name>`: For new features (e.g., `feature/improved-embeddings`).
- `bugfix/<bug-name>`: For bug fixes (e.g., `bugfix/fix-resume-parsing`).

## Pull Request Process
1. Ensure your code passes all local linting (e.g., `eslint` for frontend, `flake8` for python).
2. Update any relevant documentation in `docs/` and the `README.md`.
3. Submit a Pull Request against the `main` (or `dev`) branch.
4. Provide a clear description of the problem you're solving and your approach.
5. Wait for a code review and address any feedback.

## Issue Reporting
If you find a bug or have a feature request, please open an issue in the GitHub repository. Provide as much context as possible, including:
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
- Screenshots if applicable.
- Environment details (OS, Docker vs Local, Browser).
