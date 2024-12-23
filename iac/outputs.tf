output "mgmt_vm_ips" {
  value = module.mgmt_vm[*].ip_address
}

output "mgmt_vm_ids" {
  value = module.mgmt_vm[*].id
}

output "storage_vm_ips" {
  value = module.storage_vm[*].ip_address
}

output "storage_vm_ids" {
  value = module.storage_vm[*].id
}

output "worker_vm_ips" {
  value = module.worker_vm[*].ip_address
}

output "worker_vm_ids" {
  value = module.worker_vm[*].id
}
