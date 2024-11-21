/* Core modules of the data analysis cluster. */

# Reusable names
locals {
  host_vm_name    = "${var.vm_name_prefix}-mgmt-${random_id.secret.hex}"
  worker_vm_name  = "${var.vm_name_prefix}-worker-${random_id.secret.hex}"
  storage_vm_name = "${var.vm_name_prefix}-storage-${random_id.secret.hex}"
}

resource "random_id" "secret" {
  byte_length = 5
}

# Cloud config with secret
resource "harvester_cloudinit_secret" "cloud_config" {
  name      = "cloud-config-${random_id.secret.hex}"
  namespace = var.namespace

  user_data = templatefile("cloud-init.tmpl.yml", {
    public_key_openssh = data.harvester_ssh_key.mysshkey.public_key
  })
}

# Host VM
resource "harvester_virtualmachine" "host_vm" {
  name                 = local.host_vm_name
  namespace            = var.namespace
  restart_after_update = true

  description = "Cluster Head Node"

  cpu    = var.host_vm_cores
  memory = var.host_vm_ram

  efi         = true
  secure_boot = false

  run_strategy    = "RerunOnFailure"
  hostname        = local.host_vm_name
  reserved_memory = "100Mi"
  machine_type    = "q35"

  network_interface {
    name           = "nic-1"
    wait_for_lease = true
    type           = "bridge"
    network_name   = var.network_name
  }

  disk {
    name       = "root-disk"
    type       = "disk"
    size       = var.host_vm_hdd
    bus        = "virtio"
    boot_order = 1

    image       = data.harvester_image.img.id
    auto_delete = true
  }

  cloudinit {
    user_data_secret_name = harvester_cloudinit_secret.cloud_config.name
  }
}

# Worker VMs
resource "harvester_virtualmachine" "worker_vm" {
  count = var.worker_vm_count

  name                 = "${local.worker_vm_name}-${format("%02d", count.index + 1)}"
  namespace            = var.namespace
  restart_after_update = true

  description = "Cluster Compute Node"

  cpu    = var.worker_vm_cores
  memory = var.worker_vm_ram

  efi         = true
  secure_boot = false

  run_strategy    = "RerunOnFailure"
  hostname        = "${local.worker_vm_name}-${format("%02d", count.index + 1)}"
  reserved_memory = "100Mi"
  machine_type    = "q35"

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

# Storage VM
resource "harvester_virtualmachine" "storage_vm" {
  name                 = local.storage_vm_name
  namespace            = var.namespace
  restart_after_update = true

  description = "Cluster Storage Node"

  cpu    = var.storage_vm_cores
  memory = var.storage_vm_ram

  efi         = true
  secure_boot = false

  run_strategy    = "RerunOnFailure"
  hostname        = local.storage_vm_name
  reserved_memory = "100Mi"
  machine_type    = "q35"

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

    image       = data.harvester_image.img.id
    auto_delete = true
  }

  cloudinit {
    user_data_secret_name = harvester_cloudinit_secret.cloud_config.name
  }
}
