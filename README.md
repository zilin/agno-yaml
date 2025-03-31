# Agno YAML Builder

[![PyPI version](https://badge.fury.io/py/agno-yaml-builder.svg)](https://badge.fury.io/py/agno-yaml-builder) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://github.com/zilin/agno-yaml/actions/workflows/ci.yml/badge.svg)](https://github.com/zilin/agno-yaml/actions/workflows/ci.yml) [![Coverage Status](https://coveralls.io/repos/github/zilin/agno-yaml/badge.svg?branch=main)](https://coveralls.io/github/zilin/agno-yaml?branch=main) A Python utility library for defining and constructing [Agno](https://github.com/agno-agi/agno) Agents, Teams, and Workflows using declarative YAML configuration files.

## Overview

The Agno library provides powerful primitives for building sophisticated AI agent systems. However, defining complex Agents, Teams with multiple agents, and multi-step Workflows directly in Python code can become verbose and harder to manage.

`agno-yaml-builder` bridges this gap by allowing you to define your Agno components in human-readable YAML files. This promotes a declarative approach, making it easier to configure, share, and version control your agent structures.

## Key Features

* **Declarative Configuration:** Define Agno Agents, Teams, and Workflows using intuitive YAML syntax.
* **Simplified Instantiation:** Load complex Agno structures from YAML files with a simple Python function call.
* **Component Referencing:** Easily reference defined Agents within Teams or Workflows by name.
* **Human-Readable:** YAML format makes configurations easy to read, write, and maintain.
* **Seamless Integration:** Works directly with the core `agno` library objects.

## Prerequisites

* Python 3.8+ (or your supported versions)
* `pip` package manager

## Installation

You can install `agno-yaml-builder` using pip:

```bash
pip install agno-yaml-builder
```