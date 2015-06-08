# spring-xd-packaing
Packaging and release code and artifacts for Spring XD

### For the RPM build:

Prepare by copying `spring-xd-1.2.0.{version}-dist.zip` to `rpmbuild/SOURCES/`

Build using:

    $ rpmbuild -bb rpmbuild/SPECS/spring-xd-noarch.spec
