# customers
The customers resource is a representation of the customer accounts of the eCommerce site

## Prerequisite Installation using Vagrant

The easiest way to setup the environment is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

```shell
    git clone https://github.com/nyu-devops-team/customers.git
    cd customers
    vagrant up
    vagrant ssh
    cd /vagrant
```

When you are done, you can exit and shut down the vm with:

```shell
    $ exit
    $ vagrant halt
```
