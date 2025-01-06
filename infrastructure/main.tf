/* Core modules of the data analysis cluster. */

# Reusable names
locals {
  cloud_config_name     = "${var.cluster_name}-cloud-config-${random_id.secret.hex}"
  mgmt_vm_name          = "${var.cluster_name}-mgmt-${random_id.secret.hex}"
  storage_vm_name       = "${var.cluster_name}-storage-${random_id.secret.hex}"
  worker_vm_name_prefix = "${var.cluster_name}-worker"
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
    condenser_ingress_isEnabled      = true
    condenser_ingress_isAllowed      = true
    condenser_ingress_hdfs_hostname  = "hdfs-${var.username}"
    condenser_ingress_hdfs_port      = 9870
    condenser_ingress_yarn_hostname  = "yarn-${var.username}"
    condenser_ingress_yarn_port      = 8088
    condenser_ingress_spark_hostname = "spark-${var.username}"
    condenser_ingress_spark_port     = 4040
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
    condenser_ingress_os_hostname                = "${var.username}-s3"
    condenser_ingress_os_port                    = 9000
    condenser_ingress_os_protocol                = "https"
    condenser_ingress_os_nginx_proxy-body-size   = "100000m"
    condenser_ingress_cons_hostname              = "${var.username}-cons"
    condenser_ingress_cons_port                  = 9001
    condenser_ingress_cons_protocol              = "https"
    condenser_ingress_cons_nginx_proxy-body-size = "100000m"
  }
}

# Worker VMs
module "worker_vm" {
  source = "./modules/virtual-machine"
  count  = var.worker_vm_count

  name        = "${local.worker_vm_name_prefix}-${count.index + 1}-${random_id.secret.hex}"
  description = "Cluster compute node"
  namespace   = var.namespace

  cores = var.worker_vm_cores
  ram   = var.worker_vm_ram

  network_name           = var.network_name
  root_disk_size         = var.worker_vm_hdd
  root_disk_image        = data.harvester_image.img.id
  cloud_init_secret_name = harvester_cloudinit_secret.cloud_config.name
}
