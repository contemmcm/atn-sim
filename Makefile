dump1090:
	git clone https://github.com/MalcolmRobb/dump1090.git   ;\
	cd dump1090                                             ;\
	make

core:
	git clone https://github.com/coreemu/core.git   ;\
	cd core                                         ;\
	./bootstrap.sh                                  ;\
	./configure                                     ;\
	make -j8

emane:
	git clone https://github.com/adjacentlink/emane.git ;\
	git checkout v0.9.3                                 ;\
	cd emane                                            ;\
	./autogen.sh                                        ;\
	./configure                                         ;\
	make deb

all: dump1090 core emane

install: dump1090 core emane
	# CORE
	cd core ; sudo make install

	# EMANE
	cd emane/.debbuild ; sudo dpkg -i *.deb

	# DUMP 1090
	sudo cp -r dump1090 /opt

	# ATN-SIM

	sudo rm -f /usr/local/lib/python2.7/dist-packages/atn
	sudo ln -s `pwd`/atn/ /usr/local/lib/python2.7/dist-packages/atn
	sudo ln -s `pwd` /opt/atn-sim

	sudo rm -rf /etc/core
	rm -rf ~/.core
	sudo ln -s `pwd`/configs/core/etc/ /etc/core
	ln -s `pwd`/configs/core/home ~/.core

clean:
	rm -rf core
	rm -rf emane
	rm -rf dump1090

uninstall:
	sudo rm /opt/atn-sim
	sudo rm /usr/local/lib/python2.7/dist-packages/atn
	sudo rm -rf /opt/dump1090
