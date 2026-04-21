#!/usr/bin/env python3
"""
Kubernetes MCP Server

Gives an AI agent direct access to a Kubernetes cluster via SSH.
Read-only tools run automatically. Write tools require user confirmation.

Usage:
    pip install mcp fastmcp
    python3 k8s_mcp_server.py

Configuration:
    Edit the SSH_CONFIG section below to match your cluster.
"""

import subprocess
from mcp.server.fastmcp import FastMCP

# --- Configuration ---
# Edit these to match your cluster
SSH_HOST = "user@your-k8s-server"       # SSH target (user@hostname or user@ip)
SSH_KEY  = "~/.ssh/id_rsa"              # Path to your SSH private key

# Only these namespaces can be accessed — add yours here
ALLOWED_NAMESPACES = {
    "default",
    "production",
    "staging",
    "monitoring",
}

SSH_CMD = [
    "ssh",
    "-o", "IdentitiesOnly=yes",
    "-i", SSH_KEY,
    "-o", "ConnectTimeout=10",
    "-o", "LogLevel=ERROR",
    SSH_HOST,
]

# --- MCP Server ---
mcp = FastMCP(
    "k8s-cluster",
    instructions="""
    Kubernetes MCP server. Provides read and write access to a Kubernetes cluster via SSH.
    Read-only tools run automatically.
    Write tools (install, uninstall, delete) require explicit user confirmation before running.
    Only allowed namespaces can be accessed.
    """,
)


# --- Helpers ---

def _ssh(cmd: str, timeout: int = 30) -> str:
    """Run a command on the remote server via SSH and return the output."""
    result = subprocess.run(
        SSH_CMD + [cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    output = result.stdout.strip()
    if result.returncode != 0:
        error = result.stderr.strip()
        return f"ERROR (exit {result.returncode}):\n{error}\n{output}" if error else f"ERROR (exit {result.returncode}):\n{output}"
    return output


def _check_namespace(namespace: str) -> str | None:
    """Return an error message if the namespace is not allowed, otherwise None."""
    if namespace not in ALLOWED_NAMESPACES:
        allowed = ", ".join(sorted(ALLOWED_NAMESPACES))
        return f"Namespace '{namespace}' is not allowed. Allowed namespaces: {allowed}"
    return None


# ============================================================
# READ-ONLY TOOLS
# These run automatically without user confirmation.
# ============================================================

@mcp.tool()
def get_pods(namespace: str, label_selector: str = "") -> str:
    """
    List all pods in a namespace with their status and node.
    Optionally filter by label (e.g. label_selector='app=my-service').
    """
    if err := _check_namespace(namespace):
        return err
    cmd = f"kubectl get pods -n {namespace} -o wide"
    if label_selector:
        cmd += f" -l {label_selector}"
    return _ssh(cmd)


@mcp.tool()
def get_pod_logs(namespace: str, pod_name_pattern: str, lines: int = 100) -> str:
    """
    Get logs from a pod. Use a partial name pattern — the server will find the matching pod.
    Example: pod_name_pattern='my-service' will match 'my-service-7d9f8b-xkj2p'.
    """
    if err := _check_namespace(namespace):
        return err
    # Find the full pod name matching the pattern
    find_cmd = f"kubectl get pods -n {namespace} --no-headers -o custom-columns=':metadata.name' | grep {pod_name_pattern} | head -1"
    pod_name = _ssh(find_cmd)
    if not pod_name or pod_name.startswith("ERROR"):
        return f"No pod matching '{pod_name_pattern}' found in namespace '{namespace}'"
    return _ssh(f"kubectl logs {pod_name} -n {namespace} --tail={lines}")


@mcp.tool()
def describe_pod(namespace: str, pod_name_pattern: str) -> str:
    """
    Describe a pod — shows events, resource limits, volumes, and container status.
    Useful for debugging CrashLoopBackOff and pending pods.
    Use a partial name pattern.
    """
    if err := _check_namespace(namespace):
        return err
    find_cmd = f"kubectl get pods -n {namespace} --no-headers -o custom-columns=':metadata.name' | grep {pod_name_pattern} | head -1"
    pod_name = _ssh(find_cmd)
    if not pod_name or pod_name.startswith("ERROR"):
        return f"No pod matching '{pod_name_pattern}' found in namespace '{namespace}'"
    return _ssh(f"kubectl describe pod {pod_name} -n {namespace}")


@mcp.tool()
def get_events(namespace: str) -> str:
    """
    Get recent events in a namespace, sorted by time.
    Events show warnings, errors, and state changes — useful for debugging.
    """
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"kubectl get events -n {namespace} --sort-by='.lastTimestamp'")


@mcp.tool()
def get_deployments(namespace: str) -> str:
    """List all deployments in a namespace with their ready/desired replica counts."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"kubectl get deployments -n {namespace}")


@mcp.tool()
def get_services(namespace: str) -> str:
    """List all services in a namespace with their type, cluster IP, and ports."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"kubectl get services -n {namespace}")


@mcp.tool()
def get_configmaps(namespace: str) -> str:
    """List all configmaps in a namespace."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"kubectl get configmaps -n {namespace}")


@mcp.tool()
def get_persistent_volumes(namespace: str) -> str:
    """List persistent volume claims in a namespace and their bound status."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"kubectl get pvc -n {namespace}")


@mcp.tool()
def helm_list(namespace: str) -> str:
    """List all Helm releases in a namespace with their status and chart version."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"helm list -n {namespace}")


@mcp.tool()
def helm_status(namespace: str, release_name: str) -> str:
    """Get the status of a specific Helm release."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"helm status {release_name} -n {namespace}")


@mcp.tool()
def helm_get_values(namespace: str, release_name: str) -> str:
    """Get the values used to deploy a Helm release — shows actual configuration."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"helm get values {release_name} -n {namespace}")


@mcp.tool()
def get_node_status() -> str:
    """Get the status of all nodes in the cluster — shows CPU, memory, and conditions."""
    return _ssh("kubectl get nodes -o wide")


@mcp.tool()
def get_resource_usage(namespace: str) -> str:
    """Get CPU and memory usage for all pods in a namespace (requires metrics-server)."""
    if err := _check_namespace(namespace):
        return err
    return _ssh(f"kubectl top pods -n {namespace}")


# ============================================================
# WRITE TOOLS
# These modify cluster state. Always confirm with the user before running.
# ============================================================

@mcp.tool()
def helm_uninstall(namespace: str, release_name: str, confirmed: bool = False) -> str:
    """
    Uninstall a Helm release from a namespace.

    IMPORTANT: This deletes all resources created by the release.
    Set confirmed=True only after the user has explicitly approved this action.
    """
    if err := _check_namespace(namespace):
        return err
    if not confirmed:
        return (
            f"⚠️  This will uninstall release '{release_name}' from namespace '{namespace}' "
            f"and delete all associated resources.\n"
            f"To confirm, call this tool again with confirmed=True."
        )
    return _ssh(f"helm uninstall {release_name} -n {namespace}")


@mcp.tool()
def helm_upgrade(
    namespace: str,
    release_name: str,
    chart_path: str,
    set_values: str = "",
    confirmed: bool = False,
) -> str:
    """
    Upgrade a Helm release.

    Args:
        namespace: Target namespace
        release_name: Name of the existing release
        chart_path: Path to the chart on the server
        set_values: Optional --set values (e.g. 'image.tag=1.2.3')
        confirmed: Must be True to actually run — user must approve first

    IMPORTANT: Always confirm with the user before running.
    """
    if err := _check_namespace(namespace):
        return err
    cmd = f"helm upgrade {release_name} {chart_path} -n {namespace}"
    if set_values:
        cmd += f" --set {set_values}"
    if not confirmed:
        return (
            f"⚠️  This will run:\n  {cmd}\n\n"
            f"To confirm, call this tool again with confirmed=True."
        )
    return _ssh(cmd, timeout=120)


@mcp.tool()
def delete_pod(namespace: str, pod_name_pattern: str, confirmed: bool = False) -> str:
    """
    Delete a pod (it will be recreated by its deployment).
    Use a partial name pattern to find the pod.

    IMPORTANT: Always confirm with the user before running.
    """
    if err := _check_namespace(namespace):
        return err
    find_cmd = f"kubectl get pods -n {namespace} --no-headers -o custom-columns=':metadata.name' | grep {pod_name_pattern} | head -1"
    pod_name = _ssh(find_cmd)
    if not pod_name or pod_name.startswith("ERROR"):
        return f"No pod matching '{pod_name_pattern}' found in namespace '{namespace}'"
    if not confirmed:
        return (
            f"⚠️  This will delete pod '{pod_name}' in namespace '{namespace}'.\n"
            f"It will be recreated automatically by its deployment.\n"
            f"To confirm, call this tool again with confirmed=True."
        )
    return _ssh(f"kubectl delete pod {pod_name} -n {namespace}")


# --- Entry point ---
if __name__ == "__main__":
    mcp.run()
