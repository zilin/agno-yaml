# Agno YAML Builder

A Python utility library for defining and constructing [Agno](https://github.com/agno-agi/agno) Agents, Teams, and Workflows using declarative YAML configuration files.

## Status

[![PyPI version](https://badge.fury.io/py/agno-yaml-builder.svg)](https://badge.fury.io/py/agno-yaml-builder) [![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/MIT) 

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

## Quickstart

You can clone this repo using:

```bash
git clone git@github.com:zilin/agno-yaml.git
```

Try some examples.
```bash
python -m agno_yaml.main
```
