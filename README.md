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

## Reprovisioning the VM
If you make changes to the Vagrantfile after the virtual machine (VM) is already created, you can reprovision the VM:

```shell
    $ exit
    $ vagrant reload --provision
    $ vagrant ssh
```

## Manually Installing Requirements 

Install the necessary packages by running:
```shell
    $ pip install -r requirements.txt
```

## Running the Flask app

Create a .env file in the directory and add the content from: https://github.com/nyu-devops-team/customers/blob/data-model/dot-env-example

Then you can run the Flask app: 

```shell
    $ flask run --host=0.0.0.0
```

Note: since you are running the service inside a virtual machine, you have to set the host to a public server so that the service can be accessible outside of the VM.

## Manually Running the Tests

Run the tests using `nose`

```shell
    $ nosetests
```

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
    $ coverage report -m
```

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases to get higher code coverage.

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
    $ nosetests --with-coverage --cover-package=service
```

Try and get as close to 100% coverage as you can.

It's also a good idea to make sure that your Python code follows the PEP8 standard. `flake8` has been included in the `requirements.txt` file so that you can check if your code is compliant like this:

```shell
    $ flake8 --count --max-complexity=10 --statistics model,service
```

I've also include `pylint` in the requirements. If you use a programmer's editor like Atom.io you can install plug-ins that will use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

```shell
    $ pylint service
    $ pylint tests
```