output "ips" {
  value = harvester_virtualmachine.vm[*].network_interface[0].ip_address
}

output "ids" {
  value = harvester_virtualmachine.vm[*].id
}
