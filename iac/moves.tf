moved {
  from = harvester_virtualmachine.mgmt_vm
  to   = module.mgmt_vm.harvester_virtualmachine.vm
}

moved {
  from = harvester_virtualmachine.storage_vm
  to   = module.storage_vm.harvester_virtualmachine.vm
}

moved {
  from = harvester_virtualmachine.worker_vm[0]
  to   = module.worker_vm[0].harvester_virtualmachine.vm
}

moved {
  from = harvester_virtualmachine.worker_vm[1]
  to   = module.worker_vm[1].harvester_virtualmachine.vm
}

moved {
  from = harvester_virtualmachine.worker_vm[2]
  to   = module.worker_vm[2].harvester_virtualmachine.vm
}
