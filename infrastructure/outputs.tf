output "mgmt_vm_ips" {
  value = flatten(module.mgmt_vm[*].ip_addresses)
}

output "mgmt_vm_ids" {
  value = module.mgmt_vm[*].id
}

output "storage_vm_ips" {
  value = flatten(module.storage_vm[*].ip_addresses)
}

output "storage_vm_ids" {
  value = module.storage_vm[*].id
}

output "worker_vm_ips" {
  value = flatten(module.worker_vm[*].ip_addresses)
}

output "worker_vm_ids" {
  value = module.worker_vm[*].id
}

output "hostnames" {
  value = local.hostnames
}
