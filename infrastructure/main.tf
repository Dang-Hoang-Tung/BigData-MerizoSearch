/* Core modules of the data analysis cluster. */

# Reusable variables
locals {
  # Cluster ID
  cluster_id = random_id.secret.hex
  # Cloud config name
  cloud_config_name = "${var.cluster_name}-cloud-config-${local.cluster_id}"
  # VM names
  mgmt_vm_name    = "${var.cluster_name}-mgmt-${local.cluster_id}"
  storage_vm_name = "${var.cluster_name}-storage-${local.cluster_id}"
  worker_vm_name  = "${var.cluster_name}-worker"
  # Hostnames
  hostnames = {
    hdfs          = "hdfs-${local.cluster_id}"
    yarn          = "yarn-${local.cluster_id}"
    prometheus    = "prometheus-${local.cluster_id}"
    node_exporter = "nodeexporter-${local.cluster_id}"
    grafana       = "grafana-${local.cluster_id}"
    minio_s3      = "s3-${local.cluster_id}"
    minio_console = "cons-${local.cluster_id}"
  }
}

data "harvester_ssh_key" "mysshkey" {
  name      = var.keyname
  namespace = var.namespace
}

data "harvester_image" "img" {
  display_name = var.img_display_name
  namespace    = "harvester-public"
}

resource "random_id" "secret" {
  byte_length = 8
}

# Cloud config with secret
resource "harvester_cloudinit_secret" "cloud_config" {
  name      = local.cloud_config_name
  namespace = var.namespace

  user_data = templatefile("cloud_init.tmpl.yml", {
    public_key_openssh = data.harvester_ssh_key.mysshkey.public_key
  })
}

# Management VM
module "mgmt_vm" {
  source = "./modules/virtual-machine"

  name        = local.mgmt_vm_name
  description = "Cluster head node"
  namespace   = var.namespace

  cores = var.mgmt_vm_cores
  ram   = var.mgmt_vm_ram

  network_name           = var.network_name
  root_disk_size         = var.mgmt_vm_hdd
  root_disk_image        = data.harvester_image.img.id
  cloud_init_secret_name = harvester_cloudinit_secret.cloud_config.name

  tags = {
    # Ingress configurations
    condenser_ingress_isEnabled           = true
    condenser_ingress_isAllowed           = true
    condenser_ingress_hdfs_hostname       = local.hostnames.hdfs
    condenser_ingress_hdfs_port           = 9870
    condenser_ingress_yarn_hostname       = local.hostnames.yarn
    condenser_ingress_yarn_port           = 8088
    condenser_ingress_prometheus_hostname = local.hostnames.prometheus
    condenser_ingress_prometheus_port     = 9090
    condenser_ingress_grafana_hostname    = local.hostnames.grafana
    condenser_ingress_grafana_port        = 3000
  }
}

# Storage VM
module "storage_vm" {
  source = "./modules/virtual-machine"

  name        = local.storage_vm_name
  description = "Cluster storage node"
  namespace   = var.namespace

  cores = var.storage_vm_cores
  ram   = var.storage_vm_ram

  network_name           = var.network_name
  root_disk_size         = var.storage_vm_hdd
  root_disk_image        = data.harvester_image.img.id
  data_disk_size         = var.storage_vm_hdd2
  cloud_init_secret_name = harvester_cloudinit_secret.cloud_config.name

  tags = {
    # Ingress configurations
    condenser_ingress_isEnabled                  = true
    condenser_ingress_isAllowed                  = true
    condenser_ingress_os_hostname                = local.hostnames.minio_s3
    condenser_ingress_os_port                    = 9000
    condenser_ingress_os_protocol                = "https"
    condenser_ingress_os_nginx_proxy-body-size   = "100000m"
    condenser_ingress_cons_hostname              = local.hostnames.minio_console
    condenser_ingress_cons_port                  = 9001
    condenser_ingress_cons_protocol              = "https"
    condenser_ingress_cons_nginx_proxy-body-size = "100000m"
  }
}

# Worker VMs
module "worker_vm" {
  source = "./modules/virtual-machine"
  count  = var.worker_vm_count

  name        = "${local.worker_vm_name}-${count.index + 1}-${local.cluster_id}"
  description = "Cluster compute node ${count.index + 1}"
  namespace   = var.namespace

  cores = var.worker_vm_cores
  ram   = var.worker_vm_ram

  network_name           = var.network_name
  root_disk_size         = var.worker_vm_hdd
  root_disk_image        = data.harvester_image.img.id
  cloud_init_secret_name = harvester_cloudinit_secret.cloud_config.name

  tags = {
    # Ingress configurations
    condenser_ingress_isEnabled             = true
    condenser_ingress_isAllowed             = true
    # condenser_ingress_hdfs_hostname         = "${local.hostnames.hdfs}-${count.index + 1}"
    # condenser_ingress_hdfs_port             = 9864
    condenser_ingress_yarn_hostname         = "${local.hostnames.yarn}-${count.index + 1}"
    condenser_ingress_yarn_port             = 8042
    condenser_ingress_nodeexporter_hostname = "${local.hostnames.node_exporter}-${count.index + 1}"
    condenser_ingress_nodeexporter_port     = 9100
  }
}
