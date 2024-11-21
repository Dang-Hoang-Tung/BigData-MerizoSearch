variable img_display_name {
  type = string
  default = "almalinux-9.4-20240805"
}

variable namespace {
  type = string
  default ="ucabhtd-comp0235-ns"
}

variable network_name {
  type = string
  default = "ucabhtd-comp0235-ns/ds4eng"
}

variable username {
  type = string
  default = "ucabhtd"
}

variable keyname {
  type = string
  default = "ucabhtd-cnc"
}

variable vm_count {
  type    = number
  default = 4
}
