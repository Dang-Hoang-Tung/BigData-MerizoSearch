# System variables

variable "cluster_name" {
  type    = string
  default = "merizo-search"
}

variable "username" {
  type    = string
  default = "ucabhtd"
}

variable "namespace" {
  type    = string
  default = "ucabhtd-comp0235-ns"
}

variable "network_name" {
  type    = string
  default = "ucabhtd-comp0235-ns/ds4eng"
}

variable "keyname" {
  type    = string
  default = "ucabhtd-cnc"
}

variable "img_display_name" {
  type    = string
  default = "almalinux-9.4-20240805"
}

# Machine specs

variable "mgmt_vm_cores" {
  type    = number
  default = 2
}

variable "mgmt_vm_ram" {
  type    = string
  default = "4Gi"
}

variable "mgmt_vm_hdd" {
  type    = string
  default = "10Gi"
}

variable "worker_vm_count" {
  type    = number
  default = 3
}

variable "worker_vm_cores" {
  type    = number
  default = 4
}

variable "worker_vm_ram" {
  type    = string
  default = "32Gi"
}

variable "worker_vm_hdd" {
  type    = string
  default = "25Gi"
}

variable "storage_vm_cores" {
  type    = number
  default = 4
}

variable "storage_vm_ram" {
  type    = string
  default = "8Gi"
}

variable "storage_vm_hdd" {
  type    = string
  default = "10Gi"
}

variable "storage_vm_hdd2" {
  type    = string
  default = "200Gi"
}
