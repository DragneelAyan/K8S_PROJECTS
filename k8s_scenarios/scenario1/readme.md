Setup (one-time)

# create a kind cluster (single-node)

kind create cluster --name devops-practice

# confirm kube context

kubectl cluster-info --context kind-devops-practice
kubectl get nodes

If your cluster name is different, substitute it. Ready? Let’s break things.

Part A — CrashLoopBackOff (3 variations)
Common debugging commands (use these first every time)
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -c <container-name> -n <namespace> # if container restarts, add --previous
kubectl get events --sort-by=.metadata.creationTimestamp -A

Crash A1 — Liveness probe misconfigured (HTTP path wrong)

What to do (create failure)
Save as crash-probe-bad.yaml:

apiVersion: apps/v1
kind: Deployment
metadata:
name: probe-bad
spec:
replicas: 1
selector: { matchLabels: { app: probe-bad } }
template:
metadata: { labels: { app: probe-bad } }
spec:
containers: - name: web
image: nginx:stable
ports: [{ containerPort: 80 }]
livenessProbe:
httpGet:
path: /not-exist # WRONG path -> will fail
port: 80
initialDelaySeconds: 2
periodSeconds: 2

kubectl apply -f crash-probe-bad.yaml
kubectl get pods -w

Symptoms

Pod Restarts repeatedly

kubectl describe pod → Liveness probe failed

Fix
Edit to correct path or remove probe:

kubectl edit deployment probe-bad

# change path to / or increase initialDelaySeconds

# OR apply corrected YAML:

# (use path: /)

Apply corrected YAML probe-proper.yaml (set path / and initialDelaySeconds:10). Then:

kubectl rollout restart deployment/probe-bad
kubectl get pods

Interview line:

“CrashLoopBackOff caused by a misconfigured liveness probe; I used kubectl describe and logs, adjusted probe thresholds and initialDelay, and stabilized the pod. Prevented recurrence by adding probe validations to CI.”
