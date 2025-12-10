Crash A2 — OOMKilled due to tiny memory limits
Create failure (crash-oom.yaml):
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: oom-trigger
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: oom-trigger
          template:
            metadata:
              labels:
                app: oom-trigger
            spec:
              containers:
              - name: memhog
                image: python:3.11-alpine
                # This Python creates a ~200MB string then sleeps, causing resident memory allocation.
                command: ["sh", "-c", "python - <<'PY'\n# allocate ~200MB string\ns = 'x' * 200_000_000\nimport time\nprint('allocated', len(s))\ntime.sleep(300)\nPY"]
                resources:
                  requests:
                    memory: "20Mi"
                  limits:
                    memory: "50Mi"


kubectl apply -f crash-oom.yaml
kubectl get pods -w
kubectl describe pod <pod-name>

Symptoms
Pod shows OOMKilled


kubectl describe shows OOM events


Fix
 Increase requests/limits to appropriate values or change the workload to less memory-hungry. Example:
requests: { memory: "256Mi" }
limits:   { memory: "512Mi" }

kubectl apply -f corrected file.
Interview line
“Pod was OOMKilled from incorrect resource sizing; I inspected events, updated resource requests/limits, and added HPA/monitoring to avoid future surprises.”
