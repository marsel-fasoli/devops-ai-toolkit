# Kubernetes & Helm Skill

## Overview

This skill teaches you how to work effectively with Kubernetes clusters — navigating namespaces, debugging pods, reading logs, managing Helm releases, and troubleshooting common failures.

Read this skill at the start of any session involving Kubernetes work.

---

## Core Concepts to Keep in Mind

- **Namespace first** — always confirm which namespace before running any command
- **Read before write** — always check current state before making changes
- **Pattern matching** — use partial pod names with `grep` instead of full names (pods have random suffixes)
- **Complete logs** — always save full log files and analyze entirely, never work from snippets
- **Events are gold** — `kubectl get events` often reveals what happened faster than logs

---

## Common Commands

### Pods

```bash
# List pods with status and node
kubectl get pods -n <namespace> -o wide

# Get logs from a pod (partial name works)
kubectl logs $(kubectl get pods -n <namespace> --no-headers -o custom-columns=':metadata.name' | grep <pattern> | head -1) -n <namespace>

# Stream logs in real time
kubectl logs -f <pod-name> -n <namespace>

# Describe a pod (events, resource limits, volumes)
kubectl describe pod <pod-name> -n <namespace>

# Shell into a running pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Copy file from pod to local
kubectl cp <namespace>/<pod-name>:/path/to/file ./local-file
```

### Deployments

```bash
# List deployments
kubectl get deployments -n <namespace>

# Check rollout status
kubectl rollout status deployment/<name> -n <namespace>

# View rollout history
kubectl rollout history deployment/<name> -n <namespace>

# Rollback to previous version
kubectl rollout undo deployment/<name> -n <namespace>
```

### Events and Debugging

```bash
# Get events sorted by time (most useful for debugging)
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Get all resources in a namespace
kubectl get all -n <namespace>

# Check resource usage (requires metrics-server)
kubectl top pods -n <namespace>
kubectl top nodes
```

### Helm

```bash
# List releases in a namespace
helm list -n <namespace>

# Get status of a release
helm status <release-name> -n <namespace>

# Get values used for a release
helm get values <release-name> -n <namespace>

# Lint a chart before deploying
helm lint <chart-path>

# Dry run to preview what would be deployed
helm upgrade --dry-run <release-name> <chart-path> -n <namespace>

# Install a chart
helm install <release-name> <chart-path> -n <namespace>

# Upgrade a release
helm upgrade <release-name> <chart-path> -n <namespace>

# Uninstall a release
helm uninstall <release-name> -n <namespace>
```

---

## Debugging Patterns

### Pod not starting

1. Check pod status: `kubectl get pods -n <namespace>`
2. Describe the pod: `kubectl describe pod <name> -n <namespace>`
   - Look at **Events** section at the bottom — this usually shows the problem
   - Check **Containers** section for resource limits and image pull status
3. Check logs if the container started at all: `kubectl logs <name> -n <namespace>`
4. Check events: `kubectl get events -n <namespace> --sort-by='.lastTimestamp'`

Common causes:
- `ImagePullBackOff` — wrong image name, tag, or missing pull secret
- `CrashLoopBackOff` — container starts but crashes, check logs
- `Pending` — insufficient resources or no matching node, check events
- `OOMKilled` — container exceeded memory limit, increase limit or fix memory leak

### Pod running but service not working

1. Check service: `kubectl get svc -n <namespace>`
2. Check endpoints: `kubectl get endpoints <service-name> -n <namespace>`
   - If endpoints are empty, the service selector doesn't match any pod labels
3. Check pod labels match service selector: `kubectl get pod <name> -n <namespace> --show-labels`
4. Try port-forward to test directly: `kubectl port-forward <pod-name> <local-port>:<pod-port> -n <namespace>`

### Helm release failing

1. Check release status: `helm status <release-name> -n <namespace>`
2. Check values: `helm get values <release-name> -n <namespace>`
3. Always lint before deploying: `helm lint <chart-path>`
4. Use dry-run to preview: `helm upgrade --dry-run <release-name> <chart-path> -n <namespace>`
5. Check pod events after deploy: `kubectl get events -n <namespace> --sort-by='.lastTimestamp'`

### Storage issues

```bash
# Check PVC status
kubectl get pvc -n <namespace>

# Check PV status
kubectl get pv

# Describe PVC for binding issues
kubectl describe pvc <pvc-name> -n <namespace>
```

Common causes:
- `Pending` PVC — no matching PV, or storage class not available
- `Released` PV — PV was used by a deleted PVC, needs manual cleanup before reuse

---

## Working Rules for Kubernetes

- **Never run `helm install/upgrade/uninstall`** without showing the command first and waiting for user approval
- **Never run `kubectl delete`** without showing what will be deleted and waiting for approval
- **Read-only commands are safe** — `get`, `describe`, `logs`, `events`, `top` can run without asking
- **Always confirm the namespace** before any operation — wrong namespace is a common and costly mistake
- **Check before changing** — always look at current state before modifying anything
- **Backward compatibility** — when editing Helm charts, never change defaults that existing deployments depend on
- **Test with dry-run** — always use `--dry-run` before applying Helm changes in production

---

## Useful Patterns

### Find a pod by partial name

```bash
kubectl get pods -n <namespace> | grep <partial-name>
```

### Save complete logs to file for analysis

```bash
kubectl logs <pod-name> -n <namespace> > /tmp/pod-logs.txt
```

### Watch pod status in real time

```bash
kubectl get pods -n <namespace> -w
```

### Get pod's environment variables

```bash
kubectl exec <pod-name> -n <namespace> -- env
```

### Check what image a pod is running

```bash
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}'
```
