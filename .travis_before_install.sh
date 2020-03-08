#!/bin/sh

if [ -n "$JYTHON" ];
then
    sudo apt-get update && sudo apt-get install bash curl wget fakeroot binutils java-common -y
    echo "deb http://ppa.launchpad.net/linuxuprising/java/ubuntu xenial main" | tee /tmp/linuxuprising-java.list
    sudo cp /tmp/linuxuprising-java.list /etc/apt/sources.list.d/
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 73C3DB2A 40976EAF437D05B5 3B4FE6ACC0B21F32 EA8CACC073C3DB2A
    sudo apt-get update
    apt-get download oracle-java13-installer
    fakeroot dpkg-deb -R oracle-java13-installer* /tmp/deb
    fakeroot echo '#!/bin/sh' > /tmp/deb/DEBIAN/preinst
    fakeroot dpkg-deb -b /tmp/deb/ /tmp/oracle-java13-inst.deb
    sudo dpkg -i /tmp/oracle-java13-inst.deb
    sudo apt-get install -f -y
    curl -L -o jython-installer.jar $JYTHON
    java -jar ./jython-installer.jar -s -d /opt/jython -t standard
    sudo /opt/jython/bin/jython -m ensurepip
    sudo /opt/jython/bin/pip install -U pip
    sudo /opt/jython/bin/pip install -U pytest
    echo '#!/bin/sh' >> /tmp/testrunner
    echo "sudo /opt/jython/bin/pytest" >> /tmp/testrunner
else
    pip install -U pip
    pip install -U pytest
    echo '#!/bin/sh' >> /tmp/testrunner
    echo "pytest" >> /tmp/testrunner
fi

chmod +x /tmp/testrunner
sudo cp /tmp/testrunner /usr/local/bin/
