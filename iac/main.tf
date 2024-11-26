/* Core modules of the data analysis cluster. */

# Reusable names
locals {
  cloud_config_name = "${var.cluster_name}-cloud-config"

  mgmt_vm_name    = "${var.cluster_name}-mgmt"
  worker_vm_name  = "${var.cluster_name}-worker"
  storage_vm_name = "${var.cluster_name}-storage"
}

resource "random_id" "secret" {
  byte_length = 5
}

# Cloud config with secret
resource "harvester_cloudinit_secret" "cloud_config" {
  name      = "${local.cloud_config_name}-${random_id.secret.hex}"
  namespace = var.namespace

  user_data = templatefile("cloud-init.tmpl.yml", {
    public_key_openssh = data.harvester_ssh_key.mysshkey.public_key
  })
}

# Management VM
resource "harvester_virtualmachine" "mgmt_vm" {
  name        = local.mgmt_vm_name
  hostname    = local.mgmt_vm_name
  description = "Cluster head node"
  namespace   = var.namespace

  cpu    = var.mgmt_vm_cores
  memory = var.mgmt_vm_ram

  restart_after_update = true
  efi                  = true
  secure_boot          = false
  run_strategy         = "RerunOnFailure"
  reserved_memory      = "100Mi"
  machine_type         = "q35"

  network_interface {
    name           = "nic-1"
    wait_for_lease = true
    type           = "bridge"
    network_name   = var.network_name
  }

  disk {
    name       = "root-disk"
    type       = "disk"
    size       = var.mgmt_vm_hdd
    bus        = "virtio"
    boot_order = 1

    image       = data.harvester_image.img.id
    auto_delete = true
  }

  cloudinit {
    user_data_secret_name = harvester_cloudinit_secret.cloud_config.name
  }
}

# Storage VM
resource "harvester_virtualmachine" "storage_vm" {
  name        = local.storage_vm_name
  hostname    = local.storage_vm_name
  description = "Cluster storage node"
  namespace   = var.namespace

  cpu    = var.storage_vm_cores
  memory = var.storage_vm_ram

  restart_after_update = true
  efi                  = true
  secure_boot          = false
  run_strategy         = "RerunOnFailure"
  reserved_memory      = "100Mi"
  machine_type         = "q35"

  network_interface {
    name           = "nic-1"
    wait_for_lease = true
    type           = "bridge"
    network_name   = var.network_name
  }

  disk {
    name       = "root-disk"
    type       = "disk"
    size       = var.storage_vm_hdd
    bus        = "virtio"
    boot_order = 1

    image       = data.harvester_image.img.id
    auto_delete = true
  }

  disk {
    name       = "data-disk"
    type       = "disk"
    size       = var.storage_vm_hdd2
    bus        = "virtio"
    boot_order = 2

    auto_delete = true
  }

  cloudinit {
    user_data_secret_name = harvester_cloudinit_secret.cloud_config.name
  }
}

# Worker VMs
resource "harvester_virtualmachine" "worker_vm" {
  count = var.worker_vm_count

  name        = "${local.worker_vm_name}-${count.index + 1}"
  hostname    = "${local.worker_vm_name}-${count.index + 1}"
  description = "Cluster compute node"
  namespace   = var.namespace

  cpu    = var.worker_vm_cores
  memory = var.worker_vm_ram

  restart_after_update = true
  efi                  = true
  secure_boot          = false
  run_strategy         = "RerunOnFailure"
  reserved_memory      = "100Mi"
  machine_type         = "q35"

  network_interface {
    name           = "nic-1"
    wait_for_lease = true
    type           = "bridge"
    network_name   = var.network_name
  }

  disk {
    name       = "root-disk"
    type       = "disk"
    size       = var.worker_vm_hdd
    bus        = "virtio"
    boot_order = 1

    image       = data.harvester_image.img.id
    auto_delete = true
  }

  cloudinit {
    user_data_secret_name = harvester_cloudinit_secret.cloud_config.name
  }
}
