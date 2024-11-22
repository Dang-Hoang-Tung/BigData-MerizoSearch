output "mgmt_vm_ips" {
  value = harvester_virtualmachine.mgmt_vm[*].network_interface[0].ip_address
}

output "mgmt_vm_ids" {
  value = harvester_virtualmachine.mgmt_vm[*].id
}

output "worker_vm_ips" {
  value = harvester_virtualmachine.worker_vm[*].network_interface[0].ip_address
}

output "worker_vm_ids" {
  value = harvester_virtualmachine.worker_vm[*].id
}

output "storage_vm_ips" {
  value = harvester_virtualmachine.storage_vm[*].network_interface[0].ip_address
}

output "storage_vm_ids" {
  value = harvester_virtualmachine.storage_vm[*].id
}
