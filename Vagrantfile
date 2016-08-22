# -*- mode: ruby -*-
# vi: set ft=ruby sw=2 :

Vagrant.configure(2) do |config|
  config.vm.provider :libvirt do |domain|
    domain.memory = 1024
    domain.cpu = 1
  end

  config.vm.define :c6, autostart: false do |c6|
    c6.vm.box = "c6"
  end
  
  config.vm.define :c7, autostart: false do |c7|
    c7.vm.box = "c7"
  end
end
