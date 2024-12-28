# Reusable module for creating a virtual machine
resource "harvester_virtualmachine" "vm" {
  name        = var.name
  hostname    = var.name
  description = var.description
  namespace   = var.namespace

  cpu    = var.cores
  memory = var.ram

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
    name        = "root-disk"
    type        = "disk"
    size        = var.root_disk_size
    bus         = "virtio"
    boot_order  = 1
    auto_delete = true
    image       = var.root_disk_image
  }

  dynamic "disk" {
    # Only create a data disk if the size is specified
    for_each = var.data_disk_size != null ? ["provision"] : []
    content {
      name        = "data-disk"
      type        = "disk"
      size        = var.data_disk_size
      bus         = "virtio"
      boot_order  = 2
      auto_delete = true
    }
  }

  cloudinit {
    user_data_secret_name = var.cloud_init_secret_name
  }

  tags = var.tags
}
