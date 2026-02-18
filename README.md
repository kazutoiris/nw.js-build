# NW.js Build Automation for Windows

[![Build Status](https://github.com/kazutoiris/NW.js-Build/workflows/Build%20NW.js%20on%20Windows/badge.svg)](https://github.com/kazutoiris/NW.js-Build/actions)

Automated build system for NW.js using GitHub Actions with resumable builds.

## 🎯 Overview

This repository provides an automated build pipeline for NW.js applications using GitHub Actions. The system implements a resumable build approach with artifact caching to handle long-running compilation processes that may exceed GitHub's timeout limits.

## 🛠 Prerequisites

- GitHub repository with Actions enabled

## 🚀 Getting Started

### 1. Repository Setup

Fork this repository or create a new repository using this as a template.

### 2. Trigger Builds

The workflow can be triggered in three ways:

- **Manual dispatch**: Use GitHub Actions UI with custom NW.js version (like `nw97`)
- **Push to main branch**: Automatic build trigger
- **Scheduled**: Weekly Sunday runs

## ⚠️ Compatibility Notes

NW.js versions prior to `nw90` are not supported due to architectural changes and dependency requirements.

## 📄 License

This project is licensed under the Anti-996 License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for the NW.js community
</p>
