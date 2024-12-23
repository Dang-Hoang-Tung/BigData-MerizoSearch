/* Core modules of the data analysis cluster. */

# Reusable names
locals {
  cloud_config_name = "${var.cluster_name}-cloud-config"
  mgmt_vm_name      = "${var.cluster_name}-mgmt"
  worker_vm_name    = "${var.cluster_name}-worker"
  storage_vm_name   = "${var.cluster_name}-storage"
}

data "harvester_ssh_key" "mysshkey" {
  name      = var.keyname
  namespace = var.namespace
}

data "harvester_image" "img" {
  display_name = var.img_display_name
  namespace    = "harvester-public"
}

# Cloud config with secret
resource "harvester_cloudinit_secret" "cloud_config" {
  name      = local.cloud_config_name
  namespace = var.namespace

  user_data = templatefile("cloud-init.tmpl.yml", {
    public_key_openssh = data.harvester_ssh_key.mysshkey.public_key
  })
}

# Management VM
module "mgmt_vm" {
  source = "./virtual_machine"

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
    condenser_ingress_isEnabled     = true
    condenser_ingress_isAllowed     = true
    condenser_ingress_hdfs_hostname = "hdfs-${var.username}"
    condenser_ingress_hdfs_port     = 9870
    condenser_ingress_yarn_hostname = "yarn-${var.username}"
    condenser_ingress_yarn_port     = 8088
  }
}

# Storage VM
module "storage_vm" {
  source = "./virtual_machine"

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
}

# Worker VMs
module "worker_vm" {
  source = "./virtual_machine"
  count  = var.worker_vm_count

  name        = "${local.worker_vm_name}-${count.index + 1}"
  description = "Cluster compute node"
  namespace   = var.namespace

  cores = var.worker_vm_cores
  ram   = var.worker_vm_ram

  network_name           = var.network_name
  root_disk_size         = var.worker_vm_hdd
  root_disk_image        = data.harvester_image.img.id
  cloud_init_secret_name = harvester_cloudinit_secret.cloud_config.name
}
