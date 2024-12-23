output "mgmt_vm_ips" {
  value = module.mgmt_vm.ips
}

output "mgmt_vm_ids" {
  value = module.mgmt_vm.ids
}

output "worker_vm_ips" {
  value = concat(module.worker_vm[*].ips)
}

output "worker_vm_ids" {
  value = concat(module.worker_vm[*].ids)
}

output "storage_vm_ips" {
  value = module.storage_vm.ips
}

output "storage_vm_ids" {
  value = module.storage_vm.ids
}
