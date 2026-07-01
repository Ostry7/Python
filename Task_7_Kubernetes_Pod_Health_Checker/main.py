from kubernetes import client, config
config.load_kube_config()

v1 = client.CoreV1Api()
print("NAMESPACE    |   POD_NAME    |   POD_STATUS")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print(f"{i.metadata.namespace} | {i.metadata.name} | {i.status.phase}")
