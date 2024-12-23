output "ip_addresses" {
  value = harvester_virtualmachine.vm.network_interface[*].ip_address
}

output "id" {
  value = harvester_virtualmachine.vm.id
}
