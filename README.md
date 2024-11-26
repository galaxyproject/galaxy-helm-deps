# Galaxy Helm Dependencies Chart (v1)

This is a companion repo to the [Galaxy Helm Chart](https://github.com/galaxyproject/galaxy-helm)
for more conveniently deploying global environmental dependencies required by the Galaxy helm chart,
such as the Postgres operator, RabbitMQ operator, CVMFS and S3FS. These dependencies cannot be
bundled with the Galaxy Chart itself because they are usually installed once per cluster. We recommend
installing this chart prior to installing Galaxy helm.

## Supported software versions

- Kubernetes 1.27+
- Helm 3.5+

## Kubernetes cluster

You will need `kubectl` ([instructions](https://kubernetes.io/docs/tasks/tools/#kubectl))
and `Helm` ([instructions](https://helm.sh/docs/intro/install/)) installed.

## Dependency charts

This chart relies on the features of other charts for common functionality:
- [postgres-operator](https://cloudnative-pg.io/documentation/current/) for the
  database;
- [galaxy-cvmfs-csi](https://github.com/CloudVE/galaxy-cvmfs-csi-helm) for linking the
  reference data to Galaxy and jobs based on CVMFS (default).
- [k8s-csi-s3](https://github.com/yandex-cloud/k8s-csi-s3/tree/master/deploy/helm/csi-s3) for linking
  reference data to Galaxy and jobs based on S3FS (optional/alternative to CVMFS).
- [rabbitmq-cluster-operator](https://github.com/rabbitmq/cluster-operator) for deploying
  the message queue.

---

## Installing the chart

### Using the chart from the packaged chart repo

1. The chart is automatically packaged, versioned and uploaded to a helm repository
on each accepted PR. Therefore, the latest version of the chart can be downloaded
from this repository.

```console
helm repo add cloudve https://raw.githubusercontent.com/CloudVE/helm-charts/master/
helm repo update
```

2. Install the chart

```console
helm install --create-namespace -n "galaxy-deps" galaxy-deps galaxyproject/galaxy-deps
```

### Using the chart from GitHub repo

1. Clone this repository:

```console
git clone https://github.com/galaxyproject/galaxy-helm.git
```

2. Setup the chart

```console
cd galaxy-helm/galaxy-deps
helm dependency update
helm install --create-namespace -n "galaxy-deps" galaxy-deps .
```

## Uninstalling the chart

To uninstall/delete the `galaxy-deps` chart, run:

```console
helm delete -n "galaxy-deps" galaxy-deps
```

## Configuration

The following table lists the configurable parameters of this chart. The
current default values can be found in `values.yaml` file.

| Parameters                                 | Description                                                                                                                                                                                                |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cvmfs.deploy`                             | Whether to deploy the CVMFS sub chart. Default is true.                                                                                                                                                    |
| `cvmfs.{}`                                 | Refer to the [galaxy cvmfs chart](https://github.com/CloudVE/galaxy-cvmfs-csi-helm) for possible configuration values.                                                                                     |
| `postgresql.deploy`                        | Whether to deploy the postgres sub chart. Default is true.                                                                                                                                                 |
| `postgresql.{}`                            | Refer to the [postgres-operator chart](https://cloudnative-pg.io/documentation/current/) for possible configuration values.                                                                                    |
| `rabbitmq.deploy`                          | Whether to deploy the rabbitmq sub chart. Default is true.                                                                                                                                                 |
| `rabbitmq.{}`                              | Refer to the [rabbitmq-cluster-operator chart](https://github.com/rabbitmq/cluster-operator) for possible configuration values.                                                                            |
| `s3csi.deploy`                             | Whether to deploy the csi-s3 sub chart as an alternative to cvmfs. Default is false.                                                                                                                       |
| `s3csi.{}`                                 | Refer to the [k8s-csi-s3 chart](https://github.com/yandex-cloud/k8s-csi-s3/tree/master/deploy/helm/csi-s3) for possible configuration values.                                                              |
