# Production Change Approval System

## Overview
A rule-based system that validates infrastructure changes before execution.  
Inspired by real DevOps safety mechanisms.

## Features
- YAML-based input
- Rule validation engine
- Decision output:
  - AUTO-APPROVED
  - APPROVAL REQUIRED
  - BLOCKED
- REST API using FastAPI
- CLI support

## Tech Stack
- Python
- FastAPI
- PyYAML

## How to Run

### CLI
```bash
python change_gate.py test.yaml