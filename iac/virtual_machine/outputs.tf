output "ip_address" {
  value = harvester_virtualmachine.vm.network_interface[0].ip_address
}

output "id" {
  value = harvester_virtualmachine.vm.id
}
