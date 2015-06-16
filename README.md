# spring-xd-packaging

Packaging and release code and artifacts for Spring XD

## Prepare for a new version

Update `rpmbuild/SPECS/spring-xd-noarch.spec` with the current version. Also, create a Git tag for the version.

Next, build the RPM using one of the following methods:


### Building the Spring XD Release RPM from a RedHat/CentOS system:

Prepare by copying `spring-xd-{new-release-version}-dist.zip` to `rpmbuild/SOURCES/`

Build using:

    $ rpmbuild -bb rpmbuild/SPECS/spring-xd-noarch.spec

The Spring XD RPM should now be available in `rpmbuild/RPMS/noarch`


### Building Spring XD Release RPM with Vagrant

You need to install [Vagrant](http://docs.vagrantup.com/v2/installation/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads). Then add the `chef/centos-6.5` box for VirtualBox.

We are providing a Vagrant file for easy building of the RPM. Follow these steps from the root directory of this project:

    vagrant up

That should start the VM and you can now ssh to it using:

    vagrant ssh

The first time the VM is started we should install `rpm-build`

    $ sudo yum -y install rpm-build

Now copy the Spring XD release distribution zip file (set XD_VERSION to the correct version):

    $ export XD_VERSION='{new-release-version}'
    $ export XD_REPO='http://repo.spring.io/libs-release-local'
    $ wget -P rpmbuild/SOURCES  ${XD_REPO}/org/springframework/xd/spring-xd/${XD_VERSION}/spring-xd-${XD_VERSION}-dist.zip

Finally build the RPM:

    $ rpmbuild -bb rpmbuild/SPECS/spring-xd-noarch.spec

The Spring XD RPM should now be available in `rpmbuild/RPMS/noarch`
