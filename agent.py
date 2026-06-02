from kubernetes import client, config
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

config.load_kube_config()

v1 = client.CoreV1Api()

pods = v1.list_namespaced_pod(namespace="default")

for pod in pods.items:

    statuses = pod.status.container_statuses

    if statuses and not statuses[0].ready:

        pod_name = pod.metadata.name

        print(f"\nAnalyzing: {pod_name}")
        print("-" * 50)

        # Events
        events = v1.list_namespaced_event(
            namespace="default"
        )

        event_text = ""

        for event in events.items:
            if event.involved_object.name == pod_name:
                event_text += (
                    f"Reason: {event.reason}\n"
                    f"Message: {event.message}\n\n"
                )

        # Logs
        try:
            logs = v1.read_namespaced_pod_log(
                name=pod_name,
                namespace="default",
                previous=True
            )
        except Exception:
            logs = "No logs available"

        # Exit Code
        exit_code = "Unknown"

        try:
            exit_code = (
                statuses[0]
                .last_state
                .terminated
                .exit_code
            )
        except Exception:
            pass

        container_command = (
            pod.spec.containers[0].command
        )

        container_args = (
            pod.spec.containers[0].args
        )

        try:
            response = gemini.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"""
You are a Senior Kubernetes SRE.

Analyze the following information.

Provide:

1. Issue Type
2. Root Cause
3. Impact
4. Recommended Fix

Pod Name:
{pod_name}

Exit Code:
{exit_code}

Command:
{container_command}

Args:
{container_args}

Events:
{event_text}

Logs:
{logs}
"""
            )

            print(response.text)

        except Exception as e:
            print(f"Gemini Error: {e}")