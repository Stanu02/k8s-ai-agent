# Kubernetes AI Troubleshooting Agent

## Overview

An AI-powered Kubernetes troubleshooting agent that automatically detects unhealthy pods, collects diagnostic information, and uses Google Gemini to provide root cause analysis and recommended fixes.

## Features

* Detect unhealthy Kubernetes pods
* Collect Kubernetes events
* Collect pod logs
* Collect container exit codes
* Collect container commands and arguments
* Generate AI-powered root cause analysis
* Recommend remediation steps

## Architecture

Kubernetes Cluster
↓
Python Agent
↓
Collect Events + Logs + Exit Codes
↓
Google Gemini
↓
Root Cause Analysis

## Tech Stack

* Python
* Kubernetes
* Minikube
* Google Gemini
* Docker

## Setup

Install dependencies:

pip install -r requirements.txt

Configure environment variables:

Create a `.env` file:

GEMINI_API_KEY=your_api_key

Run:

python agent.py

## Example Use Cases

* CrashLoopBackOff
* ImagePullBackOff
* Container startup failures
* Kubernetes troubleshooting automation

## Future Improvements

* Multi-namespace support
* Slack integration
* Streamlit dashboard
* Automated remediation
* Prometheus integration
