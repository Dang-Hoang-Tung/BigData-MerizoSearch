variable "img_display_name" {
  type    = string
  default = "almalinux-9.4-20240805"
}

variable "namespace" {
  type    = string
  default = "ucabhtd-comp0235-ns"
}

variable "network_name" {
  type    = string
  default = "ucabhtd-comp0235-ns/ds4eng"
}

# variable "username" {
#   type    = string
#   default = "ucabhtd"
# }

variable "keyname" {
  type    = string
  default = "ucabhtd-cnc"
}

variable "vm_name_prefix" {
  type    = string
  default = "data-analysis"
}

# Machine specs

# locals {
#   host_cores = 2
#   host_ram   = "4Gi"
#   host_hdd   = "10Gi"

#   worker_count = 3
#   worker_cores = 4
#   worker_ram   = "32Gi"
#   worker_hdd   = "25Gi"

#   storage_cores = 4
#   storage_ram   = "8Gi"
#   storage_hdd   = "10Gi"
#   storage_hdd2  = "200Gi"
# }

variable "host_vm_cores" {
  type = number
  # default = 2
}

variable "host_vm_ram" {
  type = string
  # default = "4Gi"
}

variable "host_vm_hdd" {
  type = string
  # default = "10Gi"
}

variable "worker_vm_count" {
  type = number
  # default = 3
}

variable "worker_vm_cores" {
  type = number
  # default = 4
}

variable "worker_vm_ram" {
  type = string
  # default = "32Gi"
}

variable "worker_vm_hdd" {
  type = string
  # default = "25Gi"
}

variable "storage_vm_cores" {
  type = number
  # default = 4
}

variable "storage_vm_ram" {
  type = string
  # default = "8Gi"
}

variable "storage_vm_hdd" {
  type = string
  # default = "10Gi"
}

variable "storage_vm_hdd2" {
  type = string
  # default = "200Gi"
}
