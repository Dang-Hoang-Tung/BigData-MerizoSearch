variable "name" {
  type = string
}

variable "description" {
  type = string
}

variable "namespace" {
  type = string
}

variable "cores" {
  type = number
}

variable "ram" {
  type = number
}

variable "network_name" {
  type = string
}

variable "root_disk_size" {
  type = string
}

variable "data_disk_size" {
  type    = string
  default = null
}

variable "cloud_init_secret_name" {
  type = string
}
